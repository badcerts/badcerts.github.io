"""Replays of the retained public-key toy controls and planning calculations."""
import collections
import hashlib
import itertools
import json
import math
import statistics
from pathlib import Path
import membership
from diagnostics import windows, multiplicity_diagnostics, zscore

def repetition_probe(keys=4096):
    w = membership
    gamma = 0.25
    vocab = 4096
    fixtures = json.loads((Path(__file__).resolve().parents[2] / 'fixtures/synthetic-controls.public.json').read_text())['fixtures']
    ret = []
    for label, ids in fixtures.items():
        c = collections.Counter(windows(ids, vocab, []))
        scores = []
        dedup = []
        for i in range(keys):
            key = hashlib.sha256(f'AxisPL public synthetic null v1 {i}'.encode()).digest()
            bits = [int(w.token_is_green(w.context_seed(key, prefix, vocab_size=vocab), target, gamma)) for prefix, target in c]
            h = sum((bit * weight for bit, weight in zip(bits, c.values())))
            scores.append(zscore(h, sum(c.values()), gamma))
            dedup.append(zscore(sum(bits), len(c), gamma))
        ret.append({'fixture': label, **multiplicity_diagnostics(windows(ids, vocab, [])), 'fixed_public_key_trials': keys, 'z_mean': statistics.mean(scores), 'z_sd': statistics.stdev(scores), 'raw_ge4_count': sum((s >= 4 for s in scores)), 'raw_ge4_fraction': sum((s >= 4 for s in scores)) / keys, 'raw_ge6_count': sum((s >= 6 for s in scores)), 'dedup_ge4_count': sum((s >= 4 for s in dedup)), 'dedup_z_sd': statistics.stdev(dedup)})
    return {'scope': 'synthetic null over frozen public keys, NOT empirical FPR over natural text', 'predeclared_trials': keys, 'native_trace_keys_tested': False, 'key_search': False, 'fixtures': ret}

def tokenizer_relabeling():
    symbols = ['oak', 'river', 'stone', 'cloud']
    weights = [1, 2, 3, 4]
    total = sum(weights)
    checks = 0
    for perm in itertools.permutations(range(4)):
        relabeled = [0] * 4
        inverse = {}
        for original, new in enumerate(perm):
            relabeled[new] = weights[original]
            inverse[new] = symbols[original]
        original_dist = dict(zip(symbols, weights))
        decoded_dist = {inverse[i]: relabeled[i] for i in range(4)}
        assert original_dist == decoded_dist
        checks += 1
    pieces = {1: 'water', 2: 'mark', 3: 'watermark'}
    sequences = [[1, 2], [3]]
    texts = [''.join((pieces[i] for i in seq)) for seq in sequences]
    assert texts[0] == texts[1]
    return {'permutations_checked': checks, 'decoded_probability_mass_identical': True, 'segmentation_example': {'id_sequences': sequences, 'decoded_texts': texts, 'identical_bytes': True}, 'conclusion': 'Consistent bijective ID relabeling alone leaves decoded probabilities unchanged; latent segmentation alone need not survive decoding.', 'not_tested': ['tokenizer choices that alter emitted-text distribution', 'custom non-bijective keyed encoders coupled to generation', 'private provider mechanisms', 'novelty claim']}

def finite_sample():
    alpha = 0.05
    return {'scope': 'exact binomial zero-success bounds assuming independent fixed-threshold held-out negatives', 'zero_false_positives_one_sided_95_upper': {str(n): 1 - alpha ** (1 / n) for n in [30, 60, 100, 299, 300]}, 'negatives_required_zero_fp_upper_at_most_one_percent': math.ceil(math.log(alpha) / math.log(0.99)), 'calibration_30_empirical_nonzero_step': 1 / 30, 'continuous_exchangeable_split_conformal_30_min_p': 1 / 31, 'base_rate_example': {'sensitivity': 0.9, 'specificity': 0.99, 'prevalence': 0.01, 'positive_predictive_value': 0.9 * 0.01 / (0.9 * 0.01 + 0.01 * 0.99)}, 'not_permission_to_expand_pilot': True}
