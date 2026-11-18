"""Validate the reviewed public export; standard library only, no network."""
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_PREVIEWS = {
    "docs/images/after-hours.webp": "db51425353e8c11e303f71d834c4073dcbc241b187ade91a69f031bd56574298",
    "docs/images/furnace-v011.webp": "e5683ba2ede7c43b733989056aa3127dbd709c395f7935c43acc31f953f5173c",
    "docs/images/guozai-print-study.webp": "ecaf06034b3228f072ac494fca76238070d2c0ac11544b9915c9f47aac6d0e21",
    "docs/images/milk-tea.webp": "afe67c998fcc233ae5e6ff790182d8d39c4d43b641d6cd39b719ee1fa55ba7f2",
    "docs/lux3d/images/printer-views.webp": "409a0033e8aa6cba2b1e6167a9fbc858de967ff58f0c0b79191660755e523e08",
    "docs/lux3d/images/input-front.webp": "91e5901a7e0911fada55b4b8fb4315686d0db326cbf1796400d84acf3d3ad932",
    "docs/lux3d/images/input-right.webp": "432e23139c69c8d824cbc9cdef62bc6596bd9bc995882850589661611061e4be",
    "docs/lux3d/images/input-back.webp": "e6a37d3ff39b7ad406884b23e42e6acd3097bb434cf861b064b1921e6f229382",
    "docs/lux3d/images/printer-source.webp": "49373b25aa3d74afda1491c3202faa43c334d92c0169cdae3a2b3ebfb0bd79e1",
    "docs/lux3d/images/printer-rear-source.webp": "93175c11a538c8f4fed87e552ad74b066e980592809d9a9e15552c649b56307d",
    "docs/lux3d/images/printer-rear-pass5.webp": "db0c6ba0606f74273402a95365dd2b5a4fa934479a0e4a864bdea44234054611",
    "docs/lux3d/images/printer-detail.webp": "d24f9ba4ba55d79a364e2f8f8f4cbca0c8b730263231b312f16558c97086ed30",
    "docs/lux3d/images/paper-packet.webp": "ae97aa83dd151f4b1e9c1bef839c8208449509f2e2bdf879acd39bfdeb20d562",
    "docs/lux3d/images/guozai-enter.webp": "7b94db8ad439141440a66f1de1950bcf3e80f521aa13e4f8f44a40cbc658f9f2",
    "docs/lux3d/images/guozai-hold.webp": "da743c905feda2779fddbfaad16491f4ef2f35f14c119c78d87911d33853ac69",
    "docs/lux3d/images/guozai-rebound.webp": "37df007bdb45e4f0451ee4e1d3ac41d17fd1bcf5158c26600265f628a542f3b7",
    "docs/lux3d/images/guozai-grip.webp": "da462c40598b837e5af570bac996398d8142cf63b351fc26696c31df55ffad4a",
    "docs/lux3d/images/yige-select.webp": "fa96b158af32534d85c9096ae8f0effa70a7eb89cd9f64675e84fd12ce4eb250",
    "docs/lux3d/images/yige-flat.webp": "697faa95e5f1ea53ac99c00f275f7a94dc7bdd272bac2dc642ba6f5e4e162d9c",
    "docs/lux3d/images/xiaomo-decoy.webp": "fcfbc6bcb869000a04d34d3ef52e711779541cf84afb45b1554d61cb6551b3f6",
}
RELEASE_BASE = 'https://github.com/huangxin-design/after-hours-hell-godot/releases/download/v011/'
REVIEWED_DOWNLOADS = {
    'AfterHoursHell-Windows-v011.zip': (852595689, 'bb1ab8cc17306e36b33157f5a66df81390e57d86a6477936b06630cadcba0f8f'),
    'AfterHoursHell-Models-v011.zip': (41869007, '1ba08fe77867069413d42285dd5e8ebc3ee312485c4e0ddb7ab91225c43cd4f5'),
}
FILES = (
    "docs/creator-notes.md", "devlog/2026-11-18.md", "status/godot-20261106.json",
    ".gitignore", "AGENTS.md", "README.md", "RIGHTS.md", "project.json",
    "docs/architecture.md", "docs/build-and-run.md", "docs/for-ai.md", "docs/updating.md",
    "docs/lux3d/deadline-printer.md", "docs/lux3d/characters.md",
    "docs/lux3d/printer-design-prompt.txt", *REVIEWED_PREVIEWS,
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
        hashes[name] = hashlib.sha256(raw).hexdigest()
        total += len(raw)
        if name in REVIEWED_PREVIEWS:
            if hashes[name] != REVIEWED_PREVIEWS[name]:
                raise ValueError("Review image hash mismatch: " + name)
            continue
        content = raw.decode("utf-8-sig")
        for label, pattern in PATTERNS.items():
            if re.search(pattern, content):
                raise ValueError("Sensitive-content pattern " + label + " in " + name)
        if name.endswith(".json"):
            json.loads(content)

    def read(name):
        return json.loads((root / name).read_text(encoding="utf-8-sig"))

    project = read("project.json")
    for path in project["index"].values():
        if path not in expected:
            raise ValueError("Index references an unpublished file")
    if project["remote_apis"]:
        raise ValueError("Remote services require a new review")
    downloads = [
        {"name": name, "url": RELEASE_BASE + name, "bytes": size, "sha256": checksum}
        for name, (size, checksum) in REVIEWED_DOWNLOADS.items()
    ]
    if project["binary_downloads"] != downloads:
        raise ValueError("Release attachment manifest differs from reviewed files")
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
            "checks": ["allowlist", "text_size", "sensitive_patterns", "json", "index", "commands", "example_hashes", "preview_hashes", "history", "asset_exclusion"]}

if __name__ == "__main__":
    try:
        print(json.dumps(validate(), ensure_ascii=False))
    except (ValueError, KeyError, UnicodeError) as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False))
        raise SystemExit(1)
