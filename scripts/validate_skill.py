#!/usr/bin/env python3
"""Validate skill packaging; this is not a manuscript-quality evaluator."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'SKILL.md', 'README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md',
    'references/default-engineering-style.md',
    'references/deep-editing-workflow.md',
)
PRIVATE_MARKERS = (
    re.compile(r'(?<![A-Za-z])[A-Za-z]:[\\/]'),
    re.compile(r'/(?:Users|home)/[^\s/]+/'),
    re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}\b'),
    re.compile(r'\bgithub_pat_[A-Za-z0-9_]{20,}\b'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
)


def validate(root: Path) -> list[str]:
    errors = []
    root = root.resolve()
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f'missing required file: {name}')
    skill = root / 'SKILL.md'
    if skill.is_file():
        text = skill.read_text(encoding='utf-8')
        if not text.startswith('---\n'):
            errors.append('SKILL.md must start with YAML frontmatter without BOM')
        parts = text.split('---', 2)
        if len(parts) != 3 or not parts[2].strip():
            errors.append('missing frontmatter closing delimiter or skill body')
        else:
            front = parts[1]
            for key in ('name', 'description', 'version', 'author', 'license', 'platforms'):
                if not re.search(rf'^{key}:\s*\S', front, re.M):
                    errors.append(f'missing metadata: {key}')
            if not re.search(r'^name:\s*chinese-academic-humanizer\s*$', front, re.M):
                errors.append('unexpected skill name')
            version = re.search(r'^version:\s*(\S+)\s*$', front, re.M)
            if version and not re.fullmatch(r'\d+\.\d+\.\d+', version.group(1)):
                errors.append('version must be a three-component release version')
            description = re.search(r'^description:\s*(.+)$', front, re.M)
            if description and len(description.group(1).strip().strip('\"\'')) > 60:
                errors.append('description exceeds 60 characters')
    for path in sorted(root.rglob('*')):
        if not path.is_file() or any(x in ('.git', '__pycache__', '.venv') for x in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in ('.pdf', '.doc', '.docx', '.xlsx', '.pptx'):
            errors.append(f'private/binary manuscript artifact must not be published: {relative}')
        if path.suffix != '.md' and path.name != 'LICENSE':
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'not valid UTF-8: {relative}')
            continue
        for marker in PRIVATE_MARKERS:
            if marker.search(text):
                errors.append(f'possible local path or credential marker: {relative}')
        for target in set(re.findall(r'`(references/[\w./-]+\.md)`', text)):
            resolved = (root / target).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                errors.append(f'broken or escaping skill reference in {relative}: {target}')
        for label, target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text):
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target) or target.startswith('#'):
                continue
            destination = (path.parent / target.split('#', 1)[0]).resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f'broken relative link in {relative}: {label} -> {target}')
    return errors


if __name__ == '__main__':
    errors = validate(ROOT)
    print(json.dumps({'ok': not errors, 'errors': errors}, ensure_ascii=False, indent=2))
    sys.exit(1 if errors else 0)
