"""Report Deathlord text that has no Japanese translation.

Collects every high-bit-terminated string (Deathlord text is ASCII XOR 0x65,
the last character has bit 7 set) from the scenario file DEATHLORD.Z, the
plain program files and RAM dumps taken in different game states, then checks
each one against the translation dictionary and patterns the way the game
does at run time (whitespace and case are ignored).

usage: python -I check_coverage.py <game.json or game_src.json> <ignore.txt> <out.tsv> <binary files...>
"""
import json, re, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dlkey import key_hash

sys.stdout.reconfigure(encoding="utf-8")

OK = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?'\"-:;()/\r#$%&*+<>=@[]")


def norm(t):
    return re.sub(r"\s+", "", t).upper()


def strings(data):
    cur = bytearray()
    start = None
    for i, b in enumerate(data):
        c = (b & 0x7F) ^ 0x65
        if c in OK:
            if start is None:
                start = i
            cur.append(c)
            if b & 0x80:
                yield start, bytes(cur).decode()
                cur = bytearray()
                start = None
        else:
            cur = bytearray()
            start = None


TOKEN_OK = re.compile(r"^(?:[A-Z][A-Z'\-]*|[A-Z][a-z'\-]+|[a-z][a-z'\-]*|\d+|[A-Z]\d*)$")


def plausible(t):
    s = t.replace("\r", " ").strip()
    words = re.findall(r"[A-Za-z][A-Za-z'\-]*", s)
    if not words or sum(len(w) for w in words) < 3:
        return False
    if not any(len(w) >= 3 and re.search(r"[AEIOUYaeiouy]", w) for w in words):
        return False
    tokens = re.findall(r"[A-Za-z0-9'\-]+", s)
    good = sum(1 for w in tokens if TOKEN_OK.match(w))
    if good / len(tokens) < 0.85:
        return False
    other = sum(1 for c in s if not (c.isalnum() or c in " .,!?'-:#()*/\"=&+"))
    if other > 1:
        return False
    if re.search(r"(.)\1\1", s.replace(" ", "").replace(".", "").replace("*", "").replace("-", "").replace("=", "")):
        return False
    return True


def dos_order(z):
    """DEATHLORD.Z holds the two scenario floppies track by track in ProDOS
    sector order; the game reads DOS 3.3 logical sectors, so text that spans
    sectors only reads continuously after reordering."""
    out = bytearray()
    for t in range(len(z) // 4096):
        track = z[t * 4096:(t + 1) * 4096]
        for s in range(16):
            p = s if s in (0, 15) else 15 - s
            out += track[p * 256:(p + 1) * 256]
    return bytes(out)


def main():
    dict_path, ignore_path, out_path = sys.argv[1:4]
    game = json.load(open(dict_path, encoding="utf-8"))
    keys = set()
    for e in game["entries"]:
        if "src" in e:
            keys.add(norm(e["src"]))
            keys.add(key_hash(e["src"]))
        if "key" in e:
            keys.add(e["key"])
    patterns = [re.compile(p["re"], re.I) for p in game.get("patterns", [])]
    ignore = set()
    if os.path.exists(ignore_path):
        for line in open(ignore_path, encoding="utf-8"):
            line = line.rstrip("\n")
            if line and not line.startswith("## "):
                if re.fullmatch(r"[0-9a-f]{16}", line):
                    ignore.add(line)  # hashed entry (published list)
                else:
                    ignore.add(norm(line.replace("|", " ")))
                    ignore.add(key_hash(line.replace("|", " ")))

    def covered(t):
        k = norm(t)
        if not k or k in keys or key_hash(t) in keys or k in ignore or key_hash(t) in ignore:
            return True
        spaced = re.sub(r"\s+", " ", t).strip().upper()
        if any(p.match(spaced) for p in patterns):
            return True
        return False

    missing = {}
    total = 0
    for path in sys.argv[4:]:
        data = open(path, "rb").read()
        name = os.path.basename(path)
        if name.upper() == "DEATHLORD.Z":
            data = dos_order(data)
        for off, s in strings(data):
            # Program code prints inline strings after a JSR and positioned
            # strings after two coordinate bytes: try trimming such prefixes.
            candidates = [s[k:] for k in range(0, min(6, len(s)))]
            best = None
            for c in candidates:
                if plausible(c):
                    best = c
                    break
            if best is None:
                continue
            total += 1
            if any(covered(c) for c in candidates):
                continue
            k = norm(best)
            if k not in missing:
                missing[k] = (best, f"{name}:{off:x}")
    with open(out_path, "w", encoding="utf-8") as f:
        for k, (t, ref) in missing.items():
            f.write(f"{ref}\t{t.replace(chr(13), '|')}\n")
    print(f"plausible strings: {total}, untranslated: {len(missing)} -> {out_path}")


if __name__ == "__main__":
    main()
