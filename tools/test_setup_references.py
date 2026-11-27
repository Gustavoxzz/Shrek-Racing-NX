import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import setup_references


class SetupTests(unittest.TestCase):
    def test_clone_repeat_and_preserve_changes(self):
        with tempfile.TemporaryDirectory(prefix="setup test ") as tmp:
            root = Path(tmp)
            source = root / "source with space"
            subprocess.run(["git", "init", "-q", str(source)], check=True)
            (source / "fixture.txt").write_text("fixture", encoding="utf-8")
            subprocess.run(["git", "-C", str(source), "add", "fixture.txt"], check=True)
            subprocess.run(["git", "-C", str(source), "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"], check=True)
            commit = setup_references.git("rev-parse", "HEAD", cwd=source)
            manifest = root / "deps.json"
            manifest.write_text(json.dumps({"schema_version": 1, "repositories": [{"name": "fixture", "url": str(source), "commit": commit}]}))
            dest = root / "dest with space"
            with contextlib.redirect_stdout(io.StringIO()):
                setup_references.setup(manifest, dest)
                setup_references.setup(manifest, dest)
            file = dest / "fixture" / "fixture.txt"
            file.write_text("local modification", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "local changes"):
                setup_references.setup(manifest, dest)
            self.assertEqual(file.read_text(encoding="utf-8"), "local modification")


if __name__ == "__main__":
    unittest.main()
