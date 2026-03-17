## v8

- Added `payment-link` command that prints only the raw payment URL on one line.
- Scan billing failures now include `"mode": "PAYMENT_URL_ONLY"` to signal raw-link handling in OpenClaw.
- Updated `SKILL.md` to require the raw-link command for insufficient-balance flows.

# Changelog

## 0.1.4
- Payment links are now returned and instructed to be shown as full plain-text URLs for easier copy/open on Ubuntu 20.04 and similar environments.

## 0.1.0 - 2026-03-13

Initial release bundle prepared for distribution.

### Added

- Clean release `README.md`
- `CHANGELOG.md`
- `LICENSE`

### Changed

- Packaged HunterMiner as a release-ready OpenClaw skill bundle

### Removed

- Cached Python bytecode directories (`__pycache__/`)
- Pre-generated output files and test reports from `output/`


## Unreleased

- Removed all fallback prompts that sent users to a website homepage when balance was insufficient.
- Kept only billing API payment links for the recharge flow.
- Enforced raw single-line payment URL output guidance for insufficient-balance flows.
## v7
- Fixed Python 3.10 compatibility by replacing `datetime.UTC` with `timezone.utc`.

