#!/usr/bin/env python3
"""Render inspectable evidence tables and a file-level catalog from public data."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text())


def table(headers, rows):
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    return '\n' + '| ' + ' | '.join(headers) + ' |\n|' + '|'.join('---' for _ in headers) + '|\n' + ''.join('| ' + ' | '.join(cell(c) for c in row) + ' |\n' for row in rows) + '\n'


def route(path, title=None):
    return f'[{title or path}](PACKAGE/{path})'


def catalog():
    specs = [
        ('E01', 'Owned native specimens and methods', 'S-RESULTS', 'public_exact_specimens_and_method_projection',
         ['data/native-methods.public.json', 'fixtures/native-prompt.public.txt', 'fixtures/native-clean.public.txt', 'fixtures/native-marked.public.txt'],
         'Inspect the exact owned prompt and output quality, match text hashes and inspect scientific conditions.',
         'Original generation receipts are retained privately; scientific settings and text are public. Native keys, model assets and private runtime are not included.'),
        ('E02', 'Native counts and supplied-hit results', 'S-RESULTS', 'public_data_and_reproducible_arithmetic',
         ['fixtures/profile.public.json', 'fixtures/clean-completion.public.json', 'fixtures/marked-completion.public.json', 'data/results.public.json', 'data/results.public.csv', 'data/observation-tracks.public.json', 'data/keyless-check.expected.json'],
         'Recompute exact contexts/windows and all 18 nominal scores from supplied hit counts.',
         'Public wrappers preserve the completion arrays. Aggregate membership hits remain key-holder reported; no public native membership labels are supplied.'),
        ('E03', 'Seven historical field observations', 'S-FIELD-HISTORY', 'public_projection_of_historical_reported_results',
         ['data/field-observations.public.json', 'data/field-observations.public.csv'],
         'Recompute means/ranges; inspect missing utility, log availability and thermal/device observations.',
         'Numerical original report fields are projected publicly with neutral row IDs. Complete clean historical exporter source is unavailable; raw operational logs remain private.'),
        ('E04', 'AgentHRIM and Corax contribution chronology', 'S-FIELD-HISTORY', 'public_projection_of_dated_receipts',
         ['data/field-contributions.public.json', 'data/observer-receipt.public.json'],
         'Distinguish implementation failures/repairs, installed-package qualification, executor preparation and the later observer.',
         'Original handoffs are retained privately and identified by document hashes. No event authentication or new sample independence follows from receipt agreement.'),
        ('E05', 'Early negative audit and six summaries', 'S-EARLY-AUDITS', 'public_measurement_projection_originals_partly_unavailable',
         ['data/historical-audits.public.json'],
         'Inspect 17 audit rows, six summary records and all 15 summary pairs; recompute retained aggregate counts.',
         'The 17 original audit inputs are unavailable. Six summary copies were recovered privately. Their measured fields are public; raw personal context is not redistributed.'),
        ('E06', 'Corpus, null, format and image observations', 'S-COMPARATIVE', 'public_projection_of_historical_reported_results',
         ['data/comparative-observations.public.json', 'data/comparative-observations.public.csv'],
         'Inspect nine prose pairs, 32 constrained continuations, arbitrary-key nulls and parser/format findings.',
         'Original corpora and converted assets are retained privately. The selected aggregates are reproducible from rows; raw-corpus and pooled-ngram recomputation remain unavailable here.'),
        ('E07', 'Frozen toy controls', 'S-ENGINEERING', 'public_fixtures_source_and_reproducible_calculation',
         ['fixtures/synthetic-controls.public.json', 'data/synthetic-controls.expected.json', 'scripts/reproduce_controls.py', 'sources/controls/membership.py', 'sources/controls/diagnostics.py', 'sources/controls/experiments.py', 'sources/controls/README.md', 'sources/controls/LICENSE.axispl.txt'],
         'Repeat all frozen public-key motif trials, all 24 relabelings and finite-sample calculations.',
         'Exact fixtures, public key derivation, focused source and full expected receipt are included. This is a toy replay, not native membership verification or field calibration.'),
        ('E08', 'Full research register', 'S-HISTORY', 'public_research_record',
         ['data/research-register.public.json', 'data/glossary.public.json', 'data/publication-changes.public.json'],
         'Inspect all 42 records, weak/absent signals, assumptions, corrections and open discovery probes.',
         'The original conversation is retained privately. Scientific record fields and publication corrections are public; private locators/personal context are abstracted.'),
        ('E09', 'Questions and original gates', 'S-QUESTIONS', 'public_research_history',
         ['data/future-work.public.json', 'data/original-gates.public.json', 'data/content-map.public.json'],
         'Inspect 36 questions/probes and their histories, plus all 64 original gate obligations.',
         'Historical pending wording is preserved alongside later dispositions. Printing a gate does not recertify it.'),
        ('E10', 'Claims and contribution decisions', 'S-HISTORY', 'public_editorial_and_claim_record',
         ['data/claim-ledger.public.json', 'data/contribution-decisions.public.json', 'data/contribution-implementation.public.json', 'data/format-implementation.public.json', 'design/format-candidates.public.json', 'design/VISUAL_GRAMMAR.md'],
         'Inspect 14 bounded/excluded claims, 26 contribution dispositions and 20 format decisions.',
         'Shared inputs are explicit. Multiple reviews are not independent generations or replicated scientific experiments.'),
        ('E11', 'Ten analytical figures', 'S-HISTORY', 'public_visual_derivatives_and_editable_source',
         ['figures/figures.json'] + [str(p.relative_to(ROOT)) for p in sorted((ROOT/'figures').glob('*.svg'))] + [str(p.relative_to(ROOT)) for p in sorted((ROOT/'figures').glob('*.png'))],
         'Download SVG/PNG plates with captions, units, links and limits. The original F01–F10 identities are retained.',
         'Figures organize the same evidence. Hypothesis lanes, Toulmin maps, the shared-input network and provenance cutaway are explanatory structures, not new measurements.'),
        ('E12', 'Methods, manuscripts and build sources', 'S-ENGINEERING', 'public_editable_sources_and_verifiers',
         ['manuscript/narrative.md', 'manuscript/methods.md', 'manuscript/background-sources.md', 'docs/REPRODUCE.md', 'docs/DATA_DICTIONARY.md', 'data/source-map.public.json', 'sources/build_atlas.py', 'sources/build_supplement.py', 'sources/build_figures.py', 'sources/format_cards_history.py', 'sources/format_cards_network.py', 'sources/format_cards_cutaway.py', 'sources/finalize_package.py', 'sources/requirements.txt', 'scripts/verify_public_package.py', 'scripts/verify_supplement.py', 'scripts/VERIFICATION_SCOPE.md'],
         'Read method definitions, check payload integrity and rebuild the static reader/report locally.',
         'Build sources are delivered as source files. They are not a deployed backend; rebuilding changes output identities and requires fresh visual review.'),
    ]
    groups = []
    for id_, title, family, availability, paths, check, limit in specs:
        files = []
        for path in paths:
            file = ROOT/path
            files.append({'path':path, 'bytes':file.stat().st_size, 'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
        groups.append({'id':id_, 'title':title, 'source_family':family, 'availability':availability,
                       'reader_check':check, 'original_and_limit':limit, 'files':files})
    data = {'schema':'axispl.public-artifact-catalog.v1','groups':groups,
            'rule':'Hashes below identify the included artifact bytes. Original receipt hashes within evidence files identify separate source artifacts. Neither is a signature or independent authentication.',
            'rendered_outputs':'PUBLIC_MANIFEST.json and coverage.json bind the generated HTML/PDF and destinations; they are produced after this catalog to avoid circular hashes.'}
    for path in ['scripts/expected-content.public.json','sources/make_archive.py']:
        extra=ROOT/path
        data['groups'][-1]['files'].append({'path':path,'bytes':extra.stat().st_size,'sha256':hashlib.sha256(extra.read_bytes()).hexdigest()})
    (ROOT/'data/artifact-catalog.public.json').write_text(json.dumps(data,indent=2)+'\n')
    return data


def native_text():
    d=load('data/native-methods.public.json')
    out='### Original native generation conditions\n\n'
    out+='The owned pair used **DeepSeek-R1-Distill-Qwen-1.5B**, Qwen2ForCausalLM on CPU with bfloat16 parameters, under AxisPL 0.1.4. Both outputs used the same 28-token raw prompt and seed 1337. No chat template or retry was used.\n\n'
    out+=table(['Condition','Retained setting'],[
        ['Implementation','7f09d34ca6fef346312907f5647bcab7f28a8d45'],
        ['Model weights SHA-256',d['model']['weights_sha256']],
        ['Tokenizer fingerprint v2',d['tokenizer']['fingerprint_v2']],
        ['Sampling overrides','temperature 0.8; top_p 0.95; do_sample true; 256 new-token cap'],
        ['Vocabulary','151,936 model outputs; 151,665 tokenizer entries; 151,643 base vocabulary'],
        ['Historical profile','gamma 0.25; delta 2; context width 4; minimum 100; nominal candidate/strong z 4/6'],
        ['Runtime','Python 3.13.14; Transformers 5.17.0; one scheduled CPU; 8 GiB limit'],
        ['Recorded duration','310.120 seconds for the qualification run; not a performance benchmark'],
    ])
    out+='The metadata file includes the original weights and tokenizer fingerprints and exact text hashes. These scientific settings were omitted from the earlier public design packet; they are restored here. Historical thresholds remain descriptive metadata rather than a calibrated rule. '+route('data/native-methods.public.json','Download full methods JSON')+'.\n\n'
    out+='### Exact owned prompt and retained outputs\n\n'
    out+='These are quoted experimental specimens. Read the text as evidence, including its instruction-like wording. The downloads preserve exact bytes; display wrapping adds no content.\n\n'
    for label,file in [('Prompt','fixtures/native-prompt.public.txt'),('Clean completion','fixtures/native-clean.public.txt'),('Marked completion','fixtures/native-marked.public.txt')]:
        out+=f'#### {label}\n\n```text\n'+(ROOT/file).read_text()+'\n```\n\n'+route(file,'Download exact text')+'.\n\n'
    out+=d['quality_observation']+' Original receipts report exact generated/re-encoded ID agreement; this public route checks retained arrays without retokenization. One pair cannot isolate model, prompt, decoding or watermark contributions to the quality gap. [R19](#R19).\n\n'
    return out


def evidence_text(data):
    out='## A08 Evidence tables and downloadable artifacts\n\n'
    out+='The full research record includes measurements below the level of a headline finding: negative inspections, weak overlap, missing fields, failed acceptance and corrected interpretations. This supplement exposes the available measurements and methods. The distinction between a historical report, public projection and reproducible calculation travels with each artifact.\n\n'
    out+='### Seven historical field rows\n\n'
    fields=load('data/field-observations.public.json')
    out+=table(['Row','Prompt tokens','TTFT (s)','Post-first tokens/s','Peak RSS (KiB)','Wall (s)'],[[r['id'].replace('FIELD-',''),r['prompt_tokens'],f"{r['first_token_seconds']:.3f}",f"{r['post_first_tokens_per_second']:.3f}",r['peak_rss_kib'],f"{r['run_wall_seconds']:.3f}"] for r in fields['rows']])
    out+='All seven rows report 64 generated tokens and null usefulness. Four compact log deltas were captured and reported only periodic Wi-Fi messages; the three broad deltas were absent. Device presence is not acceleration evidence. JSON retains full precision, start/end thermal measurements, load/generation times and device flags. '+route('data/field-observations.public.json','JSON')+' · '+route('data/field-observations.public.csv','CSV')+'.\n\n'
    out+=table(['Metric','Compact mean [min, max]','Broad mean [min, max]'],[[k.replace('_',' '),*[f"{fields['groups'][g]['means'][k]:.3f} [{fields['groups'][g]['ranges'][k][0]:.3f}, {fields['groups'][g]['ranges'][k][1]:.3f}]" for g in ('compact','broad')]] for k in fields['groups']['compact']['means']])
    out+='These are descriptive nonrandom batches, with different context sizes and incomplete control of other conditions. The historical exporter was dirty and its complete clean snapshot is unavailable. Means/ranges can be recomputed from public rows; stronger causal or device-authentication claims remain unsupported. [R27](#R27), [R28](#R28), [R32](#R32).\n\n'
    out+='### What AgentHRIM and Corax contributed\n\n'
    for event in load('data/field-contributions.public.json')['events']:
        out+=f"#### {event['date']} — {event['activity']}\n\n{event['contributor']}. {event['result']}\n\n{event['limit']}\n\n"
    out+=route('data/field-contributions.public.json','Chronology JSON with original source-document hashes')+'.\n\n'
    audits=load('data/historical-audits.public.json');early=audits['early_17'];six=audits['six_summaries']
    out+='### The negative byte audit remains a measured result\n\n'
    out+=early['original_input_availability']+' The report totals 237,506 bytes, 234,326 characters and 2,644 lines. The inspected invisible-codepoint count is zero; two trailing-space lines contain 35 ordinary spaces. This does not establish sensitivity to an undisclosed token-level mechanism.\n\n'
    out+=table(['Specimen','Bytes','Characters','Lines','Invisible hits','Trailing-space lines'],[[r['id'],r['bytes'],r['characters'],r['lines'],r['summary']['observable_invisible_codepoint_hits'],r['summary']['trailing_whitespace_line_count']] for r in early['files']])
    out+='### Six summaries: overlap and collection limits\n\n'
    out+=six['task_context']+' '+six['input_availability']+' The failed collection assumption and possible hidden context remain in R06; descriptive condition labels do not identify which user produced a pair.\n\n'
    out+=table(['Specimen / condition','Bytes','Body words','Unique words'],[[r['id']+' / '+r['condition_label'],r['bytes'],r['body_word_count'],r['body_unique_word_count']] for r in six['records']])
    out+=table(['Focused pair','Character ratio','Word ratio','Word cosine','Longest shared run'],[[r['a']+' / '+r['b'],f"{r['character_sequence_ratio']:.4f}",f"{r['word_sequence_ratio']:.4f}",f"{r['word_cosine_similarity']:.4f}",r['longest_shared_contiguous_word_run']] for r in six['focus_pairwise']])
    out+='All 15 pairs, Unicode/whitespace counts, shared-ngram counts and ZIP measurements remain in '+route('data/historical-audits.public.json','the audit projection')+'. A six-pair focused view adds no new samples. Shared task constraints and style remain alternatives to a hidden carrier. [R05](#R05), [R06](#R06), [R07](#R07).\n\n'
    comp=load('data/comparative-observations.public.json')
    out+='### Paired corpora and the arbitrary-key null\n\n'
    out+='Nine prose pairs and 32 constrained continuations share byte-identical prompt inputs. None of the nine prose or 32 completion pairs is exactly identical. Twenty of 32 continuations share the first word, twelve share the first two, and eight share the first four. That is a weak conditional observation with prompt/context confounds, not a person-level fingerprint.\n\n'
    out+=table(['Pair','Words A / B','Sequence ratio','TF–IDF cosine','Shared 8-grams'],[[r['id']+' '+r['length_group'],str(r['word_count_a'])+' / '+str(r['word_count_b']),f"{r['sequence_similarity']:.4f}",f"{r['tfidf_cosine_1_2gram']:.4f}",r['shared_8grams']] for r in comp['paired_corpora']['prose']])
    n=comp['arbitrary_key_null']
    out+=table(['Corpus','Surrogate tokens','Mean nominal z','Population SD','Range','z ≥ 4 / ≥ 6'],[[g.upper(),n['tokens_'+g],f"{n[g]['mean']:.6f}",f"{n[g]['population_sd']:.6f}",f"{n[g]['min']:.6f} to {n[g]['max']:.6f}",str(n[g]['ge4'])+' / '+str(n[g]['ge6'])] for g in ('a','b')])
    out+='This scan used 64 deterministic arbitrary keys, a 3,902-entry word-plus-punctuation vocabulary, width 4 and gamma 0.25. It checks the local laboratory profile under those keys; no provider key, tokenizer or detector was supplied. It is separate from the later 4,096-key motif control. '+route('data/comparative-observations.public.json','Full comparison JSON')+' · '+route('data/comparative-observations.public.csv','All 41 pair rows as CSV')+'.\n\n'
    out+='### Format and instrument findings\n\n'
    out+='The cross-format report retained 300 structured rows: 288 valid and 12 invalid. Clean JSONL and CSV agreed on values/order. Five HTML and nine PDF source-segment word sequences matched; two code segments also matched after removing whitespace. Conversion did not create independent linguistic samples.\n\n'
    for finding in comp['cross_format']['axispl_0_1_0_findings']:out+='- '+finding['detail']+'\n'
    out+='\nThe code/schema discrepancies remain concrete, rather than being hidden by passing tests:\n\n'
    for finding in comp['cross_format']['code']['contract_drift']:out+='- '+finding+'\n'
    out+='\nFive related images had no observed embedded C2PA/signed-provenance structure in the inspected container channels. Public fields retain export methods and structural scan results. Undisclosed steganography, unknown sensitivity and generation provenance remain outside that observation. [R12](#R12), [R13](#R13), [R15](#R15), [R16](#R16).\n\n'
    controls=load('data/synthetic-controls.expected.json')
    out+='### Reproducible toy controls and planning arithmetic\n\n'
    out+=table(['Fixture','Raw positions','Distinct windows','Raw z ≥ 4','Distinct z ≥ 4'],[[r['fixture'],r['scorable_positions'],r['unique_context_token_windows'],str(r['raw_ge4_count'])+'/4096',str(r['dedup_ge4_count'])+'/4096'] for r in controls['repetition']['fixtures']])
    out+='The same 16-window motif is repeated 4, 16 and 64 times. The fixed public key trials and full expected receipt are supplied; there was no native-key search. Raw threshold crossings are toy behavior, not natural-text FPR. All 24 consistent four-symbol ID permutations preserve decoded probability mass. The distinct sequences [1,2] and [3] both decode to “watermark”; segmentation alone need not survive decoding. Generation-coupled alternatives remain open.\n\n'
    out+=table(['Independent held-out negatives, zero false positives','One-sided 95% upper bound'],[[n,f'{v:.6f}'] for n,v in controls['finite_sample']['zero_false_positives_one_sided_95_upper'].items()])
    out+='The bound assumes a fixed rule and independent held-out negatives. It takes 299 such zero-error negatives to put the upper bound at or below 1%. With 30 continuous exchangeable calibration scores the smallest split-conformal p value is 1/31, while an empirical error-rate increment is 1/30. A separate illustrative 90% sensitivity / 99% specificity / 1% prevalence calculation gives PPV 0.47619. These are planning calculations, not attained operating performance.\n\n'
    out+='```text\npython3 -I -B scripts/reproduce_controls.py\n```\n\n'+route('docs/REPRODUCE.md','Reproduction guide')+' · '+route('docs/DATA_DICTIONARY.md','Data dictionary')+'.\n\n'
    out+='### Publication correction record\n\n'
    for c in load('data/publication-changes.public.json')['changes']:
        out+=f"**{c['id']} — {c['reason']}**\n\nEarlier wording: {c['old']}\n\nCurrent wording: {c['new']}\n\n{c['claim_impact']}\n\n"
    out+='### Artifact catalog\n\n'
    out+=data['rule']+' The PDF/HTML and their destinations are bound later by the package manifest and coverage record.\n\n'
    out+=' · '.join(f'[{g["id"]}](#{g["id"]})' for g in data['groups'])+'\n\n'
    for group in data['groups']:
        out+=f"<h4 id=\"{group['id']}\">{group['id']} — {group['title']}</h4>\n\n{group['reader_check']}\n\n{group['original_and_limit']}\n\n"
        for file in group['files']:out+='- '+route(file['path'])+'\n'
        out+='\n'
    out+='Full byte lengths and SHA-256 values are in '+route('data/artifact-catalog.public.json','the machine-readable catalog')+'. The catalog distinguishes included artifacts from privately held or unavailable originals.\n'
    return out


def main():
    data=catalog()
    (ROOT/'manuscript/native-specimens.md').write_text(native_text())
    (ROOT/'manuscript/evidence.md').write_text(evidence_text(data))
    print(json.dumps({'catalog_groups':len(data['groups']),'catalog_files':sum(len(g['files']) for g in data['groups'])}))


if __name__=='__main__':
    main()
