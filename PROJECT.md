# Project: Insane Search E2E Testing, Bug Fixing, and README Parity

## Architecture
- **Insane Search Engine**: Located under `skills/insane-search/engine/`. A 4-stage search utility fallback system (Phase 0-3) executing API queries (oEmbed, RSS, JSON API), Jina Reader, identity spoofing, and Playwright browsers.
- **First-run setup**: Scripted in `setup/setup.sh` to configure stars and markers.
- **Verification Suites**: Python unit/smoke tests under `skills/insane-search/engine/tests/` and README verification via `tests/test_readme_remediation_verification.py`.
- **E2E testing**: Automated matrix tests in `tests/run_agy_cli_e2e_matrix.py` (21 platforms), logging to `tests/e2e/`.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| 1 | E2E Test Suite | Refine/Implement E2E test suite covering setup.sh interactive star prompts, all 21 platforms, and logging results to `tests/e2e/`. Deliver `TEST_INFRA.md` and `TEST_READY.md`. | None | DONE |
| 2 | Implementation & Debugging | Execute tests, fix engine bugs, and verify all E2E tests and unit tests pass. | M1 | DONE |
| 3 | README Cleanup & Parity | Retain only README.md & README.ko.md. Achieve 1:1 line/header parity and pass verification tests. | None | DONE |
| 4 | Future Proposals | Document recommendations in `docs/insane_search_future_proposals.md`. | M2 | DONE |
| 5 | Forensic Integrity Audit | Run forensic auditor to verify implementation integrity. | M2, M3, M4 | DONE |

## Interface Contracts & Layout
- Target E2E log location: `tests/e2e/`
- Target proposal document: `docs/insane_search_future_proposals.md`
- Target READMEs: `README.md`, `README.ko.md`
