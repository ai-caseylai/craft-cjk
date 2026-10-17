# Per-app notes

Everything below was established by reading the app's own source, not by guessing, and each app was
then loaded in a real browser to confirm the interface renders Chinese.

## WordCraft v0.7.0 — 69.56 MB

`crates/fonts/build.rs` on wasm embeds one face (BIZ UDPGothic, Japanese). The patch swaps it for
the CJK face. Its `fontdb` catalogs lazily behind `OnceLock`, so a large face is fine here.

## GridCraft v0.7.0 — 33.66 MB

GridCraft has **no `crates/fonts` at all**. On wasm `try_load` returns `None` and `load_fallback`
returns an empty `Vec` — the browser build installs no fallback face whatsoever, by design. The
patch fills `load_fallback` in.

The trap: `FontData::from_owned(bytes.to_vec())` copies the whole face onto the wasm heap. It hung
at 13,804 characters and at 7,260 KB. `FontData::from_static(bytes)` borrows the `include_bytes!`
blob — `epaint::FontData::font` is a `Cow<'static, [u8]>`, so there is a zero-copy constructor —
and the full 15.67 MB face then loads in about ten seconds.

## DeckCraft v0.7.0 — 29.18 MB

Same architecture as WordCraft (`crates/fonts`, a `FontDb`, `CRAFT_FONTS`), so the same patch shape
works. DeckCraft's `build.rs` also carries an `EXCLUDED_FAMILIES` list naming Noto CJK; see the
policy note in the README.

Unlike GridCraft it never copies the bytes (`FontBytes::Static(&'static [u8])`), and it *still*
hung with the 15.67 MB face. A 4.88 MB subset loads. The exact mechanism is not established: the
`cataloged: OnceLock<()>` / `ensure_catalog()` design is the same in DeckCraft and in WordCraft,
which loads a larger face happily, so the lazy-catalog hypothesis is wrong. The practical answer is
the smaller face.

## PhotoCraft v0.9.0 — 28.79 MB

Three separate blockers, and the runtime font path is a decoy:

1. `crates/ui-egui/src/i18n/system.rs` returns an **empty** locale list for wasm, so `resolve()`
   falls back to `Lang::EN` and the shipped `zh-hant` catalogue can never be picked. Fixed by
   reading `navigator.languages()` (and adding the `Navigator` feature to `web-sys` in
   `crates/ui-egui`, which already depended on it).
2. `crates/text/build.rs` filters `CRAFT_FONTS_DIR` with `&& !wasm` — the web build embeds nothing.
3. `crates/ui-egui/src/cjk_fonts.rs` routes craft-fonts to the interface **only for Japanese**:
   `if script == CjkScript::Japanese { craft_fonts::japanese_for_ui() } else { Vec::new() }`. So
   Chinese had no interface source even when a face was embedded.

Build with the app's own profile. `--release` gives 48.16 MB; `--profile wasm-release` plus
`wasm-opt -Oz --converge` gives 23.90 MB. The profile (`lto = "fat"`, `opt-level = "z"`,
`strip = "debuginfo"`) is declared in the workspace `Cargo.toml` and referenced by
`data-cargo-profile` in `apps/photocraft-web/index.html`.

Do not try to fix the interface with the served-font mechanism. It is documented as "a host can
serve more fonts next to the app", and it does fetch them — the browser really did pull 15.67 MB in
3.8 s — but `served_fonts::install()` registers only into `photocraft_text::shared()`, the
**document** text engine; the whole function walks `LayerContent::Text`. The interface never sees
it. Also note its manifest's sha256 column must be **hex** (64 digits), not base64: `sri()` turns
hex into the `sha256-<base64>` integrity value, and a base64 value there makes the browser discard
the downloaded font.

## VectorCraft v0.9.0 — 49.30 MB — no Rust change

`apps/vectorcraft-web/src/web.rs` already reads `navigator.languages()` and calls
`i18n::set_system_locales`, and `crates/ui-egui/src/fonts.rs` documents its `startup` web fonts as
"fallbacks the first frame needs", registering them with `FontDb::global().add_font(...)` — the
database the interface shares. So one line in `crates/text/web-fonts.txt` is enough:

    startup | Noto Sans CJK TC | Regular

Two details that cost time:

- The craft-fonts manifest row must have **all eight** craft-fonts fields
  (`family | style | file | scripts | licence | licence file | sha256 | source`). With six,
  `build.rs` warns `malformed manifest row for ...` and emits an empty `WEB_FONTS`.
- The `file` field must use **forward** slashes. `web_fonts::url()` takes the basename with
  `file.rsplit('/').next()`, so a Windows path with backslashes becomes the whole URL path:
  `fonts/<sha16>/C:\...\NotoSansCJKtc-HK10k.otf`.

The served path is `fonts/<first 16 hex of the sha256>/<file name>`, so the file must be uploaded
there — that is what `cargo xtask web-fonts` does for a normal release.

## PdfCraft v0.8.0 — 46.67 MB

Three edits plus an owner decision:

1. `crates/ui-egui/src/i18n/mod.rs` returns `Lang::EN` for wasm unconditionally. Its `zh-hant.tsv`
   was already there. The patch reads `navigator.languages()`; `ui-egui` already had `web-sys`.
2. `crates/fonts/build.rs`'s `web_face` predicate keeps only BIZ UDPGothic, Arab, Telu, Hebr and
   Thai faces on wasm. The patch adds the Chinese scripts. The interface path
   (`theme.rs`'s `ui_chinese_fonts()`) already existed and simply had nothing to return.
3. The same file carries `BARRED_FAMILIES = ["Source Han", "Source Serif", "Source Sans",
   "Noto Sans CJK", "Noto Serif CJK"]`, which is checked **before** `web_face` and skipped the CJK
   face entirely. The patch adds a narrow owner waiver for `Noto Sans CJK TC` only — Simplified and
   the Adobe Source families stay barred.

PdfCraft has no `wasm-release` profile, so `--release` is correct; `wasm-opt -Oz` on top.

## Serving

All six are served from an R2 bucket by a Cloudflare Worker at `/editors/<app>/`, and each app's
wasm carries a content hash in its file name so an `immutable` cache cannot mask a deploy. The
largest wasm is 69.56 MB (WordCraft), which is fine from R2 — the 25 MiB per-file limit that
PhotoCraft's and PdfCraft's build scripts worry about applies to Workers Assets and Pages, not to
objects served out of R2. Build scripts fail above it on purpose; keep them and deploy from R2.