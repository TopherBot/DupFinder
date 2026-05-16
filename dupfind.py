#!/usr/bin/env python3
"""DupFinder – simple duplicate file detector."""
import argparse, os, hashlib, sys

def hash_file(path, chunk_size=8192):
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError) as e:
        if args.verbose:
            print(f"[WARN] Cannot read {path}: {e}", file=sys.stderr)
        return None

def walk_paths(root, recursive):
    for entry in os.scandir(root):
        if entry.is_file(follow_symlinks=False):
            yield entry.path
        elif entry.is_dir(follow_symlinks=False) and recursive:
            yield from walk_paths(entry.path, recursive)

def main():
    parser = argparse.ArgumentParser(description="Detect duplicate files by content.")
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--recursive", action="store_true", default=True, help="Scan sub‑directories (default).")
    group.add_argument("-n", "--non-recursive", action="store_false", dest="recursive", help="Do not scan sub‑directories.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show warnings.")
    global args
    args = parser.parse_args()
    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"[ERROR] {root} is not a directory.", file=sys.stderr)
        sys.exit(1)
    hashes = {}
    for path in walk_paths(root, args.recursive):
        h = hash_file(path)
        if h:
            hashes.setdefault(h, []).append(path)
    duplicates = [files for files in hashes.values() if len(files) > 1]
    if not duplicates:
        print("No duplicates found.")
        return
    for group in duplicates:
        print(", ".join(group))

if __name__ == "__main__":
    main()
