"""Exact tuple recurrence and nominal score calculations."""
import collections
import math

def check_ids(ids):
    if not isinstance(ids, list) or any((type(i) is not int or i < 0 or i >= 2 ** 64 for i in ids)):
        raise ValueError('token IDs must be nonnegative uint64 integers')
    if len(ids) > 100000:
        raise ValueError('trace too long')

def windows(ids, vocab, excluded, width=4):
    check_ids(ids)
    if type(width) is not int or width < 1 or type(vocab) is not int or (vocab < 1):
        raise ValueError('invalid profile')
    return [(tuple(ids[i - width:i]), ids[i]) for i in range(width, len(ids)) if ids[i] < vocab and ids[i] not in excluded]

def multiplicity_diagnostics(ws):
    c = collections.Counter(ws)
    ct = collections.Counter((w[0] for w in ws))
    n = len(ws)
    if not n:
        return {'scorable_positions': 0, 'unique_contexts': 0, 'unique_context_token_windows': 0}
    s2 = sum((v * v for v in c.values()))
    return {'scorable_positions': n, 'unique_contexts': len(ct), 'unique_context_token_windows': len(c), 'repeated_context_fraction': 1 - len(ct) / n, 'repeated_window_fraction': 1 - len(c) / n, 'context_multiplicity_histogram': dict(sorted(collections.Counter(ct.values()).items())), 'window_multiplicity_histogram': dict(sorted(collections.Counter(c.values()).items())), 'max_context_multiplicity': max(ct.values()), 'sum_squared_window_weights': s2, 'duplicate_only_design_effect': s2 / n, 'duplicate_only_weighted_n': n * n / s2, 'weighted_n_assumption': 'independent equal-variance distinct-window indicators; NOT an independence claim or calibrated effective sample size'}

def zscore(h, n, gamma=0.25):
    return (h - n * gamma) / math.sqrt(n * gamma * (1 - gamma))
