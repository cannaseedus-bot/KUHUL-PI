# Binary Ingest (MATRIX / ATOMIC-DOM)

This workflow converts text-like sources into a fixed-width binary stream
so runtime code can memory-map atoms without parsing.

## Pack a dataset

```bash
python tools/binary_pack.py datasets --out matrix_atoms.bin --atom-size 256
```

Defaults:

- `--atom-size 256`
- `--vocab-size 65536`
- `--extensions .txt .md .html .json`

## Read atoms at runtime

```python
from array import array
from pathlib import Path

ATOM_SIZE = 256

with Path("matrix_atoms.bin").open("rb") as handle:
    data = array("H")
    data.fromfile(handle, ATOM_SIZE * 4)  # example: read 4 atoms

atom_index = 2
start = atom_index * ATOM_SIZE
atom = data[start : start + ATOM_SIZE]
```

## Notes

- The tokenizer in `tools/binary_pack.py` is a placeholder. Swap in your
  π tokenizer / symbol map for production use.
- JSON files are normalized with compact separators to ensure deterministic
  tokenization.
- HTML stripping is intentionally minimal to keep the packer fast and
  easy to replace.
