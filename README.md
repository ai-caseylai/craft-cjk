# craft-cjk

Chinese (Traditional, + the Hong Kong supplementary set) for the six ArtCraft editors, running as
plain WebAssembly on Cloudflare R2 behind a Worker:

| App | Version | Chinese UI | Characters covered | wasm |
|---|---|---|---|---|
| WordCraft | v0.7.0 | yes | full Traditional | 69.56 MB |
| GridCraft | v0.7.0 | yes | 44,810 (whole Noto Sans CJK TC) | 33.66 MB |
| DeckCraft | v0.7.0 | yes | 10,307 (Big5 L1 + HKSCS) | 29.18 MB |
| PhotoCraft | v0.9.0 | yes | full Traditional | 28.79 MB |
| VectorCraft | v0.9.0 | yes | 10,307 (Big5 L1 + HKSCS) | 49.30 MB |
| PdfCraft | v0.8.0 | yes | 10,307 (Big5 L1 + HKSCS) | 46.67 MB |

Every app was checked in a real browser: it loads, and its interface renders Chinese glyphs — not
tofu boxes.

## Why this is not one patch

Each app picks its interface font somewhere different, and three of them had a different blocker.
Confusing the *interface* font path with the *document* font path is the trap that costs the most
time, so start here.

### Two font paths, not one

Every one of these apps has both:

| | Interface (menus, panels, labels) | Document content |
|---|---|---|
| Source | compiled-in `CRAFT_FONTS` (`include_bytes!`) | fetched at runtime (`WEB_FONTS`, `fonts/manifest.txt`) |
| When | at startup, before the first frame | when a document or its text needs it |

The runtime path does **not** feed the interface. PhotoCraft proves it: the browser fetched the
CJK face successfully (HTTP 200, 15.67 MB, 3.8 s) and the interface still drew tofu, because
`served_fonts::install()` only registers into the *document* text engine
(`photocraft_text::shared()`) — every line of it walks `LayerContent::Text`. So for PhotoCraft and
PdfCraft the interface face has to be **embedded at build time**.

### Three recipes

**A. Embed, and open the wasm gate** — PhotoCraft, PdfCraft. Both deliberately embed no CJK face
on wasm, and both report **no locale at all** on wasm, so a shipped `zh-hant` translation could
never be selected. Three edits each: read `navigator.languages()`, let the CJK face through the
wasm filter, and route it to the interface.

**B. Use the app's own startup web font** — VectorCraft. Its `startup` list means exactly
"fallbacks the first frame needs", and it registers into `FontDb::global()`, the database the
interface shares. So it needs **no Rust change at all**: one line in `crates/text/web-fonts.txt`
plus the font served at its content-addressed URL.

**C. Watch the size** — GridCraft, DeckCraft. Embedding a large CJK face hangs startup. GridCraft
hung because the face was **copied onto the wasm heap**; `FontData::from_static` borrows the
`include_bytes!` blob instead and 44,810 characters load in ~10 s. DeckCraft never copied, and
still hung at 15.67 MB — a 4.88 MB subset loads fine.

## Layout

    patches/    per-app unified diffs against the release tag named in the file
    fonts/      the character list and the scripts that build the subsets
    tools/      the manifest-building scripts
    docs/       per-app notes and the full findings

## Applying a patch

    git clone --depth 1 --branch v0.9.0 https://github.com/storytold/photocraft
    cd photocraft
    git apply ../patches/photocraft-v0.9.0-cjk.patch

Then build. PhotoCraft is the only one with a custom cargo profile — use it, or the wasm is twice
the size:

    CRAFT_FONTS_DIR=<a craft-fonts checkout> cargo build \
      --profile wasm-release --target wasm32-unknown-unknown \
      --manifest-path apps/photocraft-web/Cargo.toml --bin photocraft-web --features heif

    wasm-bindgen --target web --out-dir dist/web --out-name photocraft-web --no-typescript \
      target/wasm32-unknown-unknown/wasm-release/photocraft-web.wasm
    wasm-opt -Oz --converge -o dist/web/photocraft-web_bg.wasm dist/web/photocraft-web_bg.wasm

Everything else is `cargo build --release` plus the same `wasm-bindgen` and `wasm-opt -Oz` steps.

## Fonts

The CJK faces are subsets of **Noto Sans CJK TC**, OFL-1.1. `fonts/` holds the character list and
the scripts; the source font is not vendored here — fetch it from
[notofonts/noto-cjk](https://github.com/notofonts/noto-cjk) and run:

    pyftsubset NotoSansCJKtc-Regular.otf --text-file=fonts/hk10k.txt \
      --output-file=NotoSansCJKtc-HK10k.otf \
      --layout-features='*' --no-hinting --desubroutinize --drop-tables+=DSIG

The list is Big5 level 1 (the standard 5,495 commonly-used characters) plus the 4,684 characters
that only Big5-HKSCS can decode — the genuine Hong Kong supplementary set, with Big5 level 2 left
out. 10,307 of the 10,318 requested characters exist in Noto Sans CJK TC.

Note that the subset is Traditional-only: Simplified-only characters (`简`, `报`, `价`, `单`, `项`,
`进`) are absent. `fonts/NotoSansCJKtc-Big5.otf` is a wider 7,260 KB variant.

## Attribution and licence

The patches are derived from MIT OR Apache-2.0 projects and stay under those licences; see
`LICENSE-MIT` and `LICENSE-APACHE`. The font subsets are OFL-1.1 — see `fonts/OFL.txt` and
`ATTRIBUTION.md`.

The Noto CJK faces are Adobe's Source Han under another name. DeckCraft's and PdfCraft's
`AGENTS.md` bar those families from their own builds. The project owner waived that bar for this
deployment so the browser interface could render Chinese at all; the patches that do so say so in
a comment where it happens. If you are not that owner, read your app's AGENTS.md before applying
them.