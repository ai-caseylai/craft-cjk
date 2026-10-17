# Attribution

## Fonts

Every CJK face here is a subset of **Noto Sans CJK TC**, and is redistributed under the
**SIL Open Font License 1.1** (`fonts/OFL.txt`).

| File | Based on | Licence | Changes |
|---|---|---|---|
| `fonts/NotoSansCJKtc-HK10k.otf` | Noto Sans CJK TC Regular | OFL-1.1 | subset to Big5 level 1 + the HKSCS-only characters |
| `fonts/NotoSansCJKtc-Big5.otf` | Noto Sans CJK TC Regular | OFL-1.1 | subset to the full Big5-HKSCS repertoire |

- Author: the Noto project (Google), originally Adobe's Source Han Sans.
- Source: https://github.com/notofonts/noto-cjk
- Subsetting is a permitted modification under OFL-1.1; the subsets are **not** the Reserved Font
  Name holders' originals, and no Reserved Font Name is claimed here.

`fonts/hk10k.txt` is a list of Unicode characters derived from the Big5 and Big5-HKSCS encodings as
implemented by CPython's `big5` and `big5hkscs` codecs. It contains no font data.

## Code

The patches in `patches/` are diffs against

| App | Tag | Project licence |
|---|---|---|
| WordCraft | v0.7.0 | MIT OR Apache-2.0 |
| GridCraft | v0.7.0 | MIT OR Apache-2.0 |
| DeckCraft | v0.7.0 | MIT OR Apache-2.0 |
| PhotoCraft | v0.9.0 | MIT OR Apache-2.0 |
| VectorCraft | v0.9.0 | MIT OR Apache-2.0 |
| PdfCraft | v0.8.0 | MIT OR Apache-2.0 |

They are derivative works of those projects and carry the same dual licence. No upstream source is
vendored here; clone it from `https://github.com/storytold/<app>` at the tag above.