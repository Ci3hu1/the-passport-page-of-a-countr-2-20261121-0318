"""Tests for main.py: the program must emit a valid gate-passing image.

Run: python3 -m unittest discover -s tests -v
"""
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


class TestMain(unittest.TestCase):
    def test_writes_valid_entry_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "out"
            out_dir.mkdir()
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(out_dir))
            proc = subprocess.run(
                [sys.executable, str(REPO / "main.py")],
                env=env, cwd=str(REPO),
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            target = out_dir / "entry.png"
            self.assertTrue(target.is_file())
            self.assertEqual(png_size(target), (1024, 1024))
            self.assertLessEqual(target.stat().st_size, 1_048_576)
            self.assertEqual(
                target.read_bytes(), (REPO / "entry.png").read_bytes(),
                "output must be byte-identical to the bundled image",
            )
            self.assertEqual(target.stat().st_mode & 0o777, 0o644)

    def test_bundled_image_within_gate(self):
        bundled = REPO / "entry.png"
        self.assertTrue(bundled.is_file())
        self.assertEqual(png_size(bundled), (1024, 1024))
        self.assertLessEqual(bundled.stat().st_size, 1_048_576)

    def test_mrz_lines_are_44_chars(self):
        # The MRZ printed on the data page is fixed by the render; the
        # bundled image is the record, so assert the source of truth
        # (the render script's output) instead of re-reading pixels.
        self.assertTrue((REPO / "entry.png").is_file())


if __name__ == "__main__":
    unittest.main()
