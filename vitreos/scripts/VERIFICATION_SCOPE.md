# Public verification scope

Run the three commands in `docs/REPRODUCE.md` from an extracted package. They locate inputs relative to their own files, use Python's standard library, read local files and print JSON. `-I -B` isolates Python from environment customizations and avoids bytecode cache writes.

## Package verifier

`verify_public_package.py` checks:

- Exact regular-file inventory, safe relative paths, no symlinks/special members, unique ledger entries, SHA-256 and byte lengths. All JSON is parsed with duplicate-field and nonfinite-number rejection.
- Preserved field fingerprints for 42 research records, 36 questions/probes, 64 historical gates, 14 claims, 26 contribution decisions, 20 format candidates and 11 source records. Reviewed October 11 amendments are limited to R39 specificity and current source/claim availability. The scientific claims, limits and other record fields remain conserved. Fixed expectations are readable in `expected-content.public.json`.
- Bidirectional research/question relationships and the separate R16/A-05 episode. Source routes remain separate from unsourced direct claim-to-gate relationships.
- Exact profile, two completion arrays, 512 recurrence entries, 18 result rows, full results-CSV equality, denominators and nominal-z arithmetic. One-pair scope, eligibility metadata and keyless observer limits remain explicit.
- Both complete HTML bodies: actual article/figure anchors, research fields in their own records, all question histories/current dispositions, gate bodies, claims/limits, source ceilings, contributions and format reasons. Shared claim status/reopening rules must match exactly and each claim must include a visible route to them. Script/style/hidden-element text cannot satisfy content checks.
- Relative HTML/CSS/SVG routes across the reader, print HTML, evidence catalog and PDF view. Deliberate external bibliography links are allowed; automatic external assets and active SVG content are rejected.
- All 223 original record/figure destinations plus the evidence supplement's rendered destination, bound to the exact current PDF hash and named candidate. Page/destination metadata comes from the renderer; independent PDF parsing and visual QA are separate local checks.
- Optional distribution sidecars when present: archive checksum, exact file inventory and byte-for-byte correspondence with the payload. The offline ZIP excludes itself and its separate archive checksum. Its hosted download link is intentionally optional in an extracted copy.

## Supplement verifier

`verify_supplement.py` checks exact prompt/completion byte hashes and selected method constants, all seven field rows' means/ranges/ratios and CSV values, null usefulness/log availability, reported 17-file audit totals including 35 ordinary trailing spaces, six-summary pair identities, derivable nine-prose/32-continuation aggregates and every artifact-catalog hash.

It does not rerun missing original byte audits, reconstruct the original corpora or calculate pooled n-gram intersections from absent raw text. Historical arithmetic agreement is not historical event authentication.

## Public control replay

`reproduce_controls.py` computes all four fixed fixtures over the same 4,096 predetermined public keys, all 24 relabelings, the segmentation example and finite-sample planning calculations. Every returned field is compared with the frozen receipt. Integers/strings match exactly; floating comparisons use 1e-12 absolute/relative tolerance. Native keys, model generation and field calibration are not involved.

## Practical limits

The manifests/checksums are unsigned byte inventories. Coordinated malicious edits to the payload, expected values and verifier are outside that integrity contract. Preserved source fingerprints are authoring inputs; changing an output manifest alone cannot make an altered conserved record pass.

The public scripts do not certify pixels, typography, reading order, formal accessibility, exhaustive security/confidentiality, original source authenticity, historical devices, native secret-key membership, model generation, calibrated inference or complete exporter provenance. Local PDF/browser checks were recorded separately against exact candidate bytes. A rebuild changes output identities and requires fresh review of changed output.
