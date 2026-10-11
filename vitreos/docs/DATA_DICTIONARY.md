# Data dictionary

JSON preserves nested history, explicit booleans and null values. CSV is provided only for flat numerical observations. The literal `null` in field CSV means unmeasured/unavailable, never zero. Empty cells in the comparative CSV mean a metric is inapplicable to that row family.

## Native experiment

`native-methods.public.json` records the original public model identity, weights hash, tokenizer fingerprint, runtime/version fields, actual sampling overrides and historical watermark settings. A hash identifies retained bytes or a declared artifact; it does not prove the generation event. The tokenizer fingerprint is the original v2 implementation's fingerprint, not a hash of this new JSON wrapper. Model output vocabulary size, tokenizer length and base vocabulary size are distinct quantities.

The prompt and clean/marked text files contain exact UTF-8 bytes, including the original text termination. Display wraps text without editing these downloads. `completion_tokens` counts generated IDs; the first four positions cannot form a full context and are unscored. `eos` is end-of-sequence; both retained traces reach the cap without it. This is a trace observation, not an independently recovered native finish-reason field.

`profile.public.json` supplies width, gamma, target exclusions and vocabulary size. The two completion JSON files preserve the original ID arrays in public wrappers. `observation-tracks.public.json` contains 512 token-position records: recurrence flags/indices, not elapsed time or native membership labels. `results.public.json/csv` has 18 rows: specimen × primary/two wrong-key roles × raw/first-context/first-window units. `hits` is a key-holder-supplied aggregate; `denominator` is the selected unit count; `nominal_z = (hits − denominator × gamma) / sqrt(denominator × gamma × (1 − gamma))`. It is not a calibrated confidence value.

## Historical field rows

| Field | Definition / unit |
|---|---|
| `id`, `group` | Neutral stable row ID; compact or broad context group. |
| `created_utc` | Producer-reported row timestamp; not independent clock authentication. |
| `prompt_tokens`, `generated_tokens` | Producer-reported counts; all rows generated 64 tokens. |
| `first_token_seconds` | Reported time to first token, seconds. |
| `post_first_tokens_per_second` | Reported post-first-token throughput, tokens/second. This rate has a different interval from whole-run wall time. |
| `peak_rss_kib` | Reported peak resident memory in KiB (1,024 bytes). Means average the per-row peaks. |
| `run_wall_seconds` | Whole-run wall time reported by the producer, seconds. |
| `load_seconds`, `generation_seconds` | Separately reported load/generation durations, seconds. The projection does not invent a precise timer-instrumentation definition absent from the retained report. |
| `thermal_start_millicelsius`, `thermal_end_millicelsius` | Producer readings by cluster sensor, thousandths of a degree Celsius. Sensor rows are not causal thermal controls. |
| `operator_usefulness` | Null for all seven observations: no usefulness score was recorded. |
| `dmesg_present` | Whether a log delta was captured: true for four compact rows, false for three broad rows. |
| `only_periodic_wifi_scan_observed` | True in captured compact deltas; null where no delta exists. |
| `added_warning_lines` | Producer-reported count in the captured log delta, null when unavailable; not a severity adjudication. |
| `accelerator_device_observations` | Generic device names and presence/type/access metadata. None of these flags proves inference used the device. |
| `accepted`, `authority`, `promotion_status` | Historical producer/import disposition, not a scientific promotion made by this publication. |
| `source_member_sha256` | Identity of the original report member from which the row was projected. |

`groups` contains count, arithmetic means and closed observed min/max ranges for six scalar metrics. These ranges are descriptive, not confidence intervals. `broad_over_compact_mean_ratios` divides those means; it does not estimate a causal effect. Seven rows are not seven independent native watermark generations. `field-contributions.public.json` separately records the implementation and observer chronology, with source document hashes and dated limits.

## Early negative audits and six summaries

`historical-audits.public.json` preserves the original report's 17 per-file measurements with neutral `AUDIT-01`…`AUDIT-17` labels. Bytes, Unicode characters and lines use the original audit definitions. Line-ending counts distinguish CRLF, bare LF and bare CR. Code-point lists include Unicode code point, category and occurrence count. Empty inspected carrier lists mean no observation in those classes; unavailable original files are a separate state. Reported SHA-256 values belong to original inputs, not these public row wrappers.

Six `SUMMARY-*` records retain body-word/unique-word counts, punctuation/Unicode/whitespace counts and reported byte identities. `condition_label` retains the descriptive collection label; High A/B does not authenticate the user responsible for a sample. `all_pairwise` contains all 15 unordered pairs; `focus_pairwise` is a six-pair subset, not six extra observations. Character and word sequence ratios describe sequence matching; unigram/bigram/trigram Jaccard compares distinct sets; word cosine describes bag-of-word overlap. These are descriptive measures, not watermark probabilities. `shared_ngram_counts` counts retained common phrase entries by length; the phrases themselves and personal conversations are not redistributed.

## Corpus and format comparisons

`comparative-observations.public.json` retains nine prose pairs and 32 constrained continuations. `word_count_delta_b_minus_a` is B minus A. `sequence_similarity` is the historical word-sequence ratio; `tfidf_cosine_1_2gram` is the reported 1/2-gram TF–IDF cosine. `longest_common_prefix_words` counts consecutive matching initial words; `longest_matching_block_words` may occur later. Shared n-gram counts and Jaccard values distinguish counts from ratios. Type/token ratio divides unique words by word count. Average word length and punctuation rate use the historical report's tokenization; exact raw-corpus recomputation is unavailable in this package.

For continuations, `stem_exact` states the provided prefix matched; `completion_exact` concerns the output alone. Exact first-one/two/four-word matches are different events. `aggregate` includes both sums/means of corresponding pairs and pooled n-gram measures. Only aggregates derivable from included rows are recomputed by the public checker; pooled intersections need the original corpora.

The arbitrary-key null uses 64 deterministic keys, gamma 0.25, context width 4 and a surrogate word-plus-punctuation vocabulary of 3,902. `population_sd` is the SD over those 64 scores; `ge4`/`ge6` are nominal threshold counts. No provider detector, key or calibrated null was available. The separate 4,096-key toy study is not this analysis.

Cross-format fields preserve structured-data validation, code/schema discrepancies and extractor findings. A raw `/AA` byte match is distinct from a parsed PDF action. Format conversions do not create new linguistic samples. Image-container flags report inspected metadata/carrier structures across five related images, not an exhaustive steganographic test. Export-method fields describe how those related artifacts were made.

## Controls and research records

`synthetic-controls.public.json` freezes four exact ID arrays and the public-key derivation. `synthetic-controls.expected.json` preserves the full original receipt. Histogram keys are multiplicities; values count distinct contexts/windows with that multiplicity. `sum_squared_window_weights`, `duplicate_only_design_effect` and `duplicate_only_weighted_n` are conditional duplicate-weight calculations. They do not establish independence. Score SD uses sample SD in the toy receipt; this differs from the historical 64-key null's population SD.

The research register preserves 42 substantive records, questions preserve 36 questions/subquestions/probes and their histories, and the gate register preserves 64 historical obligations. Claims, contributions, design choices and glossary remain structured JSON. Status words distinguish measured/observed, inspected absence, weak evidence, missing observation, unavailable source, unqualified claim and proposal. Unknown unknowns remain discovery probes, not asserted hidden mechanisms. `publication-changes.public.json` records intentional corrections; `artifact-catalog.public.json` maps public files to source families, availability and checks.
