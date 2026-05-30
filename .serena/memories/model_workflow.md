# suave_rebetmc — model workflow and src-gen rules

## DSL source models (hand-edited)
Located in `models/tactical_retreat/`, written in rebetmc_eclipse_projs Xtext DSLs:

| File | DSL | Extension |
|---|---|---|
| `suave.context` | ContextModel | `.context` |
| `suave.var` | FeatureModel | `.var` |
| `suave.resolution` | ResolutionModel | `.resolution` |
| `suave.tactics` | Tactics | `.tactics` |

DSL grammar and Eclipse plugins live at: https://github.com/kas-lab/rebetmc_eclipse_projs

## Generated outputs → src-gen/
- **`src-gen/suave_tactics.tql`** — TypeDB schema; loaded by `typedb_tactics` at runtime
- `src-gen/suave/` — generated ROS package (launch files, config) from the ROS model files

## Key invariants
- **Never hand-edit `src-gen/`** — regenerate via Eclipse (open models, run "Generate Artifacts" or MWE2 workflow)
- `models/typedb/suave_tactics.tql` is a **symlink** to `src-gen/suave_tactics.tql`; Docker dereferences it (copies content, not link)
- `models/interfaces/` (`.ros`), `models/ros/` (`.ros2`), `models/system/` (`.rossystem`) are inputs to `ros2model` — also not hand-edited

## Regeneration workflow
1. Open `models/tactical_retreat/` in Eclipse IDE with rebetmc plugins installed
2. Edit `.context`/`.var`/`.resolution`/`.tactics` as needed
3. Run "Generate Artifacts" → rewrites `src-gen/suave_tactics.tql`
4. Commit the updated `src-gen/` files
5. Rebuild the Docker image or run `colcon build` in the container

See `mem:tech_stack` for rebetmc_eclipse_projs build info.
