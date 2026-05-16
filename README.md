# DupFinder

A tiny Python command‑line utility that scans a directory and reports duplicate files using SHA‑256 hashes. It works recursively, handles permission errors gracefully, and prints concise groups of duplicates.

## Usage

```sh
python dupfind.py /path/to/dir
```

Optional flags:

- `-r`, `--recursive` – Scan sub‑directories (default).
- `-n`, `--non‑recursive` – Scan only the top level.
- `-v`, `--verbose` – Show progress logs.

## Output

Each line lists files that share the same content hash, separated by commas.

## License

MIT – see the repository.
