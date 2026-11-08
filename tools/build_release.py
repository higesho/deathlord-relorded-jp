"""Make the distribution ZIP.

usage: python -I build_release.py <build output dir (contains dlrl.exe)> <out dir> <version>

The ZIP only adds files to a Deathlord Relorded 3.0 folder:
  dlrl_ja.exe, assets/misaki_gothic_2nd.ttf, assets/misaki-LICENSE.txt,
  DLRLAssets/ja/game.json, DLRLAssets/ja/ui.json, README_JP.txt, LICENSE-AGPL.txt
It contains no game data.
"""
import os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE_URL = "https://higesho.github.io/deathlord-relorded-jp/"
REPO_URL = "https://github.com/higesho/deathlord-relorded-jp"


def main():
    build, out_dir, version = sys.argv[1:4]
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"DeathlordRelorded_JP_{version}.zip")
    readme = open(os.path.join(ROOT, "dist_src", "README.txt"), encoding="utf-8").read()
    readme = readme.replace("__VERSION__", version).replace("__PAGE_URL__", PAGE_URL)
    readme = readme.replace("__REPO_URL__", REPO_URL)
    files = [
        (os.path.join(build, "dlrl.exe"), "dlrl_ja.exe"),
        (os.path.join(ROOT, "data", "fonts", "misaki_gothic_2nd.ttf"), "assets/misaki_gothic_2nd.ttf"),
        (os.path.join(ROOT, "data", "fonts", "misaki-LICENSE.txt"), "assets/misaki-LICENSE.txt"),
        (os.path.join(ROOT, "data", "ja", "game.json"), "DLRLAssets/ja/game.json"),
        (os.path.join(ROOT, "data", "ja", "ui.json"), "DLRLAssets/ja/ui.json"),
        (os.path.join(ROOT, "LICENSE"), "LICENSE-AGPL.txt"),
    ]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for source, name in files:
            z.write(source, name)
        # Windows Notepad reads UTF-8 with BOM and CRLF reliably.
        z.writestr("README_JP.txt", "﻿" + readme.replace("\n", "\r\n"))
    print(out, os.path.getsize(out))


if __name__ == "__main__":
    main()
