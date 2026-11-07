"""Validate the reviewed public export; standard library only, no network."""
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ".gitignore", "AGENTS.md", "README.md", "RIGHTS.md", "project.json",
    "docs/architecture.md", "docs/build-and-run.md", "docs/for-ai.md", "docs/updating.md",
    "assets/provenance.json", "status/current.json", "status/history.json",
    "status/repository-validation.json", "devlog/2026-11-06.md", "devlog/2026-11-07.md",
    "examples/godot-rules/project.godot", "examples/godot-rules/scripts/simulation.gd",
    "examples/godot-rules/tests/parity.gd", "examples/godot-rules/data/migration.json",
    "examples/godot-rules/data/parity-fixtures.json", "examples/godot-rules/source-manifest.json",
    "tools/validate.py",
)
PATTERNS = {
    "access_credential": r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})",
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "absolute_windows_path": r"\b[A-Za-z]:[\\/]",
    "home_directory": r"/(?:Users|home)/[A-Za-z0-9_.-]+/",
    "private_thread_id": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    "credential_assignment": r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[\"']?\s*[:=]\s*[\"'][^\"'\s]{8,}[\"']",
    "credential_url": r"https?://[^\s/]+:[^\s/@]+@",
}

def validate(root=ROOT):
    root = Path(root).resolve()
    present = set()
    for directory, dirs, files in os.walk(root):
        for name in dirs + files:
            path = Path(directory) / name
            if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                raise ValueError("Link/junction not allowed in public export")
        dirs[:] = [name for name in dirs if name not in (".git", ".godot", "__pycache__")]
        for name in files:
            path = Path(directory) / name
            present.add(path.relative_to(root).as_posix())
    expected = set(FILES)
    if present != expected:
        raise ValueError("Public file allowlist mismatch: " + str(sorted(present ^ expected)))
    hashes = {}
    total = 0
    for name in sorted(FILES):
        raw = (root / name).read_bytes()
        if len(raw) > 200_000:
            raise ValueError("Unexpected large file: " + name)
        content = raw.decode("utf-8-sig")
        for label, pattern in PATTERNS.items():
            if re.search(pattern, content):
                raise ValueError("Sensitive-content pattern " + label + " in " + name)
        if name.endswith(".json"):
            json.loads(content)
        hashes[name] = hashlib.sha256(raw).hexdigest()
        total += len(raw)

    def read(name):
        return json.loads((root / name).read_text(encoding="utf-8-sig"))

    project = read("project.json")
    for path in project["index"].values():
        if path not in expected:
            raise ValueError("Index references an unpublished file")
    if project["remote_apis"] or project["binary_downloads"]:
        raise ValueError("Remote services/downloads require a new review")
    commands = {item["id"]: item["argv"] for item in project["local_commands"]}
    if commands != {
        "validate": ["python", "tools/validate.py"],
        "rules-check": ["godot", "--headless", "--path", "examples/godot-rules", "--script", "res://tests/parity.gd"],
    }:
        raise ValueError("Unexpected command interface")
    example = "examples/godot-rules/"
    for record in read(example + "source-manifest.json")["files"]:
        if hashes.get(example + record["path"]) != record["sha256"]:
            raise ValueError("Example source hash mismatch")
    for entry in read("status/history.json")["entries"]:
        if entry["devlog"] not in expected:
            raise ValueError("History refers to unpublished devlog")
    for entry in read("assets/provenance.json")["assets"]:
        if entry["files_in_repository"]:
            raise ValueError("Binary asset publication needs a new rights review")
    receipt = read("status/repository-validation.json")
    if receipt.get("status") not in ("passed", "pending"):
        raise ValueError("Invalid validation state")
    tree = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    return {"passed": True, "files": len(hashes), "total_bytes": total, "tree_sha256": tree,
            "checks": ["allowlist", "text_size", "sensitive_patterns", "json", "index", "commands", "example_hashes", "history", "asset_exclusion"]}

if __name__ == "__main__":
    try:
        print(json.dumps(validate(), ensure_ascii=False))
    except (ValueError, KeyError, UnicodeError) as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False))
        raise SystemExit(1)
