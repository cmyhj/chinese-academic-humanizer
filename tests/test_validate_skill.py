from pathlib import Path
import importlib.util
import os
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('validate_skill', ROOT / 'scripts/validate_skill.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SkillPackageTests(unittest.TestCase):
    def fixture(self, root):
        for name in MODULE.REQUIRED:
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('# placeholder\n', encoding='utf-8')
        (root / 'SKILL.md').write_text(
            '---\nname: chinese-academic-humanizer\ndescription: Test editing.\n'
            'version: 0.3.0\nauthor: cmyhj\nlicense: MIT\n'
            'platforms: [windows, linux, macos]\n---\n# Skill\n', encoding='utf-8')

    def test_real_package(self):
        self.assertEqual(MODULE.validate(ROOT), [])

    def test_minimal_valid_fixture(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            root = Path(folder)
            self.fixture(root)
            self.assertEqual(MODULE.validate(root), [])

    def test_missing_reference_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            root = Path(folder)
            self.fixture(root)
            with (root / 'SKILL.md').open('a', encoding='utf-8') as out:
                out.write('Read `references/missing.md`.\n')
            self.assertTrue(any('broken or escaping' in e for e in MODULE.validate(root)))

    def test_local_path_is_rejected_but_https_is_allowed(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            root = Path(folder)
            self.fixture(root)
            (root / 'README.md').write_text('https://example.org/docs\n', encoding='utf-8')
            self.assertEqual(MODULE.validate(root), [])
            (root / 'README.md').write_text('C:/Users/private/draft.docx\n', encoding='utf-8')
            self.assertTrue(any('possible local path' in e for e in MODULE.validate(root)))

    def test_manuscript_binary_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            root = Path(folder)
            self.fixture(root)
            (root / 'draft.pdf').write_bytes(b'%PDF-')
            self.assertTrue(any('manuscript artifact' in e for e in MODULE.validate(root)))

    def test_link_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as folder:
            root = Path(folder)
            self.fixture(root)
            (root / 'README.md').write_text('[bad](../outside.md)\n', encoding='utf-8')
            self.assertTrue(any('broken relative link' in e for e in MODULE.validate(root)))


if __name__ == '__main__':
    unittest.main()
