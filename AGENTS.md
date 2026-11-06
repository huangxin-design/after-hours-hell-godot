# Public repository instructions

This repository documents 地狱也得下班 (After Hours in Hell). Read `project.json`,
`status/current.json` and `assets/provenance.json` before making claims.

- Preserve the distinction between concept, Blender asset, engine integration,
  automated checks, captured pixels, human playtest and print validation.
- The full game is native Godot, keyboard-first and offline. The website is a diary.
- Guozai and Xiaomo are available in the documented Windows build; Yige is disabled.
  Use the current status file if a later reviewed update supersedes this snapshot.
- Do not invent APIs, downloads, service credentials, completed levels or performance.
- `examples/godot-rules` is a small rules snapshot. Its tests do not prove rendering,
  navigation, physical input, audio quality, macOS runtime or the complete game.
- Run `python tools/validate.py` for repository validation. The actual Godot command
  and tested version are in `project.json`. Prefer headless checks.
- Keep changes small. Never copy private conversations, credential files, local user
  paths, unreleased binaries or assets of unconfirmed redistribution status.
- New publication files require explicit review and an update to the file allowlist.
  Do not stage the parent workspace or use automatic all-files staging.
- Respect `RIGHTS.md`; visibility is not a blanket open-source asset license.

There is no network API or always-on agent in this repository. Reading JSON and
running the documented local scripts are the supported machine interfaces.
