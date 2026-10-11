## S01 AI watermarking: the problem and the investigation

### Why this work matters

Vitreos investigates AI watermarking: how generated material might carry an identifiable signal, what happens to that signal as material moves between tools, and what evidence can support attribution. The work began in mid-August 2026 with exploratory tests of Claude outputs. A question about possible marks in those outputs grew into a broader investigation of detection, counter-watermarking and provenance. The practical problem is straightforward: when a text or file reaches us, what can we establish about how it was made and where it came from? [R02](#R02), [R03](#R03), [S-EARLY-DIALOGUE](#S-EARLY-DIALOGUE)

Educators need to assess permitted assistance, authorship and possible academic misconduct. Editors, researchers and evidence analysts need to assess documents whose bylines, apparent sources or histories may be misleading. Operators need records that survive movement between models, devices and formats. These decisions can fail in both directions: generated material can pass as independent human evidence, and human work can be wrongly accused. Even Turnitin's own [guidance for educators](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report) says its AI-writing results can misclassify text and require further scrutiny before adverse action against a student. That is a reason to improve the evidence and its interpretation.

Here, **watermarking** means deliberately creating a signal that a specified detector can test. **Detection** asks whether an observable feature or pattern is present. **Attribution** asks which source or process the evidence supports. **Provenance** concerns the documented origin and transformations of an artifact. A statistical text watermark, an AI-writing classifier and a signed content credential answer different parts of this problem. Recognizing AI involvement is useful, but it does not by itself establish who wrote something or whether its claims are true. [R12](#R12), [R17](#R17), [R24](#R24), [R25](#R25)

### What changed while the investigation was under way

The following developments give the investigation a concrete setting. Dates below identify publications or announcements; incident reports can describe activity that began earlier. These are selected external sources, separate from the Vitreos experiments.

| Publication date | Development | Why it matters to this work |
|---|---|---|
| 14 August 2026; updated 1 September | [Anthropic described Claude text watermarking](https://www.anthropic.com/news/claude-text-watermark) as a SynthID-Text variant using statistical choices in generated text. | A mark can reside in ordinary text choices. Looking only for hidden characters cannot test that whole possibility. |
| 10 September 2026 | [Anthropic's misuse report](https://www.anthropic.com/threat-intelligence-report-september-2026) described a Malaysia-focused operation that rewrote existing reporting, used fabricated bylines and removed original state-media attribution. The report covers disruptions from December 2025 through August 2026. | AI-assisted rewriting can obscure the source of material that still looks like ordinary reporting. The problem includes source history as well as generation. |
| 15 September 2026 | [MarkSec](https://arxiv.org/abs/2609.16681) proposed a capability-aware evaluation of watermark stealing, scrubbing and spoofing, with text-quality constraints. | A useful robustness result must say what an adversary could do and what quality survived. This study is background, not a method reproduced here. |
| 5 October 2026 | [OpenAI announced text provenance](https://openai.com/index/eu-text-provenance/), including a statistical watermark and restricted detector access. Its account distinguishes model involvement from authorship, identity and factual accuracy. | Availability, text conditions and detector access are part of any operational claim; a watermark is one source of evidence. |
| 8 October 2026 | [OpenAI reported two AI-assisted false-front operations](https://openai.com/index/disrupting-ai-enabled-false-front-operations/). One used seven fabricated journalist personas to pitch articles; the report identified almost 100 published or syndicated articles under their bylines. | Source presentation can conceal who is behind an article even when it appears in an established outlet. AI generation is only part of that attribution problem. |

The incident rows describe the providers' investigations. Vitreos did not authenticate those cases or test a detector on their artifacts. Their relevance is the decision they expose: a fluent passage and a plausible byline can leave essential source questions unanswered. The dated bibliography in [A05](#A05) gives the source routes and scope of this context review.

### Counter-watermarking is part of the research question

Claims to “remove AI watermarks,” “humanize” text or bypass detection need to be made testable. Changing an AI-writing classifier's score, erasing file metadata, weakening a keyed statistical signal and forging a signal are different outcomes. Success against one test says little about the others. The relevant questions are which mechanism was tested, what access the test assumed, what transformation occurred, whether useful content survived, and how the detector behaved on matched controls. The commercial tools mentioned in the exploratory discussions were not systematically evaluated here; this atlas supplies no blanket verdict on their efficacy. [F-10](#F-10), [F-15](#F-15)

Understanding those failure modes is necessary for evaluating a defense. A watermark that survives an untouched laboratory sample but fails under ordinary editing has a different practical role from one that withstands the transformations a user actually encounters. Equally, a test that can be made to implicate unmarked material needs that failure recorded. This is why absence, false alarms, acquisition loss and weak signals belong beside successful detections in the research record. [R01](#R01), [R15](#R15), [R18](#R18), [R36](#R36)

### How Vitreos and AxisPL approached it

The work combined local artifact analysis, AxisPL's owned watermark experiments, AgentHRIM's Corax field contributions, and browser lanes for research and analytics. It examined retained text and exported files, controlled token sequences and native completions, and records from constrained-device execution. [M01](#M01) supplies methods and specimens; [E03](#E03) and [E04](#E04) identify the field evidence and contributor chronology. This gives a future collaborator concrete material to inspect, reproduce or challenge.

The sequence matters. Early exploratory dialogue supplied hypotheses. Byte scans and text comparisons tested particular observations. Instrument controls exposed false alarms. A known-key laboratory made a narrower statistical question measurable. The contribution is both the resulting measurements and the record of how the question changed, including the tests that could not decide it. [S02](#S02), [S03](#S03), [S04](#S04), [S05](#S05)

### What this investigation supports

The most specific positive result is a registered-key excess in one retained marked completion after exact repeated context/target windows are removed. Earlier results include negative byte scans, weak text comparisons, instrument-generated false alarms, incomplete source custody and untested constructions. These belong to the same research story. The later success does not supply the missing premises of the earlier experiments. [R01](#R01), [R05](#R05), [R15](#R15), [R17](#R17), [R18](#R18)

The retained pair contains one clean and one marked completion, each with 256 completion-token IDs. With a four-token context, 252 positions are eligible in each. The primary-key raw counts are 53/252 for clean and 168/252 for marked. Counting only the first occurrence of each exact context-plus-target window gives 53/251 and 60/93. The corresponding nominal marked score falls from 15.2753 to 8.8007. Repetition increases the raw statistic, while a positive key-aligned excess remains in this specimen. Neither score is a calibrated probability of authorship or a population performance estimate. [R18](#R18), [L-01](#L-01), [L-03](#L-03), [S-RESULTS](#S-RESULTS)

The original investigation asked whether provider-generated files contained an observable signal and whether an owned instrument could expose it. Unknown activation, tokenizer, key, profile and acquisition conditions prevented a decisive answer about those historical specimens. Building a known-key laboratory changed the question to one that could be inspected: what does a declared local construction do to retained outputs, and which claims survive explicit controls? A successful local measurement answers that narrower question. It does not recover a provider's private mechanism. [R09](#R09), [R17](#R17), [F-01](#F-01), [F-04](#F-04)

[FIGURE: F06]

### Four evidence families and separate claim limits

Byte and export analysis examines properties of acquired artifacts: character classes, separators, containers and conversion effects. Registered statistical analysis examines compatibility with a specified construction, token representation and key. Credential analysis examines assertions carried by a signing or provenance system under an applicable validation and trust policy. Passive analysis examines style, similarity or interaction patterns without assuming an intentional mark. Each family has its own observation opportunities, confounders and controls. A negative in one family does not eliminate the others; a positive does not confer their capabilities. [R03](#R03), [R12](#R12), [R17](#R17), [R24](#R24), [F-13](#F-13)

The distinction also applies to attribution. A feature may be present in an artifact; a statistic may be compatible with a registered scheme; a receipt may associate an artifact with a workflow. Those statements do not automatically identify a person, establish ownership, reveal intent or certify factual truth. Conversely, failure to detect a signal does not establish human origin. The generic authorship or person-attribution claim is explicitly excluded from this milestone. [R25](#R25), [F-12](#F-12), [L-13](#L-13)

The project's request to retain evidence “below the noise floor” is interpreted with care. A measured noise floor requires a defined channel, statistic, background and sensitivity. No universal such quantity was estimated here. The phrase also expressed a broader concern about weak information missed through attention, retrieval or premature filtering. Preserving that concern does not turn absence into evidence of concealed marking. Nonexistence and limited observability remain distinct possibilities, without an assigned equal probability. [R01](#R01), [R36](#R36)

### Why follow up, and what would make it useful

As generation tools, editing workflows and detector access change, evidence collected under one set of conditions may stop answering the practical question. The useful continuation is to identify which change matters and test it with a declared protocol. The open questions in [S07](#S07) preserve several such routes:

- **Editing and counter-watermarking:** measure what happens under declared transformations and mixed-source workflows, retaining both signal and text-quality outcomes. [F-05](#F-05), [F-10](#F-10), [F-15](#F-15)
- **Reliable interpretation:** establish independent samples, false-positive behavior, relevant base rates and uncertainty before turning a score into an operational decision. [F-06](#F-06), [F-09](#F-09), [F-21](#F-21)
- **Unresolved mechanisms:** test the ordinary-separator and tokenizer/generation-coupling proposals against appropriate positive controls and nulls. Preserve their hypothesis status until that evidence exists. [F-02](#F-02), [F-03](#F-03), [A-02](#A-02)
- **Source evidence that travels:** examine whether credentials, acquisition records and field exports remain interpretable after transfer, and what each actually binds. [F-12](#F-12), [F-13](#F-13), [F-16](#F-16)

These are proposed continuations, not tests completed by publishing this atlas. A finished report can preserve uncertainty without making the next experiment compulsory. The purpose is to give researchers and operators an inspectable starting point for better attribution and provenance decisions, including cases where the available evidence remains inconclusive.

### Status and reading routes

Engineering closure, scientific qualification, product readiness and publication are separate decisions. The frozen engineering case study records a completed bounded continuation, including an accepted nonsecret observer return and an explicit unavailable exporter outcome. That closure does not establish native credential qualification, formal conformance, empirical detector calibration or a deployed service. An open research question can coexist with a finished report; an excluded stronger claim can be a correct final disposition. [R26](#R26), [R31](#R31), [R32](#R32), [R41](#R41), [L-10](#L-10), [L-12](#L-12)

Researchers can read S03–S06 for the observations, assumptions and alternatives, then follow the methods and complete records. Operators can start with S04 and the public reproduction procedure, which specifies what the disclosed files can verify. Collaborators can follow S02 and S07 to see corrected hypotheses and the smallest proposed discriminators. All routes reach the same evidence and limits. A role label changes navigation, not the strength of a result. [R17](#R17), [R33](#R33), [R38](#R38), [S-QUESTIONS](#S-QUESTIONS)

Transparency, consent, local custody, portable owned records and bounded operation on constrained devices motivated the work. They are design values, not measured proof of provenance efficacy or a conclusion about provider conduct. Adjacent memory, bias-evaluation and architecture ideas remain separate proposals. The public R39 and R40 records intentionally abstract personal and operational context while retaining the research questions and their limits. [R39](#R39), [R40](#R40), [F-23](#F-23)

## S02 Origins, correction and the quality of agreement

### A plausible mechanism is not an implementation disclosure

Early dialogue proposed token reweighting and elicited confident explanations of watermark method families. Later descriptions became more specific without acquiring corresponding implementation evidence. Familiarity with a public method can explain a technically plausible answer; agreeable dialogue and shared prompts can explain apparent confirmation. The record therefore retains the exchange as hypothesis formation. It does not treat a chatbot's account of itself as privileged disclosure or independent corroboration. Greenlist and Gumbel-family descriptions also remain distinct instead of being merged into a single alleged mechanism. [R02](#R02), [S-EARLY-DIALOGUE](#S-EARLY-DIALOGUE)

Provider background later changed the available knowledge. The source review preserved in the October freeze records an official family-level description identifying a SynthID-Text variant, with another provider's October 5 text-provenance announcement as separate background. The October 9 reconciliation preserved those dated sources and corrected contrary older summaries. The October 11 context revision checked those public pages again and links them in S01 and A05. That source check does not establish activation on an earlier file, disclose the exact private profile or make a local laboratory detector applicable to that file. [R35](#R35), [F-01](#F-01), [L-11](#L-11)

### What the ordinary-separator proposal actually said

The original whitespace lead included ordinary separators at selected offsets, potentially produced through token bias. Such a construction need not introduce unusual Unicode, extra trailing spaces or a conspicuous metadata object. Token choice and separator placement are not mutually exclusive mechanisms: changing word lengths or token choices could change where ordinary separators fall. The early anomalous-character scans therefore did not exhaust the proposal. This correction preserves an untested hypothesis; it does not demonstrate an encoded message. [R03](#R03), [F-02](#F-02), [S-INFORMAL-LEADS](#S-INFORMAL-LEADS)

A testable positional construction would need an explicit code or offset rule, a preservation model and an appropriate null. Offsets selected after viewing an artifact could fit ordinary language by accident. An owned positive control and matched unmarked text would distinguish a declared construction from retrospective pattern fitting. The proposal remains open on those terms, with broader prior art unassessed. The correct historical conclusion is that the scanned classes were absent in the tested copies; universal whitespace falsification was too strong. [R03](#R03), [R05](#R05), [F-03](#F-03)

The informal discussion also asserted inherited training-source marks, dedicated whitespace tokenizers and quotation limits caused by watermark leakage. These are three different causal or implementation claims, none established by the supplied receipts. Copyright policy, training behavior, active generation marking and ordinary style could exist independently. Retaining the assertions as historical leads prevents their disappearance, while marking them unverified prevents conversation confidence from becoming a finding. A quotation-length policy alone does not identify its cause or a provider's intent. [R04](#R04), [F-24](#F-24)

### How available knowledge was overlooked

Several losses concerned information already present in the record. An original conversation was initially treated as a derived artifact; the ordinary-offset proposal was flattened into an exotic-whitespace theory; exported copies were easy to count as new linguistic samples; a surface label obscured the absence of an exact successful model ID. Earlier requests to retain weak evidence also risked disappearing when the successful keyed result became the center of the narrative. These examples define “unknown knowns” operationally: recorded knowledge that was not loaded or integrated. They do not imply unconscious access to verified external facts. [R36](#R36), [R10](#R10), [R13](#R13)

Recovery changes custody without necessarily changing the observation. The six retained summaries and early audit material are now recovered; the 17 original audit inputs remain unavailable in the reviewed material. Earlier statements that all these files were missing are superseded. Their historical wording belongs in the correction history rather than the current account. A source-to-record crosswalk, hashes and explicit unavailable routes make this correction reviewable without requiring a new carrier experiment. [R05](#R05), [R06](#R06), [R36](#R36), [F-24](#F-24)

[FIGURE: F02]

### Agreement needs a dependency account

The operator repeatedly asked for conflict reporting and scrutiny of agreeable outputs. Multiple agents can share prompts, models, prior descriptions, fixtures and selection decisions. Separate role names do not make their conclusions statistically independent. A second implementation can detect an implementation discrepancy; a separate execution can test portability; an editorial review can find an overclaim. These are valuable contributions with different limits, and none automatically adds another generated specimen. [R38](#R38), [R18](#R18), [R31](#R31)

The appropriate human acceptance boundary is therefore evidence-based rather than a vote count. Agreement should travel with the shared inputs, actual operation and any disconfirming results. If reviewers repeat the same unsupported premise, their convergence does not strengthen that premise. If they inspect different failure modes in the same artifact, the resulting assurance is about those checks on that artifact. This distinction also informs the later passive-interaction hypothesis: apparent mirroring is a phenomenon to operationalize, not evidence of hidden communication. [R23](#R23), [R38](#R38), [A-03](#A-03), [U-03](#U-03)

Forecasts about access/cost stratification, resource constraints, information disorder and marking/guardrails receive similarly bounded treatment. The public record preserves the lesson of prospective logging while omitting personal circumstances. Timestamps, fixed endpoints, probabilities, scoring rules and a baseline are needed before assigning predictive credit. Selective recall and ordinary changes in conditions remain alternatives to a retrospective causal story. No prediction success or hidden intent is claimed. [R39](#R39)

## S03 Weak, absent and unavailable evidence

### The 17-file byte audit: a result with a precise object

The historical audit reports 17 Markdown files totaling 237,506 bytes, 234,326 Unicode characters and 2,644 lines. Its specified hidden, format and whitespace classes were absent. The retained account describes no zero-width or non-ASCII whitespace, format/bidirectional/variation/tag/private-use characters, tabs, byte-order marks or mixed line endings. Two trailing-space lines held 35 ordinary spaces, including diagram alignment. These are concrete reported observations about the inspected copies, not an undifferentiated statement that nothing unusual existed. [R05](#R05), [S-EARLY-AUDITS](#S-EARLY-AUDITS)

The audit report, JSON, script and manifest have been recovered. The 17 exact source Markdown files have not been recovered in the reviewed material. Consequently, this report can preserve and inspect the historical audit documentation but cannot present a fresh raw-byte rerun of all 17 inputs. The historical report's checks on uploaded-copy extended attributes also cannot establish the filesystem metadata of originals elsewhere. The missing input set is a custody limitation independent of the negative feature result. [R05](#R05), [F-02](#F-02), [F-24](#F-24)

The inference is conditional on what the method should have seen. A validated check for a specified character class can constrain that class in a preserved copy. It does not constrain a keyed distribution of ordinary words or separators, an external credential, a mark lost during acquisition, or every feature the parser did not inspect. No mark, a different carrier, acquisition normalization and an inaccessible statistical mechanism remain alternatives. Listing them does not assign them equal likelihood, and the negative result does not prove either human origin or concealed marking. [R01](#R01), [R03](#R03), [R05](#R05)

The smallest useful reopening depends on the stronger claim sought. Reproducing the historical audit would first require recovering the exact bytes of the 17 files against their manifest, then exercising named feature checks with positive controls. Testing ordinary-space positioning would instead require a declared positional construction and matched controls. These are different questions. Recovering a report alone accomplishes neither, but it improves the evidentiary route enough that the historical result need not be discarded. [R03](#R03), [R05](#R05), [F-02](#F-02)

### Six summaries, three pairs and a retained collection mistake

The summary collection consists of three long/short pairs from the same blog-summary sequence: one Max-effort pair and two High-effort pairs across two operators. An initial effort-setting mistake is part of the collection history. The shorter summaries followed longer requests, so the six files are not six independent draws under an identical fully frozen state. The anonymous High A/B labels do not establish which operator produced which pair. Preserving these conditions prevents a later reader from mistaking exploratory acquisition for a randomized comparison. [R06](#R06), [S-EARLY-AUDITS](#S-EARLY-AUDITS)

All six retained copies and their containing ZIP were recovered and hash-matched to the historical manifest. This is a substantial custody improvement over the earlier synthesis. It preserves the exact retained byte streams without authenticating their complete generation conditions, session state or historical marking activation. The numerical comparisons below remain historical reported metrics; their inclusion is not a claim that the authoring pass reran the carrier audit or original comparison pipeline. [R06](#R06), [F-24](#F-24)

| Historical High A/B comparison | Long summaries | Short summaries |
|---|---:|---:|
| Sequence similarity | 0.638 | 0.735 |
| Bag-of-words cosine | 0.912 | 0.869 |
| Longest exact common span | 13 words | 11 words |

These measurements show a combination of content overlap and wording variation under a shared source and task. High bag-of-words similarity can coexist with lower sequence similarity because related content need not appear in the same order. The values do not identify why the outputs differ. Common source material, constrained summarization, effort, style, stochastic generation and context differences remain plausible explanations. No calibration converts these metrics into a watermark test. [R06](#R06)

The scanned anomalous byte features were also absent in this collection. Separately, the Max summaries placed domain/date information in prose with a source line, while the High pairs used heading placement. That formatting difference deserves preservation because it is visible and could motivate a controlled experiment. The small uncontrolled collection cannot isolate effort as its cause, establish a stable effort fingerprint or identify a provider. A future matched comparison would need effort to be the sole changed factor and the formatting feature declared before inspection. [R06](#R06), [R07](#R07)

### Conditional divergence is weaker than family exclusion

The early reasoning treated divergent outputs as weak evidence against a vanilla fixed-key deterministic Gumbel-Max setup. That reasoning only discriminates when the complete determining state is fixed: prompt and hidden context, model, tokenizer, key, nonce and relevant generation state. Those premises were not established across the accounts. Divergence therefore cannot be assigned a quantified likelihood against a method family, and it does not identify a different provider mechanism. [R08](#R08), [F-04](#F-04)

This is a useful conditional argument rather than a failed observation. Under a fully specified owned deterministic implementation, repeated identical state should support a reproducibility test. When relevant state is unknown, distinct outputs leave several explanations alive: different hidden context, key scope, seed or nonce, sampling behavior and deployment variation. The proper continuation is to test a defined construction, not to elevate the conversational comparison into vendor forensics. [R08](#R08), [R17](#R17)

A related early overstatement held that a single Markdown file could never support detection. File count is not the decisive quantity. A sufficiently informative artifact under a validated known profile can support a profile-specific result. In these early files, short length, unknown activation, unavailable key/tokenizer/profile and unqualified sensitivity limited the inference. “Not marked,” “marked but undetected by this procedure,” and “altered by acquisition” are different states; none becomes established merely because there is one file. [R09](#R09), [F-06](#F-06)

### Matching-prompt corpora and the arbitrary-key null

A separate archived comparison covered nine prose pairs and 32 constrained completions. There were no exact pair matches. Mean prose sequence similarity was approximately 0.191 and TF-IDF cosine approximately 0.564; 20 of the 32 constrained pairs shared their first word and eight shared their first four words. Those observations belong to the historical comparative corpus, not the six-summary collection or the retained native pair. Shared prompts, common factual phrases and constrained answers provide direct alternatives to a watermark interpretation. [R10](#R10), [S-COMPARATIVE](#S-COMPARATIVE)

The exact successful command-line model identifier was missing. Matching archive hashes now bind the retained inputs to the historical analysis, but they do not supply every missing execution or scoring fact. The study supports a weak descriptive comparison with a named provenance gap. A stronger generalization would require generation-event and model receipts, followed by a separately selected comparison suited to that claim. Repetition of a surface label cannot repair a missing model identity. [R10](#R10), [F-20](#F-20)

The associated laboratory scan used surrogate word/punctuation tokenization and 64 deterministic arbitrary keys. Neither corpus crossed nominal z = 4, with mean z approximately 0.128 and 0.008. This is a profile-specific non-detection under the artificial laboratory construction. It is not a search of a provider's undisclosed key or a demonstration that provider marking was absent. Correct-profile positives and negatives are needed to establish detector applicability. The 64-key historical study must also remain separate from the later 4,096-key synthetic fixture. [R11](#R11), [F-03](#F-03), [F-09](#F-09)

### Container negatives and equivalent analytical care

Five image/export fixtures lacked the inspected embedded C2PA/JUMBF and related metadata structures; the reported visible structures matched ordinary SVG, PNG and JPEG tool paths. This describes those artifacts and acquisition routes under the stated parser coverage. A separate download route, external manifest or conversion that strips a credential remains a different possibility. The negative does not establish universal provider absence and does not qualify a native trusted-credential validator. [R12](#R12), [F-05](#F-05), [F-13](#F-13)

A route-specific continuation would retain pre- and post-export bytes and compare trusted, untrusted and other applicable controls. Merely citing a credential specification would not perform that qualification. Across these early studies, analytical care means retaining the observation, instrument, custody, assumptions, alternatives and claim limit together. The same structure applies to the later positive result: neither absence nor excess can outrun the method that produced it. [R01](#R01), [R12](#R12), [R18](#R18)

[FIGURE: F03]

## S04 Instruments, contracts and the unit of evidence

### Files are not generation events

Cross-format validation found that all five checked HTML source segments and all nine checked PDF segments preserved the source word sequence; both code segments preserved non-whitespace content. These conversions are useful transport controls. They do not add independent linguistic samples, because the model-generated content is inherited from the same source event. A PDF, HTML file and Markdown file can have different container bytes while carrying the same linguistic observation. [R13](#R13), [S-CONTRACTS](#S-CONTRACTS)

The unit can also be smaller than a file. A bundle may combine model prose, model code, programmatic data, deterministic conversions and a later rewrite. A condensed version produced by a model may be a new generation and potentially a new marking event. Treating that rewrite as a purely post-hoc transformation would confound editing with new generation. Span and event identities make the distinction explicit; local non-model edits are the appropriate starting point when the intended question concerns transformation alone. [R14](#R14), [F-10](#F-10)

### When the instrument creates the anomaly

The historical parser review found a raw `/AA` byte sequence inside compressed PDF data that had falsely suggested an Additional Actions structure. Parsed-object inspection did not support that interpretation. A byte substring and a parsed semantic object are different observations: an arbitrary occurrence in compressed data does not by itself establish the object named by the same characters. The failure belonged to the analysis path and must not be presented as hidden producer behavior. [R15](#R15), [S-CONTRACTS](#S-CONTRACTS)

Another extractor mapped ten ordinary bullet glyphs to U+007F. A second extractor and rendered pages showed bullets. Binary ZIP CR/LF counts were also misread as text line endings, and whole-bundle comparison obscured exact source segments within a larger document. These are productive weak-signal findings because they reveal how representation choice can manufacture an apparent anomaly. Their historical checks are retained; the report does not assert that current code still exhibits the same defects. [R15](#R15)

For a new suspicious feature, the corresponding discriminator is structural inspection, extractor comparison and rendered appearance under identified versions. These checks address different failure modes. Visual agreement cannot establish every byte property, while raw-byte agreement cannot validate a parser's semantic interpretation. The record supports preserving both the suspicious first result and the explanation that narrowed it, so future users can recognize the instrument failure without erasing the investigative path. [R15](#R15), [F-21](#F-21), [F-22](#F-22)

### Passing normal tests does not define the accepted language

In an earlier generated-fixture experiment, Go and Python programs agreed on 288 accepted records out of 300 and passed their reported normal tests. Yet they differed from the intended schema or each other on additional fields, whitespace, dates and oversized lines. Agreement over one fixture set did not establish equivalence across the full accepted input language. Different parser permissiveness and limits were sufficient explanations; no malicious behavior was required. [R16](#R16), [S-CONTRACTS](#S-CONTRACTS)

The later scalar-validation episode is separate. It concerned invalid scalar and token inputs at the watermark module's direct API, not the historical Go/Python fixture experiment. A bounded validation change was implemented and tested on the declared local branch. Broader public-ingress reachability and deployment remain outside scope. Linking A-05 to R16 preserves their shared methodological lesson without claiming the same incident occurred twice or inventing an exploitable public endpoint. [R16](#R16), [A-05](#A-05), [F-22](#F-22)

Historical importer work exposed raw-field, contradictory-promotion, boolean/type, infinity and count problems; subsequent repair added date, exception, concurrency, accounting and dirty-source checks. The accepted 0.1.4 closure remains the current historical disposition. Discovery text from an older transcript is not a present assignment to reopen every defect. A new regression or expanded contract would justify consulting current source and receipts, but stale pending wording cannot override a later accepted repair. [R30](#R30), [F-17](#F-17), [F-22](#F-22)

The frozen engineering ledger records 597 passing core tests with two expected skips, an amended browser replay with 101 top-level passes plus nine subtests, and wheel/sdist build with six smoke commands. Those are source- and scope-bound historical engineering checks. Optional Torch and native trusted-C2PA capability were not qualified by skipped cases, and the branch test packages did not replace the accepted release. The totals must not be combined into a scientific sample size or presented as fresh tests of this public manuscript. [L-06](#L-06), [L-07](#L-07), [L-08](#L-08)

### Formal assurance must bind the actual policy

The source record retains a discrepancy between the executable Python policy and archived Lean semantics. It supports one documented source-level finding; an intermediate seven-case claim lacked an inspected complete inventory. No current compiled certificate was produced for the actual policy. The stronger statement that the current Python policy is formally certified is therefore excluded. [R26](#R26), [F-14](#F-14), [L-12](#L-12)

A future proof obligation would need to bind the intended policy, executable version, complete case inventory and checked proof artifact. Formal tooling can establish a property of its formalized assumptions; it cannot by itself authenticate a historical device event or calibrate an empirical detector. Temporal, statistical, adversarial and operational assurance remain additional questions beyond a first policy kernel. Their presence in the research register preserves the frontier without implying implementation. [R26](#R26), [R42](#R42), [F-15](#F-15)

## S05 Bounded measured results and their dependence

### One pair, three observation units

The central native evidence is one retained clean/marked pair. The disclosed fixtures preserve 256 completion-token IDs per specimen. The original four-token context prefix is unscored, giving 252 eligible positions in each. Public wrappers retain the completion arrays and omit operational fields; they are new public artifacts with their own identities. They support exact recounting of tuple recurrence without requiring a tokenizer, model or secret key. [R18](#R18), [S-RESULTS](#S-RESULTS)

For a token at an eligible position, the context is its preceding four IDs and the window is that context together with the target ID. Raw scoring counts every eligible position. First-context selection keeps the first eligible occurrence of each exact context tuple. First-window selection keeps the first eligible occurrence of each exact context-plus-target tuple. The distinction matters when the same context is followed by different targets: the clean completion has 249 contexts but 251 windows; the marked completion has 93 of each. [R18](#R18), [F-08](#F-08)

The primary-key results illustrate how the unit changes the descriptive statistic. All values below are carried from the original-key local rescore; public verification can recount denominators and recompute arithmetic, but cannot remeasure key membership. [L-01](#L-01), [L-02](#L-02), [S-RESULTS](#S-RESULTS)

| Specimen | Selection unit | Hits | Denominator | Nominal z, not calibrated |
|---|---|---:|---:|---:|
| Clean | All eligible positions | 53 | 252 | −1.4548 |
| Clean | First exact context | 53 | 249 | −1.3538 |
| Clean | First exact context plus target | 53 | 251 | −1.4212 |
| Marked | All eligible positions | 168 | 252 | 15.2753 |
| Marked | First exact context | 60 | 93 | 8.8007 |
| Marked | First exact context plus target | 60 | 93 | 8.8007 |

Two wrong-key diagnostic roles are retained for every unit in the complete numerical table. Together, two specimens, three key roles and three units produce 18 analysis rows. They are repeated analyses of the same pair, not 18 generated samples, independent controls or trials of a population detector. The wrong-key results describe the selected diagnostic roles; they do not calibrate the distribution of every possible key or text. [R18](#R18), [L-02](#L-02), [S-RESULTS](#S-RESULTS)

[FIGURE: F04]

### From an aggregate bound to measured distinct membership

Before distinct membership was measured, the marked raw total and recurrence structure permitted between 39 and 75 distinct-window hits. That interval was a feasible bound, not a previously observed count or another specimen. The original key holder subsequently measured 60 hits among the 93 distinct windows. The computation occurred on October 7 at 23:26 UTC; the later return and review belong to October 8. The bound remains part of the knowledge history, while 60/93 is the current measured aggregate. [R18](#R18), [A-01](#A-01), [S-RESULTS](#S-RESULTS)

The key-holder rescore agrees with all six historical raw sample/key-role results. A separate scalar membership implementation agrees with the hit totals. That cross-check is valuable for detecting a mismatch between implementations of the declared construction. It shares the original sample, key material and construction assumptions, so it is not independent scientific replication. Public readers can verify the consistency of the published aggregates but cannot infer that multiple implementations create multiple samples. [L-02](#L-02), [R18](#R18)

The marked raw excess is partly repeated evidence. Once exact repeated windows are removed, the primary-key excess remains: 60 compared with the nominal gamma-weighted expectation of 93 × 0.25 = 23.25. This supports a bounded observation under the local construction. It does not establish independence among the remaining windows, isolate why the text repeats, identify a provider's private scheme or assign a probability to authorship. Deduplication changes the observation unit; it is not a general cure for dependence. [R18](#R18), [L-03](#L-03)

[FIGURE: F07]

### Nominal arithmetic and the historical minimum

The displayed statistic is z = (h − nγ) / √[nγ(1 − γ)], with γ = 0.25, hits h and denominator n. Recomputing this equation checks arithmetic conditional on the supplied counts. Its familiar denominator does not establish that the observed indicators are independent Bernoulli trials or that a normal-tail interpretation is valid for this profile. No qualified empirical null supports a population error rate or an authorship probability in this study. [R18](#R18), [R33](#R33), [F-09](#F-09)

The historical profile retains a minimum of 100 scorable positions. The original raw unit has 252; the marked distinct-window diagnostic has only 93. If a future rule reapplied a minimum of 100 to distinct windows, this specimen would be below that minimum. Such a rule has not been adopted or calibrated here. The report therefore preserves the historical rule and the later diagnostic without silently promoting the 93-window value into a new qualified verdict. [R18](#R18), [F-08](#F-08), [S-RESULTS](#S-RESULTS)

The two native outputs also reached their token cap and were unsuitable in different ways. The marked text repeats a paragraph; the clean text continues in a prompt-like form and does not fully fulfill the task. These adverse observations remain beside the score. One matched pair cannot separate watermark, formatting, decoding and model effects. Neither a claim of proven marking-induced damage nor a claim of no quality cost follows. [R19](#R19), [F-07](#F-07)

### A synthetic dependence counterexample

The fixed synthetic experiment compares 1,024 distinct windows with a 16-window motif repeated 64 times, using 4,096 predetermined public test keys. The raw z ≥ 4 crossing count is 0/4096 for the distinct fixture and 1502/4096 for the highly repetitive fixture. Repeatedly reusing a favorable motif can increase the raw statistic without creating corresponding new independent evidence. This is a controlled counterexample to an incautious interpretation of raw score growth. [R20](#R20), [L-04](#L-04)

The sampling ensemble is keys applied to a deliberately constructed fixture. It is not 4,096 human texts, provider outputs, users or deployment submissions. Reporting 1502/4096 as a field false-positive rate would substitute a different population and observation unit. The preserved engineering freeze reproduced the fixed-fixture analysis. This edition publishes the exact fixtures, public-key derivation, focused source and expected output; its bounded replay matches that receipt. The control remains separate from the native pair and population calibration. [R20](#R20), [L-04](#L-04), [S-ENGINEERING](#S-ENGINEERING)

### A bounded tokenizer null

All 24 permutations of a four-token toy vocabulary preserve visible-text distributions when token probabilities and decoding are relabeled consistently. The intervention changes internal names while preserving their probabilistic and decoding roles. The null is therefore informative: identity-only relabeling does not produce the proposed observable change in this toy construction. It does not test a tokenizer-derived state that changes generation choices. [R21](#R21), [L-05](#L-05)

The broader tokenizer/generation proposal survives as an untested construction, not as a confirmed effect. Hidden segmentation, ID relabeling and output-changing coupling remain separate questions. The existing invariant control supplies a useful baseline for an eventual owned positive construction, while novelty and detector performance would still require their own evidence. [R21](#R21), [R22](#R22), [F-03](#F-03), [A-02](#A-02)

### What the keyless observer added

A field contributor reported execution of the standard-library nonsecret observer on a second architecture. Its returned output exactly matched the reference supplied with the request: clean 251 and marked 93 distinct windows, together with six reported-score arithmetic checks. The observer reused the trace and algorithm, contained no model or secret key, and did not remeasure the 60 membership hits. Expected output was supplied in advance. The result is a bounded reported portability check, not independent event authentication or a new generated sample. [R31](#R31), [L-09](#L-09), [S-OBSERVER](#S-OBSERVER)

The associated external archive hash and 23 payload entries matched, while the original manifest's self-hash was incorrect. The unchanged original and a receiver-computed inventory preserve that exception. Byte binding establishes what was received; it does not authenticate source execution or repair unavailable exporter history. The scoped observer request is closed without a requirement for another field run. [L-14](#L-14), [R31](#R31), [R32](#R32)

[FIGURE: F05]

## S06 Conditional constructions, adverse observations and missing evidence

### Output suitability is a separate outcome

The native pair's suitability problem cannot be reduced to a high or low watermark score. The marked repetition is directly observed; the clean continuation also fails to provide a satisfactory answer. Shared cap-reaching behavior leaves truncation and task completion relevant to both conditions. A matched seed does not isolate causality when formatting, sampling, model behavior and marking may interact. Preserving both outputs prevents favorable signal strength from displacing the practical quality question. [R19](#R19), [F-07](#F-07)

The existing optional continuation changes one predeclared prompt-format factor, with all attempts retained and at most 12 generations. It is a development diagnostic, not a population quality study. A later contribution proposed a different small factorial option; the current question register does not silently replace the selected maximum-12 proposal with it. No new run is required to describe the current adverse result, and a future failure would remain a valid endpoint rather than a reason to keep generating until an attractive example appears. [R19](#R19), [A-04](#A-04), [F-20](#F-20)

### What would make a tokenizer construction observable

The broader proposal couples a key or algorithm to tokenizer behavior, boundaries or generation choices so that decoded outputs might carry a detectable distributional difference. Merely naming tokens differently has already failed to change the visible distribution in the toy control. A proposed positive construction must therefore specify the operation that actually changes output, the detector that is supposed to observe it, and what information that detector requires. Otherwise an internal representation difference could be mistaken for a recoverable public signal. [R21](#R21), [R22](#R22), [A-02](#A-02)

An owned constructive test would retain the identity-only negative control, a declared output-changing rule, correct- and wrong-key controls, decoding parity and quality measurements. It would also need an appropriate null before assigning detector error probabilities. A positive toy result might still be explained by ordinary keyed token selection or segmentation effects rather than a distinct new family. The idea is original within the recorded project; global novelty has not been assessed. Neither conversational agreement nor a successful small example can resolve that separate question. [R22](#R22), [F-03](#F-03)

### Passive interaction and code-style hypotheses

Apparent same-model mirroring motivated a passive interaction-fingerprint hypothesis. Shared learned patterns could influence conversational style or convergence, but shared prompts, context, incentives, task constraints, copying and selection can produce the same appearance. The conversation lacked blinding, context separation and controlled independence. It establishes neither hidden communication nor subconscious recognition, intent or an intentional watermark. [R23](#R23), [A-03](#A-03)

A proposed blind comparison crosses same/different-model conditions with shared/separate-context conditions and prespecified features. Such a study would ask whether an effect survives the controls, rather than treating agreement as the outcome that must be confirmed. It remains optional future work. The same confounds apply to review of this project itself: if several agents read the same trace and explanation, agreement may reflect common evidence or common error. A dependency account is necessary before attaching independent weight to convergence. [R23](#R23), [R38](#R38), [U-03](#U-03)

Passive code/style analysis is another possible inspection aid. Its suggested utility is to prioritize review, while an alleged association between generated style and defects is a separate hypothesis. Origin labels and defect labels would need independent evidence, matched tasks and a held-out population. Common templates, formatter conventions, programming habits and problem difficulty can mimic source associations. Style is not identity, and likely origin is not a quality score. [R24](#R24), [F-11](#F-11), [F-12](#F-12)

Even a future classifier with a useful association would require an application-specific account of false alarms, misses and abstention. Inspection utility is not established by classification accuracy alone; the cost of reviewing an ordinary template or overlooking a serious defect matters to the intended use. The present record supports the proposal and its controls, not a validated source classifier or a claim that generated code is inherently defective. [R24](#R24), [F-21](#F-21)

### False implication and transformations

The original dialogue considered forged marks, transplantation and false attribution as well as removal. No successful attack was demonstrated in the retained record. The question matters because a positive result could be associated with processing or a fragment without establishing authorship of the whole artifact. An owned robustness study would therefore need to examine signal creation and transfer, mixed-source localization and removal, while preserving the distinction between detection and the attribution claimed from it. [R25](#R25), [F-10](#F-10), [F-12](#F-12)

Whitespace changes, rewrapping, editing and mixed-source transformations remain unmeasured robustness questions here. Early sweeping statements that formatting always breaks a mark were unsupported. A model rewrite may generate and mark anew, whereas a deterministic local edit changes an existing output; a detector failure may reflect altered tokenization or profile mismatch. Those operations cannot be pooled into a universal removal conclusion. A finite transformation matrix would need parent-child identities, an unchanged control and a frozen applicable profile. [R14](#R14), [R34](#R34), [F-10](#F-10)

Selective disclosure and the legal treatment of a particular transformation are also separate from technical feasibility. The register retains a background-review state and an unresolved fact-specific question. This report makes no legal determination for an actor, artifact or jurisdiction. Further analysis would be tied to an actual proposed use, not inferred from the existence of a public method or owned-sample experiment. [R34](#R34), [A-06](#A-06)

The dated contribution chronology and full seven-row field table are in [A08](#A08), with exact downloadable data and units.

### Historical field resource observations

Earlier field work included direct and compact runtime activity beyond the later observer-only task. The retained historical rows support a descriptive compact/broad-context comparison: four compact rows and three broad rows, each reporting 64 generated tokens. These are small nonrandom batches with incomplete equivalence of run conditions and unavailable complete clean exporter provenance. Their usefulness is as a resource-budget observation and a hypothesis for future matched work. [R27](#R27), [R32](#R32), [S-FIELD-HISTORY](#S-FIELD-HISTORY)

| Historical reported field | Compact context, 4 rows | Broad context, 3 rows |
|---|---:|---:|
| Prompt tokens | 437 | 1,749 |
| Generated tokens per row | 64 | 64 |
| Mean time to first token | 12.452 s | 63.001 s |
| Mean throughput | 8.349 tokens/s | 3.871 tokens/s |
| Mean resident memory | 647,049 KiB | 1,482,581.33 KiB |
| Mean wall time | 49.847 s | 109.218 s |

The numerical differences motivate a context-budget question, but context size, scheduling, thermal conditions, configuration and other factors were not isolated. The table is not a clean causal performance benchmark, an assertion of current device speed or a claim of reproducible exporter-bound performance. Matching row bytes and previously recomputed arithmetic preserve the historical observation while leaving those stronger interpretations excluded. [R27](#R27), [R32](#R32), [L-10](#L-10)

### Three missingness states that cannot be coded as zero

Usefulness was null in both historical groups: task utility was not measured. Compact rows included a log delta reporting periodic Wi-Fi messages only, while broad rows lacked that delta. The first is limited observation within a captured path; the second is unavailable log evidence. Accelerator device nodes were reported present, which establishes neither application use of the device nor acceleration of inference. These states must not collapse into “no issue” or zero activity. [R28](#R28), [F-19](#F-19)

A claim of useful accelerated field inference would need a task utility measure and application-level evidence of the actual execution path. An absent logged accelerator error is not that evidence. Recovery of old records can clarify what was captured, but it cannot retroactively create an unmeasured usefulness score. Keeping null, unavailable and inspected-not-observed separate makes the historical comparison more informative without strengthening it beyond its receipts. [R28](#R28), [F-16](#F-16), [F-24](#F-24)

### Repeatability without semantics; custody without clean source

Adjacent radio work reported 513 events, comprising 511 read-only and two passive events, 16 candidate channels and matching image evidence across captures or devices. Stable bytes or images can support repeatability of acquisition and representation while the interpretation remains wrong. No validated protocol or channel semantics follows from matching captures or producer-declared acceptance. Controlled known differences and independent operator labels would discriminate meanings more directly than another identical dump. This adjacent work is preserved without becoming a watermark acceptance requirement. [R29](#R29), [F-18](#F-18)

The complete clean exporter snapshot for historical model/radio rows remains unavailable. Dirty-source lineage is explicit; no fresh qualified export repaired it. A separate August preservation ledger with 24 matching entries must not be confused with the October return's defective manifest self-hash. Integrity can bind available files, but it cannot reconstruct missing source or authenticate historical execution. The stronger reproducible clean-producer claim is excluded, while the descriptive historical observations remain. [R32](#R32), [L-10](#L-10), [L-14](#L-14)

That unavailable disposition satisfies the selected request for evidence or an honest limitation. It does not satisfy the stronger claim it excludes. Reopening is appropriate only if a future selected field-performance claim needs complete source and a matching new export. A current clean checkout cannot stand in for the unknown historical exporter state, and another keyless observer run would not answer the missing-source question. [R32](#R32), [F-16](#F-16), [F-19](#F-19)

[FIGURE: F01]

## S07 Continuation, discovery and finite stopping

### Choose the claim before the study size

The current pair supports descriptive, construction-specific observations. It does not establish a rare-error operating point. Even a proposed study with zero errors among 30 independent held-out negatives would give a one-sided 95% binomial upper bound of 1 − 0.05^(1/30), approximately 9.50%, for a fixed rule under its assumptions. The 30/30 draft is unfrozen, so this is a planning calculation, not a reported experimental error bound. [R33](#R33), [F-09](#F-09)

Independence, a fixed threshold, held-out status and a defined population do the inferential work; a sample count alone does not grant them. Selection, dependence and drift can invalidate a naive precision claim. A future calibration study should begin with an estimand and uncertainty target, then choose sampling and stopping rules suitable for that claim. The present limitation is not an instruction to run hundreds of cases merely to close the report or obtain a more attractive performance statement. [R33](#R33), [F-06](#F-06), [F-20](#F-20)

[FIGURE: F08]

### Three different ways to remain uncertain

Known unknowns are named missing premises or measurements: historical activation, exact private profiles, calibration, repetition cause, utility, clean exporter lineage and global novelty. Each can be paired with a discriminator or an explicit decision to defer. Unknown knowns concern information already in the available record but missed in synthesis, such as ordinary separator offsets or closed repairs. Their remedy is source conservation and current-status precedence, not a new scientific experiment. [R09](#R09), [R19](#R19), [R22](#R22), [R28](#R28), [R32](#R32), [R36](#R36)

Unknown unknowns cannot be exhausted by a list of possible causes. The six U probes preserve opportunities for discovery. U-01 concerns omitted profile variables; U-02 concerns failed expected controls; U-03 concerns shared selection failures; U-04 concerns route, version and timestamp changes; U-05 concerns unsupported downstream interpretation; U-06 concerns a concrete residual that defeats current explanations. These are observable triggers for opening a bounded question, not six discovered hidden mechanisms. [R37](#R37), [U-01](#U-01), [U-02](#U-02), [U-03](#U-03), [U-04](#U-04), [U-05](#U-05), [U-06](#U-06)

The historical U-02 wording calls a control expected to signal “negative.” The retained history preserves that error; current implementation guidance uses a positive control expected to signal and a negative control expected not to signal. This small correction illustrates why literal preservation and current instruction must remain distinguishable. Repeating an old sentence without its disposition can reintroduce the error that the record was intended to prevent. [U-02](#U-02), [R37](#R37)

[FIGURE: F09]

### A continuation map, not an assignment queue

The tokenizer construction, single-factor formatting diagnostic and blind interaction comparison are concrete optional routes with different evidence requirements. The first needs a specified output-changing mechanism and the identity-only negative control. The second needs one frozen intervention and all attempts under the existing cap. The third needs blinded features and separation of model, context and communication effects. None follows automatically from an unresolved question, and none would by itself establish provider implementation or general attribution. [R19](#R19), [R22](#R22), [R23](#R23), [A-02](#A-02), [A-03](#A-03), [A-04](#A-04)

More ambitious dependence-aware, temporal, adversarial and formal methods remain in the original frontier. A named mathematical technique is not a validated detector. Before adopting one, choose the estimand or failure mode, a falsifiable control and a finite scope. Simpler profile, custody or sampling errors may explain an anomaly before more elaborate machinery becomes useful. Broader memory, architecture and hardware proposals remain separate projects rather than hidden prerequisites of this case study. [R42](#R42), [R40](#R40), [F-14](#F-14), [F-15](#F-15), [F-23](#F-23)

The preserved record systems serve different purposes: 42 substantive research entries, 36 question/probe identities, 64 original gate identities and 14 claims. They overlap and must not be summed into a count of independent findings. Current effective dispositions lead; historical states remain visible. A scoped response may close through evidence, correction, deferral or exclusion with a reason. The records contain no direct claim-to-gate fields, so a reader should not infer an evidentiary edge merely because a claim and gate share a theme. [S-QUESTIONS](#S-QUESTIONS), [R36](#R36), [R41](#R41)

### When this milestone stops

The stopping rule is a complete inspectable account of the selected evidence, its custody, corrections, limitations and next discriminators. A concrete contradictory receipt or method error can reopen a result. A separately selected stronger claim can justify a new protocol. Persistent uncertainty alone does not turn every optional branch into unfinished mandatory work. This preserves the operator's distinction between collection, analysis, synthesis and publication while avoiding repeated handoffs that obscure the current state. [R41](#R41), [F-20](#F-20), [F-24](#F-24)

A useful continuation begins from the declared boundary: the native distinct-window excess is retained; the raw statistic is affected by repetition; early negative and weak observations remain informative within their methods; utility, calibration, mechanisms and stronger provenance remain unqualified where stated. The work can be inspected and extended without requiring a favorable new experiment, a universal attribution verdict or an invented explanation for every missing signal. [R01](#R01), [R18](#R18), [R28](#R28), [R33](#R33), [R37](#R37)
