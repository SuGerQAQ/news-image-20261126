"""Copy the news-image entry to the sandbox output directory.

Reads entry.png sitting next to this script and writes it to
/output/entry.png, creating /output when it does not exist.
Standard library only; no network access.

The output must be a PNG of at most 1 MiB (1048576 bytes), matching the
competition gate. The copy is byte-for-byte, so repeated runs produce
identical output.
"""

import shutil
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.png"


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.png"
    data = source.read_bytes()

    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1

    if len(data) > MAX_BYTES:
        print(
            f"error: entry.png is {len(data)} bytes, over the 1 MiB limit",
            file=sys.stderr,
        )
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, OUTPUT_FILE)

    written = OUTPUT_FILE.read_bytes()
    if written != data:
        print("error: output bytes differ from entry.png", file=sys.stderr)
        return 1

    print(f"wrote {OUTPUT_FILE} ({len(written)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
