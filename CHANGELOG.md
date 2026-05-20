# Changelog

## 0.2.0 — 2026-05-19

- Added `validate` subcommand (JSON-schema check)
- Resume support: re-running `annotate` skips tasks already in the output
- Summary now includes "elements with no issues" count

## 0.1.1 — 2026-05-14

- Fix: the evidence prompt looped forever if you typed exactly 5 characters.
  (off-by-one — `>= 5` should have been `> 4`.)

## 0.1.0 — 2026-05-10

- First working version: `annotate` + `summary` CLI commands
- JSON schema for annotation records
- 9 regions, 18 element types, 11 issue categories
