"""List the visible text of every loc::T(...) / HelpMarker(...) literal in C++ sources.

usage: python -I extract_ui_literals.py <out.json> <source files...>
Adjacent literals and backslash line continuations are joined the way the
compiler joins them; "##id" suffixes are dropped (only the label is shown).
"""
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
CALL = re.compile(r'(?:HelpMarker|loc::T)\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)')
LIT = re.compile(r'"((?:[^"\\]|\\.)*)"')


def unescape(text):
    return text.encode("utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")


def main():
    seen = []
    for path in sys.argv[2:]:
        source = open(path, encoding="utf-8").read().replace("\\\n", "")
        for match in CALL.finditer(source):
            text = unescape("".join(LIT.findall(match.group(1)))).split("##")[0]
            if text and text not in seen:
                seen.append(text)
    json.dump(seen, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(seen))


if __name__ == "__main__":
    main()
