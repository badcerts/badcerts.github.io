## M01 Methods, units and bounded public reproduction

### Source hierarchy and event identity

The report uses the public research register and current question dispositions as its authoritative published summaries. Historical sources remain identified through the public source map, which distinguishes included derivatives from private originals and unavailable material. The frozen engineering result supplies the measurement history; later correction overlays update custody and interpretation without rewriting original evidence. A summary's presence in several files does not make it independently corroborated. [S-HISTORY](#S-HISTORY), [S-ENGINEERING](#S-ENGINEERING), [S-QUESTIONS](#S-QUESTIONS)

An artifact identity denotes particular bytes. A generation event denotes production of linguistic material. A measurement event applies an instrument to retained material. A review event interprets existing evidence. Conversion may create a new artifact without a new linguistic event; a model rewrite may create both. The public fixture wrappers have new identities while preserving the disclosed completion-ID arrays exactly. The recurrence and arithmetic checks operate on those arrays, without retokenization or a new generation. [R13](#R13), [R14](#R14), [R18](#R18), [S-RESULTS](#S-RESULTS)

The keyed aggregate computation occurred at 2026-10-07 23:26 UTC. The October 8 return/review and second-architecture observer are separate events. The public observer receipt describes peer-reported execution with supplied expected output; it is not device authentication. Historical provider statements are dated background from the preserved source review, not fresh efficacy measurements or proof of activation on earlier specimens. [A-01](#A-01), [R31](#R31), [R35](#R35), [L-09](#L-09)

[NATIVE-SPECIMENS]

### Exact eligible and distinct units

Let the retained completion be x₀,…,x₂₅₅ and context width w = 4. For an eligible target position i, define the context cᵢ = (xᵢ₋₄,…,xᵢ₋₁) and window vᵢ = (cᵢ,xᵢ). The first four completion positions are unscored. The public profile gives vocabulary size 151,936, gamma 0.25 and excluded target IDs 151643 and 151646. Neither excluded target occurs in these completions. These definitions describe exact integer tuples, not a seed or hash whose collision behavior might merge different contexts. [R18](#R18), [S-RESULTS](#S-RESULTS)

Define E as the eligible positions in original order. Raw selection uses all of E. First-context selection retains i only if no earlier eligible j has cⱼ = cᵢ. First-window selection retains i only if no earlier eligible j has vⱼ = vᵢ. Target exclusion precedes first-occurrence selection. An excluded token could still occur inside a later context under the historical contract; excluding a target is not deletion of that token from the sequence. The results are clean 252 positions / 249 contexts / 251 windows and marked 252 / 93 / 93. [R18](#R18), [F-08](#F-08), [S-RESULTS](#S-RESULTS)

The equality of marked context and window counts is a property of this trace, not a definition making the two units interchangeable. Clean contexts can recur with different targets. Likewise, a first window is distinct only under this exact tuple rule; it need not be probabilistically independent of another first window. Plotting recurrence by token position displays repeated representation, not elapsed time, membership or calibrated evidence strength. [R18](#R18), [R20](#R20)

### Hits, nominal scores and decision rules

For a selected unit set U and registered key K, let Iₖ(cᵢ,xᵢ) denote the construction's membership indicator. The keyed hit total is h = Σᵢ∈ᵁ Iₖ(cᵢ,xᵢ), and n = |U|. The public package discloses aggregate h and n, but not K or position-level native membership. Its arithmetic is z = (h − nγ) / √[nγ(1 − γ)], with γ = 0.25. Computing z from published aggregates checks their numerical relationship; it does not independently establish the hit indicators. [L-01](#L-01), [L-02](#L-02), [S-RESULTS](#S-RESULTS)

The denominator is nominal. No qualified empirical null, independence argument or population calibration accompanies these native results. The historical minimum of 100 scorable positions remains profile information. Applying that number to a different distinct-window rule would leave the marked 93-window trace below the minimum, but no such new rule is adopted here. The raw historical outputs and descriptive distinct-unit diagnostics remain separate. [R18](#R18), [R33](#R33), [F-08](#F-08), [F-09](#F-09)

The complete table retains two specimens × three key roles × three observation units = 18 rows. An alternate membership implementation checked the original keyed aggregates within the frozen engineering work. It shares the sample and construction, and its receipt is not a second native experiment. The public checker verifies every denominator and all 18 supplied-score calculations. This extends arithmetic coverage beyond the six raw checks in the historical field observer while remaining a keyless operation. [L-02](#L-02), [R31](#R31), [S-RESULTS](#S-RESULTS)

### Two mathematical controls and their limits

The synthetic dependence example uses a fixed fixture and 4,096 predetermined public keys. If a motif's hit fraction remains fixed while it is repeated r times, substituting h = rnq into the nominal formula gives z = √r · (nq − nγ) / √[nγ(1 − γ)]. This algebra explains why duplication can increase a raw score without new independent content. It is an explanatory identity under unchanged motif membership, not a fitted law for the native text or a new experiment. The retained fixture result is 1502/4096 raw crossings for the 64-repeat motif versus zero for 1,024 distinct windows. [R20](#R20), [L-04](#L-04)

For the toy identity-only control, let π be a bijection of token IDs. Consistent relabeling sets p′(π(t)) = p(t) and decoding d′(π(t)) = d(t). Summing probability over tokens decoding to any visible output therefore preserves the same probability mass after relabeling. All 24 permutations of the four-token vocabulary were tested in the preserved engineering work. The derivation states why that control is invariant; it does not prove invariance for an intervention that changes generation probabilities, segmentation behavior or the decoding relation. [R21](#R21), [L-05](#L-05), [R22](#R22)

For a future fixed binary rule evaluated on m independent held-out negatives, zero observed errors gives the one-sided exact 95% binomial upper bound 1 − 0.05^(1/m). At m = 30 this is approximately 0.0950. It is a conditional planning calculation; the 30/30 draft was not frozen or executed as a calibrated study in this report. Population definition, selection, independence and threshold freezing remain essential assumptions. [R33](#R33), [F-09](#F-09)

### Public check: prerequisites, operation and stopping

The reproduction guide and data dictionary accompany the artifact catalog in A08. The public supplement contains an output manifest, the exact public data and fixtures, coverage records and a standard-library output checker. From the public supplement's root, run:

```text
python3 -I -B scripts/verify_public_package.py
```

The original input-packet verifier checked the preserved design inputs during assembly. It remains a separate private staging check. The public command above checks the actual distributed payload and its output manifest, substantive record and anchor coverage, exact recurrence counts, the 18 supplied-score calculations and associated data consistency. Input verification and output verification are different operations; neither should be substituted for the other. The disclosed count/arithmetic route uses no model, secret key or network access. [S-RESULTS](#S-RESULTS), [S-QUESTIONS](#S-QUESTIONS), [S-OBSERVER](#S-OBSERVER)

Before interpreting a pass, inspect the reported unit counts and the explicit limits on membership measurement, new generation and historical-device authentication. The integer counts, tuple identities and payload identities are exact checks. A numerical arithmetic comparison does not independently establish the supplied membership counts or convert nominal scores into calibrated evidence. Output validation also does not replace visual review of the final PDF or authorize publication. [R18](#R18), [R31](#R31), [S-RESULTS](#S-RESULTS)

On an integrity, route or arithmetic mismatch, preserve the supplied artifact and the discrepancy. Do not change expected counts, substitute another key, normalize token arrays or regenerate evidence to obtain a pass. A corrected tool or public derivative needs a distinct identity and an explanation of the changed comparison. No secret-key work, model installation, field run or calibration campaign is needed for this public check. [R18](#R18), [R31](#R31), [R41](#R41)

### What the public files cannot reproduce

The public package cannot recompute native key membership because the secret keys and position-level labels are undistributed. It cannot regenerate the original native pair from complete model/runtime assets, authenticate the historical device event, or infer its execution merely from expected-output equality. It supplies public projections and aggregate receipts, not the complete private runtime. [S-RESULTS](#S-RESULTS), [S-OBSERVER](#S-OBSERVER), [L-01](#L-01), [L-09](#L-09)

It cannot rerun the historical 17-file carrier audit from original inputs, which remain unavailable in the reviewed material. Six summaries and audit documentation were recovered privately, but their public summaries are not an open raw-byte route. Comparative, parser, contract and historical field claims now have numerical/structural public projections. These support inspection and selected aggregate checks; the originals are not redistributed. The synthetic repetition, identity-only tokenizer and finite-sample calculations have complete public fixtures, focused source and expected output, so those bounded controls can be replayed. The artifact catalog distinguishes these routes individually. [S-EARLY-AUDITS](#S-EARLY-AUDITS), [S-COMPARATIVE](#S-COMPARATIVE), [S-CONTRACTS](#S-CONTRACTS), [S-ENGINEERING](#S-ENGINEERING)

Finally, the package cannot reconstruct the complete clean historical exporter, supply unmeasured utility, qualify accelerator use, validate radio semantics, produce a compiled current-policy certificate or calibrate generic authorship detection. These are declared unavailable, unmeasured, unqualified or excluded states, not broken public links to be guessed. The source map and current question dispositions identify the exact boundary and the condition under which a selected stronger claim could be reopened. [R26](#R26), [R28](#R28), [R29](#R29), [R32](#R32), [L-10](#L-10), [L-12](#L-12), [L-13](#L-13)

[FIGURE: F10]
