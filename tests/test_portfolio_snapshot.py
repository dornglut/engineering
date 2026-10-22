import hashlib
import importlib.util
import io
import json
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / 'tooling' / 'portfolio_snapshot.py'
SPEC = importlib.util.spec_from_file_location('portfolio_snapshot', MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def item(i, private=False, kind='ISSUE', **overrides):
    value = {
        'id': f'item-{i}', 'type': kind, 'isArchived': False,
        'updatedAt': '2026-10-22T06:00:00Z',
        'content': {
            '__typename': 'Issue' if kind == 'ISSUE' else 'PullRequest',
            'title': f'Issue {i}', 'url': f'https://github.com/dornglut/runen-ui/issues/{i}',
            'number': i, 'state': 'OPEN',
            'repository': {'nameWithOwner': 'dornglut/runen-ui', 'isPrivate': private},
        },
        'fieldValues': {
            'pageInfo': {'hasNextPage': False},
            'nodes': [
                {'__typename': 'ProjectV2ItemFieldSingleSelectValue',
                 'field': {'name': 'Status'}, 'name': 'Ready'},
                {'__typename': 'ProjectV2ItemFieldSingleSelectValue',
                 'field': {'name': 'Priority'}, 'name': 'P1'},
                {'__typename': 'ProjectV2ItemFieldTextValue',
                 'field': {'name': 'Secret notes'}, 'text': 'never leak'},
            ],
        },
    }
    if kind == 'PULL_REQUEST':
        value['content']['isDraft'] = True
    value.update(overrides)
    return value


def page(nodes, has_next=False, cursor=None, total=None, public=True,
         views_next=False, fields_next=False):
    return {'organization': {'projectV2': {
        'id': 'PVT_1', 'title': 'Engineering Portfolio', 'url': 'https://github.com/orgs/dornglut/projects/1',
        'number': 1, 'public': public, 'updatedAt': '2026-10-22T06:00:00Z',
        'views': {'pageInfo': {'hasNextPage': views_next}, 'nodes': [
            {'number': 3, 'name': 'Planning', 'layout': 'TABLE_LAYOUT'}]},
        'fields': {'pageInfo': {'hasNextPage': fields_next}, 'nodes': [
            {'name': 'Status'}, {'name': 'Priority'}, {'name': 'Kind'},
            {'name': 'Sensitive notes'}]},
        'items': {
            'totalCount': len(nodes) if total is None else total,
            'pageInfo': {'hasNextPage': has_next, 'endCursor': cursor},
            'nodes': nodes,
        },
    }}}


class SnapshotTests(unittest.TestCase):
    def observe(self, pages):
        calls = []
        def api(query, variables):
            self.assertIn('projectV2(number: $number)', query)
            self.assertEqual(variables['org'], 'dornglut')
            self.assertEqual(variables['number'], 1)
            calls.append(variables['cursor'])
            return pages[len(calls) - 1]
        result = module.observe(api, 'dornglut', 1, '2026-10-22T07:00:00Z')
        return result, calls

    def test_public_items_and_whitelisted_fields(self):
        snapshot, calls = self.observe([page([item(7), item(4, private=True), item(8, kind='PULL_REQUEST'),
                                               item(9, kind='DRAFT_ISSUE', content=None)])])
        self.assertEqual(calls, [None])
        self.assertEqual(snapshot['meta']['total_project_items'], 4)
        self.assertEqual(snapshot['meta']['exported_public_issue_pr_count'], 2)
        self.assertEqual(snapshot['meta']['excluded_draft_private_redacted_count'], 2)
        self.assertEqual(snapshot['meta']['exported_project_fields'], ['Kind', 'Priority', 'Status'])
        self.assertEqual([v['number'] for v in snapshot['items']], [7, 8])
        self.assertEqual(snapshot['items'][0]['fields'], {'Status': 'Ready', 'Priority': 'P1'})
        self.assertNotIn('never leak', str(snapshot))
        self.assertTrue(snapshot['items'][1]['draft_pr'])
        output = io.StringIO()
        module.emit_log(snapshot, output)
        lines = output.getvalue().splitlines()
        self.assertEqual(len(lines), 1 + 1 + 2 + 1)
        self.assertTrue(lines[0].startswith('DORNGLUT_PORTFOLIO_START='))
        self.assertTrue(lines[-1].startswith('DORNGLUT_PORTFOLIO_END='))
        expected_digest = hashlib.sha256(json.dumps(snapshot, sort_keys=True, separators=(',', ':'),
                                                   ensure_ascii=True).encode()).hexdigest()
        self.assertIn(expected_digest, lines[-1])

    def test_paginate_completely(self):
        snap, calls = self.observe([
            page([item(1)], has_next=True, cursor='c1', total=2),
            page([item(2)], has_next=False, total=2),
        ])
        self.assertEqual(calls, [None, 'c1'])
        self.assertEqual(len(snap['items']), 2)

    def test_private_project_never_exported(self):
        with self.assertRaisesRegex(ValueError, 'not public'):
            self.observe([page([item(1)], public=False)])

    def test_missing_pages_never_exported(self):
        with self.assertRaisesRegex(ValueError, 'total mismatch'):
            self.observe([page([item(1)], total=2)])

    def test_duplicate_page_item_detected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.observe([
                page([item(1)], has_next=True, cursor='c1', total=2),
                page([item(1)], total=2),
            ])

    def test_stuck_cursor_detected(self):
        with self.assertRaisesRegex(ValueError, 'not advancing'):
            self.observe([page([item(1)], has_next=True, cursor=None, total=2)])

    def test_no_partial_field_values(self):
        v = item(1)
        v['fieldValues']['pageInfo']['hasNextPage'] = True
        with self.assertRaisesRegex(ValueError, 'more than 100 fields'):
            self.observe([page([v])])

    def test_no_partial_field_or_view_definitions(self):
        with self.assertRaisesRegex(ValueError, 'views exceeds'):
            self.observe([page([item(1)], views_next=True)])
        with self.assertRaisesRegex(ValueError, 'fields exceeds'):
            self.observe([page([item(1)], fields_next=True)])

    def test_graphql_query_has_no_mutations_and_public_project_guard(self):
        self.assertNotIn('mutation', module.PROJECT_QUERY)
        self.assertIn('public updatedAt', module.PROJECT_QUERY)
        self.assertIn('isPrivate', module.PROJECT_QUERY)
        self.assertEqual(module.PAGE_SIZE, 50)


if __name__ == '__main__':
    unittest.main()
