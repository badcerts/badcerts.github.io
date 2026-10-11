# Reproducing the public calculations

Run these commands from the extracted package root with Python 3.10 or later. The checks use the standard library, read local files and do not need a model, account, native key or network connection.

```sh
python3 -I -B scripts/verify_public_package.py
python3 -I -B scripts/verify_supplement.py
python3 -I -B scripts/reproduce_controls.py
```

The first command checks the package inventory, original record bodies, links, retained completion arrays, exact recurrence and all 18 nominal score calculations. Its expected content fingerprints are fixed authoring inputs; they are not silently regenerated when a verification check fails. The inventory is an unsigned integrity record, not proof of authorship or historical execution.

The supplement check recomputes the seven field rows' descriptive means and ranges, the historical audit totals available from per-file rows, and the paired-corpus aggregates available from per-pair rows. It also checks exact specimen bytes, methods consistency and catalog routes. These calculations verify a projection's internal consistency. They do not recreate missing source files or authenticate a field device.

The final command repeats the frozen toy study: four integer fixtures, 4,096 predetermined public keys per fixture, all 24 four-symbol relabelings, a segmentation counterexample, and finite-sample planning calculations. It compares every result with the retained receipt. Exact integers and strings must match; floating results use absolute/relative tolerance 1e-12. Use `--full` to print every recomputed field. Typical execution takes tens of seconds on a desktop CPU.

## What each route establishes

| Route | Public inputs | Meaning of a match |
|---|---|---|
| Native recurrence | Two 256-ID arrays; width 4, target exclusions | Clean 252 positions / 249 contexts / 251 windows; marked 252 / 93 / 93. |
| Supplied-hit arithmetic | 18 hit/denominator rows, gamma 0.25 | The reported hits and denominators give the published nominal z values. Native membership is not recomputed. |
| Output inspection | Exact owned prompt and two output texts | Readers can inspect repetition and suitability directly and compare byte hashes. |
| Field summaries | Seven producer-reported rows | The descriptive summaries follow from the published rows. Null utility remains unmeasured. |
| Historical projections | Seventeen audit rows, six summary records, nine prose pairs and 32 continuations | Reported totals and selected aggregates can be checked. This is not an original-input rerun. |
| Repetition control | Explicit fixture arrays and frozen public-key derivation | Raw z ≥ 4 counts are 0, 116, 795 and 1,502 of 4,096 as repetition increases. These are toy crossings, not natural-text false-positive rates. |
| Relabeling control | Four symbols, weights 1/2/3/4, all bijections | Consistent identity-only relabeling preserves decoded probability mass. Coupled generation interventions remain open. |
| Planning arithmetic | Stated binomial/exchangeability/base-rate assumptions | Conditional numerical consequences, not an executed calibration study. |

The model and tokenizer identities, seed, sampling overrides and historical profile are in `data/native-methods.public.json`. No native replay script is supplied: the original runtime/model assets and native secret keys are not part of this package. A new native run would be a new experiment with its own identity.

The 17 original audit inputs remain unavailable. Six retained summaries and the comparative originals are held privately; this package publishes their measurement projections. The complete clean historical field exporter is also unavailable. Neither an expected-output match nor a clean present-day checkout fills that gap.

## Rebuilding the static reader and report

The site is static. Python is used only to author files locally. The browser loads HTML, CSS, a small theme preference script and the requested images/PDF; it does not execute the build sources.

Use a copy of the package for a rebuild, because it changes output identities. Install the versions in `sources/requirements.txt` in a dedicated environment. The report uses local Noto Sans and DejaVu Sans Mono fonts; font availability and renderer versions affect pagination. No remote assets are fetched by the PDF builder.

```sh
python3 -B sources/build_supplement.py
python3 -B sources/build_atlas.py
python3 -B sources/finalize_package.py
python3 -B sources/make_archive.py
python3 -I -B scripts/verify_public_package.py
python3 -I -B scripts/verify_supplement.py
```

`sources/build_figures.py` and the three format-card modules reproduce the ten analytical figures from the public source record. Rebuilding figures is optional when using the included exact SVG/PNG files. The membership subset retains the AxisPL license notice in `sources/controls/LICENSE.axispl.txt`; the extraction and import changes are documented in `sources/controls/README.md`.

Rebuilding does not carry forward visual review or collaborator acceptance. Inspect the changed pages and browser behavior before distributing a new edition. Verification errors should be recorded against the supplied bytes; do not change expected values merely to obtain a pass.

## Offline and hosted copies

Open `index.html` for the complete reader, `evidence.html` for the artifact catalog and `pdf.html` for the PDF view. The content and ordinary file links work without JavaScript. Theme persistence works over HTTP and may be limited by a browser's storage policy for local files. A native PDF viewer is optional; separate open/download and HTML links are always available.

The hosted distribution may place a complete archive in `downloads/complete-public-package.zip`. That archive contains the payload once, without a recursive copy of itself. `PUBLIC_MANIFEST.json` and `receipts/SHA256SUMS` inventory the payload; the separately generated archive checksum identifies the downloadable container. Archive bytes are not scientific evidence or a signature.
