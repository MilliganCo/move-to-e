# Changelog

## 2026-07-07 — repository audit and safety update

- Changed `move.py` to dry-run by default.
- Added explicit `--apply` flag for destructive filesystem changes.
- Added `--target-root`, `--folders` and `--yes` CLI options.
- Added destination safety check to prevent moving into `%USERPROFILE%`.
- Updated README with backup and symlink warnings.

## Initial version

- Moved a fixed list of user-profile folders to `E:\UsersData`.
- Created Windows directory symlinks through `mklink /D`.
