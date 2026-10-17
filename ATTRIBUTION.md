# Attribution

## Fonts

Every CJK face here is a **subset of LXGW WenKai (霞鶩文楷)** by LXGW, redistributed under the
**SIL Open Font License 1.1** (`fonts/OFL.txt`).

| File | Based on | Licence | Changes |
|---|---|---|---|
| `fonts/LXGWWenKaiTC-Big5L1.otf` | LXGW WenKai Regular | OFL-1.1 | subset to Big5 level 1 |
| `fonts/LXGWWenKaiTC-HK.otf` | LXGW WenKai Regular | OFL-1.1 | subset to Big5 level 1 + the HKSCS-only characters |

- Author: LXGW (https://github.com/lxgw/LxgwWenKai), v1.522. LXGW WenKai derives from Fontworks'
  Klee One; it is **not** an Adobe design.
- Source: https://github.com/lxgw/LxgwWenKai
- `fonts/OFL.txt` is LXGW's own licence file. It states an **additional permission** that the
  Reserved Font Names may be kept in "Modified Versions subsetted or converted to other formats
  (e.g., WOFF/WOFF2) solely for web font delivery"; that is exactly what these subsets are. The
  subsets are unmodified apart from the character set, keep no hinting, are desubroutinised and
  drop the `DSIG` table.

### Why LXGW WenKai and not Noto Sans CJK

Noto Sans CJK is Adobe's Source Han under another name. DeckCraft's and PdfCraft's `AGENTS.md`
§1.1 bar those families from their builds — "even when Adobe publishes the material under an open
licence, if it is visual design". An earlier revision of this work embedded Noto Sans CJK and
needed a per-app owner waiver; LXGW WenKai needs none, so the patches here do not weaken any
project's asset policy. It is also smaller: 2.87 MB against 4.88 MB for a comparable subset.

Coverage: **100% of Big5 level 1** (the 5,630 commonly-used characters) and 8,895 of the 10,316
characters in `fonts/hk10k.txt`. The 1,421 missing characters are all CJK Extension B
(U+20021–U+2F9D4), the rarest tail of Big5-HKSCS, which ordinary text does not use.

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