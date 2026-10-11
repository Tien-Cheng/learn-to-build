"""The skill must stay portable: spec-only frontmatter, resolvable links, no orphans."""
import re

from conftest import REPO, SKILL

SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
LINK = re.compile(r"\]\(([^)\s]+)\)")
ASSET_PATH = re.compile(r"`(assets/[^`\s]+)`")


def frontmatter():
    text = (SKILL / "SKILL.md").read_text()
    assert text.startswith("---\n"), "SKILL.md must open with YAML frontmatter"
    block = text[4:text.index("\n---\n", 4)]
    fields = {}
    for line in block.splitlines():
        if line and not line[0].isspace():
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def markdown_files():
    return sorted(SKILL.rglob("*.md"))


def links(path):
    for target in LINK.findall(path.read_text()):
        if "://" in target or target.startswith("#") or target.startswith("mailto:"):
            continue
        yield target.split("#")[0]


def test_frontmatter_keys_are_spec_only():
    assert set(frontmatter()) <= SPEC_KEYS


def test_name_matches_directory():
    name = frontmatter()["name"]
    assert name == SKILL.name
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64


def test_description_and_compatibility_lengths():
    fields = frontmatter()
    assert 0 < len(fields["description"]) <= 1024
    assert len(fields.get("compatibility", "")) <= 500


def test_skill_md_under_500_lines():
    assert len((SKILL / "SKILL.md").read_text().splitlines()) < 500


def test_relative_links_resolve():
    broken = []
    for md in markdown_files():
        for target in links(md):
            if not (md.parent / target).exists():
                broken.append("%s -> %s" % (md.relative_to(SKILL), target))
    assert not broken, broken


def test_asset_paths_mentioned_exist():
    missing = []
    for md in markdown_files():
        for rel in ASSET_PATH.findall(md.read_text()):
            if not (SKILL / rel).exists():
                missing.append("%s mentions %s" % (md.relative_to(SKILL), rel))
    assert not missing, missing


def test_every_reference_is_reachable_from_skill_md():
    seen, queue = set(), [SKILL / "SKILL.md"]
    while queue:
        md = queue.pop()
        if md in seen:
            continue
        seen.add(md)
        for target in links(md):
            path = (md.parent / target).resolve()
            if path.suffix == ".md" and path.exists():
                queue.append(path)
    orphans = [p.name for p in (SKILL / "references").glob("*.md") if p.resolve() not in seen]
    assert not orphans, "unreachable references: %s" % orphans


def test_glossary_copy_matches_root():
    assert (SKILL / "references" / "glossary.md").read_text() == (REPO / "GLOSSARY.md").read_text()
