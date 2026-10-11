#!/usr/bin/env python3
"""Check published specimen bytes, historical arithmetic and catalog identities."""
from pathlib import Path
import csv
import hashlib
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text())


def require(value, message):
    if not value:
        raise ValueError(message)


def near(actual, expected, message):
    require(math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), message)


def main():
    methods = load('data/native-methods.public.json')
    for row in [methods['prompt'], *methods['samples']]:
        name = row.get('file', row.get('text_file'))
        data = (ROOT / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == row.get('sha256', row.get('text_sha256')), 'Specimen bytes differ: ' + name)
    require(methods['sampling'] == {'do_sample': True, 'seed': 1337, 'temperature': 0.8, 'top_p': 0.95, 'max_new_tokens': 256, 'retries': 0, 'note': 'Explicit overrides; not a complete dump of library defaults.'}, 'Native sampling conditions differ')
    field = load('data/field-observations.public.json')
    require(len(field['rows']) == 7, 'Field row count')
    for group, summary in field['groups'].items():
        rows = [r for r in field['rows'] if r['group'] == group]
        require(len(rows) == summary['n'], 'Field group count')
        for key, expected in summary['means'].items():
            near(statistics.mean(r[key] for r in rows), expected, 'Field mean: ' + key)
            require([min(r[key] for r in rows), max(r[key] for r in rows)] == summary['ranges'][key], 'Field range: ' + key)
        require(all(r['operator_usefulness'] is None for r in rows), 'Null usefulness lost')
        require(all(r['dmesg_present'] == (group == 'compact') for r in rows), 'Log availability lost')
    for key, value in field['broad_over_compact_mean_ratios'].items():
        near(field['groups']['broad']['means'][key] / field['groups']['compact']['means'][key], value, 'Field ratio: ' + key)
    csv_field = list(csv.DictReader((ROOT / 'data/field-observations.public.csv').open()))
    require(len(csv_field) == 7, 'CSV field row count')
    for left, right in zip(csv_field, field['rows']):
        for key, value in left.items():
            if key in right and isinstance(right[key], (str, int, float)) and not isinstance(right[key], bool):
                require(str(right[key]) == value, 'Field CSV value: ' + key)
        require(left['operator_usefulness'] == 'null', 'CSV null representation')
    audits = load('data/historical-audits.public.json')
    early = audits['early_17']
    require(len(early['files']) == early['file_count'] == 17, 'Audit file count')
    for key in ('bytes', 'characters', 'lines'):
        require(sum(r[key] for r in early['files']) == early['totals'][key], 'Audit total: ' + key)
    require(sum(r['summary']['observable_invisible_codepoint_hits'] for r in early['files']) == early['totals']['observable_invisible_codepoint_hits'] == 0, 'Audit invisible count')
    require(sum(r['summary']['trailing_whitespace_line_count'] for r in early['files']) == early['totals']['trailing_whitespace_lines'] == 2, 'Trailing whitespace count')
    require(sum(item['spaces'] for r in early['files'] for item in r['trailing_horizontal_whitespace']) == 35, 'Ordinary trailing spaces')
    six = audits['six_summaries']
    ids = {r['id'] for r in six['records']}
    require(len(ids) == 6 and len(six['all_pairwise']) == 15 and len(six['focus_pairwise']) == 6, 'Six-summary coverage')
    pairs = {tuple(sorted((r['a'], r['b']))) for r in six['all_pairwise']}
    require(len(pairs) == 15 and all(set(pair) <= ids for pair in pairs), 'Summary pair identities')
    require(all(r in six['all_pairwise'] for r in six['focus_pairwise']), 'Focused comparisons must be an exact subset')
    comp = load('data/comparative-observations.public.json')['paired_corpora']
    prose, cont, agg = comp['prose'], comp['continuations'], comp['aggregate']
    require(len(prose) == agg['prose_pair_count'] == 9 and len(cont) == agg['completion_pair_count'] == 32, 'Corpus pair counts')
    for rows, key, aggregate in [(prose, 'sequence_similarity', 'mean_prose_sequence_similarity'), (prose, 'tfidf_cosine_1_2gram', 'mean_prose_tfidf_cosine'), (cont, 'longest_common_prefix_words', 'mean_completion_lcp_words'), (cont, 'sequence_similarity', 'mean_completion_sequence_similarity')]:
        near(statistics.mean(r[key] for r in rows), agg[aggregate], aggregate)
    for key, aggregate in [('first_word_match', 'completion_first_word_match_count'), ('first_2_words_exact', 'completion_first_2_exact_count'), ('first_4_words_exact', 'completion_first_4_exact_count'), ('completion_exact', 'completion_exact_count')]:
        require(sum(r[key] for r in cont) == agg[aggregate], aggregate)
    require(sum(r['exact_text'] for r in prose) == agg['prose_exact_count'], 'Prose exact count')
    for length in (8, 12):
        require(sum(r[f'shared_{length}grams'] for r in prose) == agg[f'total_shared_corresponding_{length}grams'], 'Corresponding shared ngrams')
    catalog = load('data/artifact-catalog.public.json')
    counted = 0
    for group in catalog['groups']:
        for entry in group['files']:
            path = ROOT / entry['path']
            require(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'Catalog path')
            raw = path.read_bytes()
            require(len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], 'Catalog identity: ' + entry['path'])
            counted += 1
    print(json.dumps({'status': 'pass', 'native_text_files': 3, 'field_rows': 7, 'audit_rows': 17, 'summary_pairs': 15,
                      'prose_pairs': 9, 'continuation_pairs': 32, 'catalog_files': counted,
                      'scope': 'Published bytes and internal arithmetic; no original-input audit, historical event authentication or native key membership.'}, indent=2))


if __name__ == '__main__':
    main()
