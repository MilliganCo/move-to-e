# Public source preview — 2026-10-29

Windows folder relocation tool; current HEAD adds dry-run/--apply while initial history performs direct moves. No personal files committed.

The complete reachable history was reviewed for credentials, private data and asset provenance. No identified protected-data blocker remains for this source publication. This does not establish that every feature works or that the program is secure to deploy.

## Verification

Current Python source syntax: 1 files checked. Application UI, external APIs, drivers, ML training and real operational data were not exercised for this publication.

Use trusted local input copies and keep personal data, credentials, logs, model weights and generated outputs outside Git. No external scanner, printer password guessing, marketplace automation or model call was executed to publish this source.

## Additional reviewed runtime limits

[
  "Current dry-run protects default execution; earlier historical version mutates on launch.",
  "Current --folders accepts absolute/.. paths and target safety does not fully normalize nonexistent paths; no rollback if symlink creation fails."
]

## Before operational use

"Reject absolute/traversing --folders and normalize nonexistent target paths; add move/link rollback and failure-injection tests before recommending --apply."
