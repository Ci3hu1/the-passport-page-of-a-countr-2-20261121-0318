#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Entry program for make.fun competition
the-passport-page-of-a-countr-2-20261121-0318.

The spread is rendered at build time (Pillow is not available in the
grading sandbox) and bundled as entry.png: a 1024x1024 PNG of the open
passport of the invented Republic of Caelmar, held by Mara Iversen,
Warden of the Sands. This program is pure Python standard library: it
copies the bundled image to the output path the grader reads, trying
each location in turn and taking the first that succeeds.

Output: $MAKEFUN_OUTPUT_DIR/entry.png, then /output/entry.png, then
output.png in the working directory. Every output file is left world
readable (mode 0644) so the grader's collector can read it.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLED = HERE / "entry.png"

OUTPUT_NAME = "entry.png"
MAX_BYTES = 1_048_576


def candidate_paths():
    """Output locations, in the order the kit's proven pattern tries."""
    seen = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        seen.append(Path(env_dir) / OUTPUT_NAME)
    seen.append(Path("/output") / OUTPUT_NAME)
    seen.append(Path.cwd() / OUTPUT_NAME)
    return seen


def main():
    if not BUNDLED.is_file():
        print("bundled entry.png is missing from the repository", file=sys.stderr)
        return 1
    if BUNDLED.stat().st_size > MAX_BYTES:
        print("bundled entry.png is over the 1 MiB gate", file=sys.stderr)
        return 1

    last_error = None
    for target in candidate_paths():
        try:
            if target.resolve() == BUNDLED.resolve():
                # Output directory is the repository itself: the bundled
                # image is already the output; just make it readable.
                os.chmod(target, 0o644)
                print("entry.png already in place at %s" % target)
                return 0
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(BUNDLED, target)
            os.chmod(target, 0o644)
            if target.stat().st_size != BUNDLED.stat().st_size:
                raise OSError("short write: %s" % target)
            print("wrote %s (%d bytes)" % (target, target.stat().st_size))
            return 0
        except OSError as exc:  # read-only dir, missing /output, etc.
            last_error = exc
            continue

    print("could not write entry.png anywhere: %s" % last_error, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
