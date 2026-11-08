"""Merge an edited TSV (key, english, japanese) from extract_text.py back into game.json.

usage: python -I merge_tsv.py <edited.tsv> <game.json>
Rows with an empty Japanese column are skipped; existing keys are replaced.
"""
import json, sys


def main():
    tsv, game_path = sys.argv[1:3]
    game = json.load(open(game_path, encoding="utf-8"))
    index = {e["key"]: e for e in game["entries"] if "key" in e}
    changed = added = 0
    for line in open(tsv, encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3 or not parts[2].strip():
            continue
        key, ja = parts[0], parts[2].strip()
        if key in index:
            if index[key]["ja"] != ja:
                index[key]["ja"] = ja
                changed += 1
        else:
            entry = {"key": key, "ja": ja}
            game["entries"].append(entry)
            index[key] = entry
            added += 1
    json.dump(game, open(game_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"{changed} changed, {added} added")


if __name__ == "__main__":
    main()
