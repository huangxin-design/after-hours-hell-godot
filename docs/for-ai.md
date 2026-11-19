# AI reading and local invocation

1. Read `project.json` for delivered reusable contents, Skill status, the index and real local commands.
2. Read `status/current.json` for the version, playable characters and acceptance limits.
3. Read `assets/provenance.json` before assuming that an asset is downloadable or reusable.
4. Inspect `examples/godot-rules/source-manifest.json` and its listed files for logic work.
5. Run `python tools/validate.py`; optionally run the documented Godot command.

Every command is local. There is no hosted game API, model-generation endpoint,
reward service, email-delivery service, MCP server or automatic asset download here.
Public versioned downloads are listed in project.json.

Use [ai-3d-game-qa](../skills/ai-3d-game-qa/SKILL.md) when diagnosing an asset,
animation, first-frame, encounter or packaged-build regression. Its linked case references
the project's recorded v011 evidence. The rules example and validator use project-specific
data and allowlists.

Full debugging stories and before/after comparisons belong on the project website.
Use the verified links in `project.json`; a null archive URL means the dedicated page
has not yet been verified. Keep only concise case context needed for technical reuse.

Use explicit evidence levels: `planned`, `asset_candidate`, `integrated`,
`automated_checked`, `captured_pixels`, `human_verified` and `print_verified` are
different claims. A `not_verified` value must remain unknown, not be converted to a pass.

The English terms 3D game development, Godot, Blender, Aholo/Lux3D,
character animation, rigging, game UI and AI-assisted game development describe
this project's actual workflow. They do not promise indexing by any AI provider.
