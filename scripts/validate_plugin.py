"""Validate the Apokalypsis plugin contract. Standard library only.

Checks:
  1. Both manifests parse as JSON and carry their required fields.
  2. plugin.json and marketplace.json agree on the name and the version.
  3. The license field reads Apache-2.0.
  4. Every skills/*/SKILL.md opens with frontmatter that has a name and a description.
  5. A CHANGELOG.md exists with an [Unreleased] section or a section for the current version.

Exit 0 when every check passes, 1 when any check fails (each failure named).
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []


def load(rel):
    path = ROOT / rel
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{rel}: file is missing")
    except json.JSONDecodeError as exc:
        errors.append(f"{rel}: not valid JSON ({exc})")
    return None


def require(obj, rel, keys):
    for key in keys:
        if not obj.get(key):
            errors.append(f"{rel}: required field '{key}' is missing or empty")


plugin = load(".claude-plugin/plugin.json")
market = load(".claude-plugin/marketplace.json")

if plugin:
    require(plugin, "plugin.json", ["name", "version", "description", "author", "license"])
    if plugin.get("license") != "Apache-2.0":
        errors.append("plugin.json: license must read Apache-2.0 (ruling APK-L1)")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(plugin.get("version", ""))):
        errors.append("plugin.json: version must be MAJOR.MINOR.PATCH")

if market:
    require(market, "marketplace.json", ["name", "owner", "plugins"])
    entries = [p for p in market.get("plugins", []) if plugin and p.get("name") == plugin.get("name")]
    if plugin and not entries:
        errors.append("marketplace.json: no plugin entry matches plugin.json's name")
    if plugin and market.get("metadata", {}).get("version") != plugin.get("version"):
        errors.append("marketplace.json: metadata.version differs from plugin.json's version")

for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    rel = skill.relative_to(ROOT).as_posix()
    if not match:
        errors.append(f"{rel}: no frontmatter block")
        continue
    for key in ("name", "description"):
        if not re.search(rf"^{key}:\s*\S", match.group(1), re.M):
            errors.append(f"{rel}: frontmatter has no '{key}'")

changelog = ROOT / "CHANGELOG.md"
if not changelog.exists():
    errors.append("CHANGELOG.md: file is missing")
elif plugin:
    text = changelog.read_text(encoding="utf-8")
    if "## [Unreleased]" not in text and f"## [{plugin.get('version')}]" not in text:
        errors.append("CHANGELOG.md: no [Unreleased] section and no section for the current version")

if errors:
    print(f"PLUGIN CHECK FAILED: {len(errors)} problem(s)")
    for err in errors:
        print("  x " + err)
    sys.exit(1)
print("Plugin check passed.")
