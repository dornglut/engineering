# Runen framework map

## Current repositories

| Repository | Role | Current relationship |
|---|---|---|
| `dornglut/runenwerk` | Integration platform and reference engine | Current integration authority |
| `dornglut/runen-ui` | Host-neutral UI framework | Standalone; adoption remains repository-owned |
| `dornglut/runen-sdf` | Signed-distance-field framework | Standalone; Runenwerk clean cutover remains active |

## Planned repositories

| Repository | Intended role | Dependency direction |
|---|---|---|
| `dornglut/runen-gpu` | GPU resource, execution, and device abstraction | Lower-level dependency |
| `dornglut/runen-render` | Rendering framework built on RunenGPU | Depends on RunenGPU |
| `dornglut/runen-ecs` | Standalone ECS framework | Extraction resumes after higher-priority boundaries stabilize |

A planned repository name does not authorize source movement. Each extraction requires a repository-local correction, standalone proof, consumer cutover, old-source retirement, and duplicate-authority audit.
