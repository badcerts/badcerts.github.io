#!/usr/bin/env python3
"""Replay the published toy controls and compare with the frozen receipt."""
from pathlib import Path
import argparse
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'sources/controls'))
from experiments import repetition_probe, tokenizer_relabeling, finite_sample


def compare(actual, expected, path='result'):
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(actual) != set(expected):
            raise ValueError('Fields differ: ' + path)
        for key in expected:
            compare(actual[key], expected[key], path + '.' + key)
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise ValueError('List differs: ' + path)
        for index, (left, right) in enumerate(zip(actual, expected)):
            compare(left, right, f'{path}[{index}]')
    elif isinstance(expected, float):
        if isinstance(actual, bool) or not isinstance(actual, (int, float)) or not math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError('Floating calculation differs: ' + path)
    elif type(actual) is not type(expected) or actual != expected:
        raise ValueError('Value differs: ' + path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true', help='Print complete recomputed results after comparison.')
    args = parser.parse_args()
    expected = json.loads((ROOT / 'data/synthetic-controls.expected.json').read_text())
    result = {'repetition': repetition_probe(), 'tokenizer_relabeling': tokenizer_relabeling(), 'finite_sample': finite_sample()}
    result = json.loads(json.dumps(result, allow_nan=False))
    compare(result, expected)
    print(json.dumps(result if args.full else {
        'status': 'pass', 'fixed_public_keys_per_fixture': 4096,
        'fixtures': 4, 'relabelings': 24,
        'raw_ge4_counts': [r['raw_ge4_count'] for r in result['repetition']['fixtures']],
        'scope': 'Frozen toy fixtures and planning calculations; no native keys, model execution or calibration.'
    }, indent=2))


if __name__ == '__main__':
    main()
