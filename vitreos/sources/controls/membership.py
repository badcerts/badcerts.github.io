"""Frozen AxisPL membership functions, used only with public toy keys here."""
from __future__ import annotations
import hashlib
import hmac
import struct
from collections.abc import Sequence

MASK64 = (1 << 64) - 1
SCHEME_NAME = "hmac-sha256-splitmix64-greenlist-v1"

def _serialize_context(context_ids: Sequence[int], *, vocab_size: int, scheme: str=SCHEME_NAME) -> bytes:
    payload = bytearray()
    payload.extend(scheme.encode('utf-8'))
    payload.extend(b'\x00')
    payload.extend(struct.pack('>Q', int(vocab_size)))
    payload.extend(struct.pack('>I', len(context_ids)))
    for token_id in context_ids:
        if token_id < 0:
            raise ValueError('Token IDs must be non-negative.')
        payload.extend(struct.pack('>Q', int(token_id)))
    return bytes(payload)

def context_seed(key: bytes, context_ids: Sequence[int], *, vocab_size: int, scheme: str=SCHEME_NAME) -> int:
    digest = hmac.new(key, _serialize_context(context_ids, vocab_size=vocab_size, scheme=scheme), hashlib.sha256).digest()
    return int.from_bytes(digest[:8], 'big', signed=False)

def splitmix64(value: int) -> int:
    value = value + 11400714819323198485 & MASK64
    value = (value ^ value >> 30) * 13787848793156543929 & MASK64
    value = (value ^ value >> 27) * 10723151780598845931 & MASK64
    return (value ^ value >> 31) & MASK64

def token_is_green(seed: int, token_id: int, gamma: float) -> bool:
    if not 0.0 < gamma < 1.0:
        raise ValueError('gamma must be between 0 and 1.')
    mixed = splitmix64((seed ^ (int(token_id) + 1) * 15485907386658061715) & MASK64)
    threshold = int(gamma * (1 << 32))
    return mixed >> 32 < threshold
