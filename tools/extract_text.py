"""Extract Deathlord's English text from your own game image for translation work.

usage:
  python -I extract_text.py <Deathlord PRODOS.hdv> <game.json> <out.tsv> [ram dumps...]

Reads the ProDOS files on the HDV (DEATHLORD.Z scenario data is put back into
DOS 3.3 sector order), optionally RAM dumps taken with dlrl_capture
--memory-output (the game engine is compressed on disk), collects every
high-bit-terminated string and writes a TSV:

  key <TAB> english <TAB> japanese

with the translation looked up by hash in game.json. Line breaks are written
as "|". Edit the third column and merge it back with merge_tsv.py. The TSV
contains the game's own text: keep it local, do not publish it.
"""
import json, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dlkey import key_hash
from check_coverage import strings, plausible, dos_order

sys.stdout.reconfigure(encoding="utf-8")


def prodos_files(image):
    block = lambda n: image[n * 512:(n + 1) * 512]
    files = {}

    def read_dir(key, prefix=""):
        current, first = key, True
        while current:
            data = block(current)
            following = struct.unpack_from("<H", data, 2)[0]
            for i in range(13):
                if first and i == 0:
                    continue
                entry = data[4 + i * 39:4 + (i + 1) * 39]
                storage, length = entry[0] >> 4, entry[0] & 15
                if storage == 0:
                    continue
                name = prefix + entry[1:1 + length].decode()
                key_block = struct.unpack_from("<H", entry, 0x11)[0]
                eof = entry[0x15] | entry[0x16] << 8 | entry[0x17] << 16
                if storage == 0xD:
                    read_dir(key_block, name + "/")
                    continue
                if storage == 1:
                    content = block(key_block)
                elif storage == 2:
                    index = block(key_block)
                    content = b"".join(block(index[j] | index[256 + j] << 8) for j in range(256))
                else:
                    master = block(key_block)
                    content = b""
                    for k in range(128):
                        n = master[k] | master[256 + k] << 8
                        if not n:
                            break
                        index = block(n)
                        content += b"".join(block(index[j] | index[256 + j] << 8) for j in range(256))
                files[name] = content[:eof]
            first, current = False, following

    read_dir(2)
    return files


def main():
    hdv, game_path, out_path = sys.argv[1:4]
    game = json.load(open(game_path, encoding="utf-8"))
    ja = {e["key"]: e["ja"] for e in game["entries"] if "key" in e}
    sources = []
    for name, content in prodos_files(open(hdv, "rb").read()).items():
        if name.startswith("DEATHLORD"):
            sources.append((name, dos_order(content) if name == "DEATHLORD.Z" else content))
    for path in sys.argv[4:]:
        sources.append((os.path.basename(path), open(path, "rb").read()))
    seen, rows = set(), []
    for name, data in sources:
        for offset, text in strings(data):
            for skip in range(0, min(6, len(text))):
                candidate = text[skip:]
                if plausible(candidate):
                    k = key_hash(candidate)
                    if k not in seen:
                        seen.add(k)
                        rows.append((k, candidate.replace("\r", "|"), ja.get(k, "")))
                    break
    with open(out_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write("\t".join(row) + "\n")
    done = sum(1 for r in rows if r[2])
    print(f"{len(rows)} strings, {done} translated -> {out_path}")


if __name__ == "__main__":
    main()
