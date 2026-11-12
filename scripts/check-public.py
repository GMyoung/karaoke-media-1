"""Validate the actual Pages artifact's boundaries and size; no playback tests.

Run with Python 3.10+ from any working directory. Reads public/ and emits a
compact JSON receipt; does not modify, upload or download files.
"""
from pathlib import Path
import json
import stat


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LIMIT_BYTES = 1_000_000_000
GIT_FILE_LIMIT_BYTES = 100 * 1024 * 1024
ROOT_FILES = {"index.html", "robots.txt", ".nojekyll"}
MEDIA_DIRECTORIES = {"media", "audio"}


def main():
    if PUBLIC.is_symlink() or not PUBLIC.is_dir():
        raise ValueError("public/ must be a real directory, not a symlink")
    missing = [name for name in sorted(ROOT_FILES) if not (PUBLIC / name).is_file()]
    if missing:
        raise ValueError(f"Missing public entry files: {', '.join(missing)}")
    total = 0
    counts = {"files": 0, "mediaFiles": 0, "audioFiles": 0}
    for item in sorted(PUBLIC.rglob("*")):
        relative = item.relative_to(PUBLIC)
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError(f"Symlinks are not allowed in public/: {relative}")
        if len(relative.parts) == 1 and relative.name not in ROOT_FILES | MEDIA_DIRECTORIES:
            raise ValueError(f"Unexpected top-level public path: {relative}")
        if any(part.startswith(".") for part in relative.parts) and relative.as_posix() != ".nojekyll":
            raise ValueError(f"Unexpected hidden public path: {relative}")
        if stat.S_ISDIR(info.st_mode):
            if relative.parts[0] not in MEDIA_DIRECTORIES:
                raise ValueError(f"Unexpected public directory: {relative}")
            continue
        if not stat.S_ISREG(info.st_mode):
            raise ValueError(f"Expected a regular public file: {relative}")
        if relative.parts[0] in MEDIA_DIRECTORIES and len(relative.parts) == 1:
            raise ValueError(f"Expected a directory: {relative}")
        if info.st_size >= GIT_FILE_LIMIT_BYTES:
            raise ValueError(f"File must stay below GitHub's 100 MiB limit: {relative}")
        total += info.st_size
        counts["files"] += 1
        if relative.parts[0] == "media":
            counts["mediaFiles"] += 1
        elif relative.parts[0] == "audio":
            counts["audioFiles"] += 1
    if total >= LIMIT_BYTES:
        raise ValueError(f"Public files total {total:,} bytes; keep below {LIMIT_BYTES:,} bytes")
    print(json.dumps({"publicDirectory": str(PUBLIC), **counts,
                      "bytes": total, "limitBytes": LIMIT_BYTES,
                      "scope": "Saved file boundaries and size only; no playback tests"}, indent=2))


if __name__ == "__main__":
    main()
