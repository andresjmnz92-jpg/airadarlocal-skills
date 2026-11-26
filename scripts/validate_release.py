"""Validate the current skills release and Claude Code marketplace without dependencies."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "en": ("90-day-plan", "content", "gaps", "google-profile", "questions", "technical-check"),
    "es": ("chequeo-tecnico", "contenido", "huecos", "perfil-google", "plan-90-dias", "preguntas"),
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    check(bool(version) and version.count(".") == 2, "VERSION must contain a semantic version")
    package_dir = ROOT / "packages" / version
    check(package_dir.is_dir(), f"Missing package directory: packages/{version}")

    expected_zips: set[str] = set()
    for lang, names in SKILLS.items():
        actual = {p.name for p in (ROOT / "skills" / lang).iterdir() if p.is_dir()}
        check(actual == set(names), f"Unexpected skill folders for {lang}: {actual ^ set(names)}")
        for name in names:
            skill = ROOT / "skills" / lang / name / "SKILL.md"
            body = skill.read_bytes()
            check(body.startswith(b"---\n") or body.startswith(b"---\r\n"), f"Missing YAML front matter: {skill}")
            text = body.decode("utf-8-sig")
            check(f"name: {name}" in text.split("---", 2)[1], f"Skill name mismatch: {skill}")
            check(len(text.strip()) > 100, f"Skill appears empty: {skill}")
            filename = f"{lang}-{name}.zip"
            expected_zips.add(filename)
            with zipfile.ZipFile(package_dir / filename) as package:
                entries = [item.filename for item in package.infolist()]
                check(sorted(entries) == sorted([f"{name}/", f"{name}/SKILL.md"]),
                      f"Unexpected ZIP contents: {filename}: {entries}")
                # Git checks out LF on Linux; published ZIPs were built on Windows with CRLF.
                packaged = package.read(f"{name}/SKILL.md")
                check(packaged.replace(b"\r\n", b"\n") == body.replace(b"\r\n", b"\n"),
                      f"ZIP differs from skill source: {filename}")
    actual_zips = {p.name for p in package_dir.glob("*.zip")}
    check(actual_zips == expected_zips, f"Missing or extra ZIP packages: {actual_zips ^ expected_zips}")

    manifest = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    check(manifest.get("name") == "airadarlocal-skills", "Marketplace name mismatch")
    plugins = manifest.get("plugins")
    check(isinstance(plugins, list) and len(plugins) == 2, "Marketplace needs exactly two language plugins")
    check({plugin.get("name") for plugin in plugins} == {"airadarlocal-en", "airadarlocal-es"},
          "Marketplace must have one plugin per language")
    for plugin in plugins:
        name = plugin.get("name", "")
        check(name in {"airadarlocal-en", "airadarlocal-es"}, f"Unknown marketplace plugin: {name}")
        lang = name.removeprefix("airadarlocal-")
        check(set(plugin.get("skills", [])) == {f"./{skill}" for skill in SKILLS[lang]}, f"Plugin skills mismatch: {name}")
        source = plugin.get("source", {})
        check(source.get("source") == "git-subdir" and source.get("path") == f"skills/{lang}", f"Plugin source mismatch: {name}")
        check(source.get("url") == "https://github.com/andresjmnz92-jpg/airadarlocal-skills.git",
              f"Plugin source must use public HTTPS Git: {name}")
        ref = source.get("ref")
        check(isinstance(ref, str) and ref.startswith("v"), f"Plugin ref missing: {name}")
        check((ROOT / "packages" / ref[1:]).is_dir(), f"Plugin points to unreleased package: {ref}")
        sha = subprocess.check_output(["git", "rev-parse", f"{ref}^{{commit}}"], cwd=ROOT, text=True).strip()
        check(source.get("sha") == sha, f"Plugin SHA does not match {ref}: {name}")
    print(f"Validated 12 skill folders, 12 ZIP packages for {version}, and 2 marketplace plugins.")


if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.CalledProcessError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
