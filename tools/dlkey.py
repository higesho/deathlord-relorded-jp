"""Dictionary keys shared with src/Localization.cpp.

The runtime ignores whitespace (anything <= 0x20) and ASCII case, then hashes
the result with 64-bit FNV-1a. Published data stores only the hash.
"""


def normalize(text):
    out = bytearray()
    for b in text.encode("utf-8"):
        if b <= 0x20:
            continue
        if 0x61 <= b <= 0x7A:
            b -= 0x20
        out.append(b)
    return bytes(out)


def key_hash(text):
    h = 14695981039346656037
    for b in normalize(text):
        h = ((h ^ b) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return f"{h:016x}"
