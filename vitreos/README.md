# Vitreos / AxisPL: AI Watermarking, Attribution and Provenance

11 October 2026 purpose-and-context public edition. Vitreos began with exploratory tests of Claude outputs in mid-August and developed into an investigation of AI watermarking, counter-watermarking, attribution and provenance. This evidence atlas connects that work to the problems facing educators, editors and source-evidence analysts, then supplies the measurements, informative absences, weak signals, corrected assumptions and questions that remain open.

Open `index.html` for the complete reader, `evidence.html` for evidence tables and downloads, or `pdf.html` for the embedded PDF with separate open/download links. The full report is `report/Vitreos_AxisPL_Evidence_Atlas.pdf`. Essential reading works without JavaScript; a 1 KB script retains the optional System/Light/Dark preference.

All 42 research records, 36 questions/probes with histories, 64 original gate obligations, 14 claims, 26 contribution dispositions, 20 format decisions and 11 source families remain available. The ten analytical figures retain their identities and graphical formats. SVG/PNG exports and editable generators are included.

The October 11 source restoration supplied scientific detail that the earlier public design packet had condensed: exact owned prompt/completion text, native model/tokenizer identities and settings, seven historical field rows with missingness, dated AgentHRIM/Corax contributions, early audit/comparison measurements and runnable frozen toy controls. This revision adds the missing purpose, selected dated external developments and explicit follow-up rationale to the opening. It changes no experimental results or retained scientific records. `data/publication-changes.public.json` records both revisions. Original personal dialogue, native secret keys and operational infrastructure are not distributed.

## Check and reproduce

From this directory, with Python 3.10 or later:

```sh
python3 -I -B scripts/verify_public_package.py
python3 -I -B scripts/verify_supplement.py
python3 -I -B scripts/reproduce_controls.py
```

These are read-only, standard-library calculations. The first checks inventory, conserved records, routes, recurrence and 18 supplied-hit score calculations. The second checks specimen bytes, historical arithmetic and catalog identities. The third repeats the four frozen public-key toy fixtures, all 24 relabelings and planning calculations. Native membership, historical device authentication and calibration are different claims and are not supplied by these checks.

Read `docs/REPRODUCE.md`, `docs/DATA_DICTIONARY.md` and `scripts/VERIFICATION_SCOPE.md` for definitions, commands and limits. `data/artifact-catalog.public.json` identifies included evidence files and what readers can check. Source-family summaries distinguish publicly available data from privately retained or genuinely unavailable originals.

## Package structure

- `manuscript/`: editable narrative, methods, dated bibliography and generated specimen/evidence chapters.
- `data/`, `fixtures/`: full structured records, exact disclosed specimens, historical projections and expected control outputs.
- `figures/`, `design/`: ten vector/raster plates, captions and preserved design decisions.
- `sources/`, `scripts/`: local builders, figure sources and bounded verifiers. Python is not needed to host or read the site.
- `coverage.json`: actual HTML/PDF destinations bound to the current PDF hash.
- `PUBLIC_MANIFEST.json`, `receipts/SHA256SUMS`: exact payload inventory and checksums.

The optional hosted `downloads/complete-public-package.zip` is a distribution sidecar. It contains this payload once, without another copy of itself. Its checksum is in `downloads/SHA256SUMS`; the public verifier checks its exact payload correspondence when present. When reading an extracted copy, you already have the complete package; the hosted archive-download link is not included recursively. Checksums identify bytes, not signed authenticity.

`REVIEW_STATUS.md` identifies this revision and its verification scope. This public edition is a static, inspectable research product. No additional native or Corax experiment is required to inspect this product.

For a rebuild, use a separate copy and the pinned authoring dependencies in `sources/requirements.txt`. Rebuilding changes identities and requires fresh review. Existing AxisPL code attribution/license is retained beside the extracted control source; this package does not invent a new license for all research materials.
