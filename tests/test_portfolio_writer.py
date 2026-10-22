import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'tooling' / 'portfolio_writer.py'
SPEC = importlib.util.spec_from_file_location('portfolio_writer', SOURCE)
writer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(writer)


def op(url='https://github.com/dornglut/runenwerk/issues/1276',
       status='Blocked', present=False, **overrides):
    result = {
        'url': url, 'status': status, 'priority': 'P1', 'kind': 'Delivery',
        'expected': {'present': False} if not present else {
            'present': True, 'status': 'Ready', 'priority': 'P2', 'kind': None},
    }
    result.update(overrides)
    return result


def envelope(operations=None, ensure_kind=False):
    return {'schema': 1, 'project': 'dornglut/1', 'ensure_kind': ensure_kind,
            'operations': [op()] if operations is None and not ensure_kind
            else ([] if operations is None else operations)}


def payload(request):
    raw = writer.canonical_json(request)
    body = '```json\n' + json.dumps(request, indent=2) + '\n```'
    return body, hashlib.sha256(raw).hexdigest()


def field(name, options):
    return {'__typename': 'ProjectV2SingleSelectField', 'id': 'field-' + name,
            'name': name, 'options': [{'name': x, 'id': 'option-' + x} for x in options]}


def project_page(nodes=None, kind=True, has_next=False, cursor=None, total=None, private=False):
    fields = [field('Status', writer.STATUSES), field('Priority', writer.PRIORITIES)]
    if kind:
        fields.append(field('Kind', writer.KINDS))
    nodes = [] if nodes is None else nodes
    return {'organization': {'projectV2': {
        'id': 'PVT_1', 'number': 1, 'url': 'https://github.com/orgs/dornglut/projects/1',
        'public': not private,
        'fields': {'pageInfo': {'hasNextPage': False}, 'nodes': fields},
        'items': {'totalCount': len(nodes) if total is None else total,
                  'pageInfo': {'hasNextPage': has_next, 'endCursor': cursor},
                  'nodes': nodes},
    }}}


def project_item(url, status='Ready', priority='P2', kind=None, private=False):
    vals = []
    for name, value in [('Status', status), ('Priority', priority), ('Kind', kind)]:
        if value is not None:
            vals.append({'__typename': 'ProjectV2ItemFieldSingleSelectValue',
                         'name': value, 'field': {'name': name}})
    return {
        'id': 'PVTI_1', 'type': 'ISSUE', 'isArchived': False,
        'content': {'__typename': 'Issue', 'url': url, 'state': 'OPEN',
                    'repository': {'isPrivate': private, 'nameWithOwner': 'dornglut/runenwerk'}},
        'fieldValues': {'pageInfo': {'hasNextPage': False}, 'nodes': vals}
    }


def api_for(pages, url=None, state='OPEN'):
    counter = [0]
    def api(query, variables):
        if query == writer.PROJECT_QUERY:
            result = pages[counter[0] % len(pages)]
            counter[0] += 1
            return result
        if query == writer.TARGET_QUERY:
            return {'repository': {'isPrivate': False,
                                   'issue': {'id': 'I_1', 'url': url or op()['url'], 'state': state},
                                   'pullRequest': None}}
        raise AssertionError('Unexpected write in preflight')
    return api


class RequestTests(unittest.TestCase):
    def test_exact_digest(self):
        request = envelope()
        body, digest = payload(request)
        self.assertEqual(writer.parse_request(body, digest), request)
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            writer.parse_request(body, '0' * 64)

    def test_reject_body_prose(self):
        body, digest = payload(envelope())
        with self.assertRaisesRegex(ValueError, 'exactly one fenced'):
            writer.parse_request('Unauthorized preamble\n' + body, digest)

    def test_reject_duplicate_json_keys(self):
        data = '{"schema":1,"schema":1,"project":"dornglut/1","ensure_kind":false,"operations":[]}'
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            writer.parse_request('```json\n' + data + '\n```', '0' * 64)

    def test_reject_wrong_project_and_private_urls(self):
        for bad in ('https://github.com/other/repo/issues/1',
                    'https://github.com/dornglut/repo/discussions/1',
                    'https://github.com/dornglut/repo/issues/1?foo=bar'):
            body, digest = payload(envelope([op(url=bad)]))
            with self.assertRaisesRegex(ValueError, 'Invalid or duplicate'):
                writer.parse_request(body, digest)
        body, digest = payload(dict(envelope(), project='dornglut/2'))
        with self.assertRaisesRegex(ValueError, 'Unexpected project'):
            writer.parse_request(body, digest)

    def test_reject_dangerous_operations(self):
        for changes in [
            {'priority': 'root'},
            {'kind': 'Private'},
            {'status': 'Delete'},
            {'mutation': 'deleteProjectV2'},
            {'expected': {'present': True}},
        ]:
            body, digest = payload(envelope([op(**changes)]))
            with self.assertRaises(ValueError):
                writer.parse_request(body, digest)

    def test_reject_oversized_and_duplicate_targets(self):
        for ops in ([op(), op()], [op(url=f'https://github.com/dornglut/runenwerk/issues/{i}') for i in range(1, 23)]):
            body, digest = payload(envelope(ops))
            with self.assertRaises(ValueError):
                writer.parse_request(body, digest)

    def test_schema_bootstrap_is_separate(self):
        request = envelope(ensure_kind=True)
        body, digest = payload(request)
        self.assertEqual(writer.parse_request(body, digest), request)
        body, digest = payload(envelope([op()], ensure_kind=True))
        with self.assertRaisesRegex(ValueError, 'separate request'):
            writer.parse_request(body, digest)


class PlanTests(unittest.TestCase):
    def test_new_item_plan_is_read_only(self):
        request = envelope()
        planned = writer.plan_changes(api_for([project_page()]), request)
        self.assertFalse(planned['create_kind'])
        self.assertEqual(planned['changes'][0]['content_id'], 'I_1')
        self.assertIsNone(planned['changes'][0]['item_id'])

    def test_existing_item_exact_precondition(self):
        p = project_item(op()['url'])
        request = envelope([op(present=True)])
        planned = writer.plan_changes(api_for([project_page([p])]), request)
        self.assertEqual(planned['changes'][0]['before']['status'], 'Ready')
        request['operations'][0]['expected']['status'] = 'In progress'
        with self.assertRaisesRegex(ValueError, 'precondition'):
            writer.plan_changes(api_for([project_page([p])]), request)

    def test_target_must_be_open_for_blocked(self):
        with self.assertRaisesRegex(ValueError, 'contradicts'):
            writer.plan_changes(api_for([project_page()], state='CLOSED'), envelope())

    def test_project_must_be_public(self):
        with self.assertRaisesRegex(ValueError, 'not public'):
            writer.plan_changes(api_for([project_page(private=True)]), envelope())

    def test_schema_create_is_bounded(self):
        request = envelope(ensure_kind=True)
        plan = writer.plan_changes(api_for([project_page(kind=False)]), request)
        self.assertTrue(plan['create_kind'])
        self.assertEqual(plan['changes'], [])

    def test_missing_option_fail_closed(self):
        p = project_page()
        fields = p['organization']['projectV2']['fields']['nodes']
        fields[0]['options'] = [v for v in fields[0]['options'] if v['name'] != 'Blocked']
        with self.assertRaisesRegex(ValueError, 'Missing configured status'):
            writer.plan_changes(api_for([p]), envelope())

    def test_missing_kind_field_fail_closed(self):
        with self.assertRaisesRegex(ValueError, 'Missing configured kind'):
            writer.plan_changes(api_for([project_page(kind=False)]), envelope())

    def test_incomplete_pagination_fail_closed(self):
        with self.assertRaisesRegex(ValueError, 'item count mismatch'):
            writer.plan_changes(api_for([project_page(total=1)]), envelope())
        with self.assertRaisesRegex(ValueError, 'pagination'):
            writer.plan_changes(api_for([project_page(has_next=True, cursor=None, total=1)]), envelope())

    def test_extra_project_fields_unmodified(self):
        project = project_page()
        project['organization']['projectV2']['fields']['nodes'].append(field('Secret', ['private']))
        planned = writer.plan_changes(api_for([project]), envelope())
        self.assertEqual(set(planned['fields']), {'Status', 'Priority', 'Kind'})


class ApplyTests(unittest.TestCase):
    def test_write_only_through_execute(self):
        request = envelope()
        plan = writer.plan_changes(api_for([project_page()]), request)
        writes = []
        def api(query, variables):
            writes.append(query)
            if query == writer.ADD_ITEM:
                return {'addProjectV2ItemById': {'item': {'id': 'PVTI_1'}}}
            if query == writer.SET_FIELD:
                return {'updateProjectV2ItemFieldValue': {'projectV2Item': {'id': 'PVTI_1'}}}
            raise AssertionError('Unexpected mutation')
        writer.execute(api, request, plan, emit=lambda s: None)
        self.assertEqual(writes, [writer.ADD_ITEM, writer.SET_FIELD, writer.SET_FIELD, writer.SET_FIELD])

    def test_existing_field_null_clears_when_requested(self):
        p = project_item(op()['url'])
        request = envelope([op(present=True, priority=None, kind=None)])
        plan = writer.plan_changes(api_for([project_page([p])]), request)
        writes = []
        def api(query, vars):
            writes.append(query)
            if query == writer.SET_FIELD:
                return {'updateProjectV2ItemFieldValue': {'projectV2Item': {'id': 'PVTI_1'}}}
            if query == writer.CLEAR_FIELD:
                return {'clearProjectV2ItemFieldValue': {'projectV2Item': {'id': 'PVTI_1'}}}
            raise AssertionError('Unexpected mutation')
        writer.execute(api, request, plan, emit=lambda s: None)
        self.assertEqual(writes, [writer.SET_FIELD, writer.CLEAR_FIELD])

    def test_no_broad_project_mutations(self):
        for query in (writer.ADD_ITEM, writer.SET_FIELD, writer.CLEAR_FIELD, writer.CREATE_KIND):
            self.assertNotIn('deleteProjectV2', query)
            self.assertNotIn('updateProjectV2(', query)
            self.assertNotIn('archiveProjectV2Item', query)


if __name__ == '__main__':
    unittest.main()
