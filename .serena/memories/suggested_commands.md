# suave_rebetmc — suggested commands

## Docker build
```bash
# Standard build
docker build --secret id=gh_token,src=<(gh auth token) -t suave-rebetmc:dev src/suave_rebetmc/

# Force fresh dep clone
docker build --secret id=gh_token,src=<(gh auth token) --build-arg DEPS_CACHE_BUSTER=$(date +%s) -t suave-rebetmc:dev src/suave_rebetmc/

# Syntax check only
docker build --check src/suave_rebetmc/
```

## Exec pattern (all commands run via this)
```bash
docker exec suave_rebetmc bash -lc 'cd /home/ubuntu-user/suave_ws && source /opt/ros/humble/setup.bash && source install/setup.bash && <command>'
```

## Build
```bash
colcon build --symlink-install
colcon build --symlink-install --packages-select suave_rebetmc
colcon build --symlink-install --executor sequential --parallel-workers 1  # low-memory
```

## Test
```bash
colcon test --packages-select suave_rebetmc --event-handlers console_direct+
colcon test-result --verbose
python3 -m pytest -q suave_rebetmc/test

# Focused lint (mandatory before finishing)
colcon test --packages-select suave_rebetmc --event-handlers console_direct+ --pytest-args -k test_flake8
colcon test --packages-select suave_rebetmc --event-handlers console_direct+ --pytest-args -k test_pep257
```

## Validation shortcuts
```bash
python3 -m py_compile <launch_file.py>   # launch file syntax
bash -n <script>                          # shell script syntax
docker build --check src/suave_rebetmc/  # Dockerfile syntax
```
