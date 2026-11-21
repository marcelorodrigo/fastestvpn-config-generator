# AGENTS.md

Python 3.14 scripts that fetch WireGuard server entries from the same API the FastestVPN Android app uses and write one WireGuard `.conf` per server entry. There is no package/build setup (`pyproject.toml` is empty); run everything from the repo root.

## Environment

- Use the existing `venv/` (Python 3.14.10): `venv/bin/python ...`. The system `python3` here is 3.9.6, which does not match `.python-version` (3.14).
- Install dependencies with `venv/bin/pip install -r requirements.txt` (requests, pytest, pytest-cov).
- `generate_configs.py` requires `fastestvpn.conf` in the repo root. It is gitignored and may contain a real private key: never print, commit, or paste its contents. Only the template's `Endpoint =` line is rewritten; everything else is copied verbatim.
- No lint, formatter, or typecheck is configured. CI only runs tests; don't invent extra checks.

## Commands

- All tests: `venv/bin/python -m pytest -q`
- Single file/class/test: `venv/bin/python -m pytest tests/test_filename_utils.py::TestGenerateFilename -q`
- CI-equivalent (runs on every PR): `venv/bin/python -m pytest --cov=utils --cov-report=term-missing`
- List WireGuard entries from the app API: `venv/bin/python fetch_app_servers.py`
- Generate configs into `output/` (gitignored): `venv/bin/python generate_configs.py`

## How it works and gotchas

- `fetch_app_servers.py` GETs `https://api.fastestvpn.com/v2/servers` (unauthenticated JSON, same source the Android app reads at splash). It keeps only rows with `protocol == "WG"` and `enable == 1`. The live call is untested; parsing is tested offline against `tests/fixtures/servers_response.json`.
- WireGuard entries all report port **4443** (probes refuse 51820). `utils/config_utils.py` writes `Endpoint = <dns>:<port>` from the row, so the port must not be hardcoded.
- Filenames mirror the app listing: regular `Servers` rows are `country-label` (`Switzerland`/`Zurich 1` -> `switzerland-zurich-1.conf`), with a redundant country prefix stripped from the label (`Germany P2P 1` -> `germany-p2p-1.conf`). Streaming/P2P/D-VPN rows use their own label (`portugal-p2p.conf`, `france-via-uk.conf`). No label at all falls back to the hostname prefix.
- There is **no hostname deduplication**: distinct app entries that share a hostname each get their own file, even though the configs are identical (e.g. `portugal-lisbon.conf` and `portugal-p2p.conf`). Every row is written; two rows are the same app entry only when they share the API row id, so a row repeated across groups lands on the same file. Distinct entries that collide on a name get the hostname prefix appended, and the run fails loudly if that still collides.
- `generate_configs.py` asks before deleting files already in `output/`; declining aborts the run without generating.
- `utils/hostname_utils.py` provides the prefix/tail helpers; `utils/filename_utils.py` uses `extract_prefix` as its last-resort filename fallback. The number/dvpn extractors are unused by application code.
- Tests cover `utils/` and the API parser; `generate_configs.py` is untested.
