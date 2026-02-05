#!/usr/bin/env python3
"""Binary packer for MATRIX / ATOMIC-DOM style ingest.

This script converts text-like sources into a fixed-width binary stream
of uint16 tokens. It is intentionally simple and deterministic so you can
swap in a real tokenizer later.
"""
from __future__ import annotations

import argparse
import json
from array import array
from pathlib import Path
from typing import Iterable, Iterator

DEFAULT_EXTENSIONS = (".txt", ".md", ".html", ".json")


def load_and_clean(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")

    if path.suffix.lower() == ".json":
        try:
            obj = json.loads(text)
            text = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        except json.JSONDecodeError:
            pass

    # Minimal HTML stripping placeholder.
    return text.replace("<", " ").replace(">", " ")


def pi_tokenize(text: str, vocab_size: int) -> Iterable[int]:
    """Placeholder deterministic tokenizer.

    Replace this with a π tokenizer / symbol mapper.
    """
    for char in text:
        yield ord(char) % vocab_size


def iter_source_paths(input_dir: Path, extensions: tuple[str, ...]) -> Iterator[Path]:
    for path in input_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


def pack_directory(
    input_dir: Path,
    out_file: Path,
    atom_size: int,
    vocab_size: int,
    extensions: tuple[str, ...],
) -> int:
    tokens: list[int] = []

    for path in iter_source_paths(input_dir, extensions):
        text = load_and_clean(path)
        tokens.extend(pi_tokenize(text, vocab_size))

    pad = (-len(tokens)) % atom_size
    if pad:
        tokens.extend([0] * pad)

    if vocab_size > 65536:
        raise ValueError("vocab_size exceeds uint16 range")

    packed = array("H", tokens)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("wb") as handle:
        packed.tofile(handle)

    return len(tokens)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pack text into binary atoms.")
    parser.add_argument("input_dir", type=Path, help="Directory to ingest")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("matrix_atoms.bin"),
        help="Output binary file",
    )
    parser.add_argument("--atom-size", type=int, default=256, help="Tokens per atom")
    parser.add_argument("--vocab-size", type=int, default=65536, help="Token vocab size")
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=list(DEFAULT_EXTENSIONS),
        help="File extensions to ingest",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    total = pack_directory(
        input_dir=args.input_dir,
        out_file=args.out,
        atom_size=args.atom_size,
        vocab_size=args.vocab_size,
        extensions=tuple(args.extensions),
    )
    atom_count = total // args.atom_size
    print(f"[OK] Packed {total} tokens")
    print(f"[OK] Atoms: {atom_count}")
    print(f"[OK] Output: {args.out}")


if __name__ == "__main__":
    main()
