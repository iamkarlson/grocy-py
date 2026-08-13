# How to release

The version is **not** stored in `pyproject.toml`. It is `dynamic` and derived
from the git tag by `setuptools_scm`, so the tag is the single source of truth.
Tagging `1.0.0` produces `grocy_py-1.0.0`. If the tag is missing or malformed,
`fallback_version` silently yields `0.0.0.dev0` — always check the built
filename before publishing.

A PyPI version number can never be reused. Verify before you publish.

## Steps

1. Branch, and land everything that belongs in the release. Anything that
   changes the public surface must go in **before** the tag, not after.
2. Update `CHANGELOG.md`.
3. Check the public API against the previous tag. Any removal, rename or
   incompatible signature change means a major bump — see
   [Stability](README.md#stability).
4. Verify locally:
   ```bash
   task lint
   task test
   task docs
   uv run --isolated --python 3.12 --group dev pytest   # and 3.13, 3.14
   ```
5. Tag, then build and inspect:
   ```bash
   git tag <version>
   rm -rf dist build && uv build --no-sources
   ls dist/                      # filenames must show <version>, not 0.0.0.dev0
   tar tzf dist/*.tar.gz         # no cassettes, no .cache
   ```
6. Install both artifacts into a throwaway environment and smoke-test them.
   Run this from **outside** the repo — inside it, the source tree shadows the
   installed package and the test passes without testing anything:
   ```bash
   cd /tmp
   uv run --no-project --with /path/to/dist/grocy_py-<version>-py3-none-any.whl \
     python -c "import grocy; assert 'site-packages' in grocy.__file__; print(grocy.__file__)"
   ```
   Repeat for the `.tar.gz`.
7. Publish to TestPyPI first, install from there, and smoke-test again.
8. Push the tag. The `publish` workflow builds and uploads to PyPI when a
   GitHub release is published; `task publish` does the same locally and
   refuses to overwrite a version that already exists on PyPI.
