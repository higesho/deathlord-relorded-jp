Deathlord Relorded 日本語化パッチ __VERSION__
==================================================

1987年の Apple II 用 RPG「Deathlord」のリメイク版エミュレーター
「Deathlord Relorded 3.0」を日本語で遊べるようにする非公式パッチです。
メッセージ・NPCの台詞・看板・戦闘メッセージ・店や寺院・キャラクター作成・
メニューなどを日本語にします。

紹介ページ: __PAGE_URL__


■ 対応しているもの
  Deathlord Relorded 3.0 テスト版（Windows 版、BUILD-INFO.txt の Commit が
  f5c453fcf004324f07f9a71428cf820ee5cc1a4b のもの）で動作を確認しています。
  Deathlord Relorded は itch.io（https://rikkles.itch.io/deathlord-relorded）から入手できます。
  ゲーム本体（ディスクイメージ）は Deathlord Relorded に含まれています。このパッチには含まれていません。


■ Deathlord Relorded の導入（まだの方）
  1. itch.io の Deathlord Relorded のページ（https://rikkles.itch.io/deathlord-relorded）から、
     Windows 版の 3.0 テスト版（deathlord-relorded-windows-3-test.zip）をダウンロードします。
  2. ZIP の中身をフォルダごとすべて展開します。dlrl.exe の横のフォルダや SDL3.dll も必要なので、
     dlrl.exe だけを移動しないでください。
  3. dlrl.exe を起動してタイトル画面が出ることを確かめます。OpenGL 対応のグラフィックドライバが必要です。
     署名のないテスト版のため、「PC が保護されました」が出たら「詳細情報」→「実行」で起動できます。
     初回の起動時に、同梱のディスクイメージをユーザーごとの保存フォルダにコピーして使います。

  ゲームの始め方：タイトルで何かキー →「キャラクター設定」でキャラクターを 6 人作る
  →「パーティを解散する」→「パーティを編成する」で 6 人のパーティを組む
  → メインメニューで「ゲームを始める」→ Space キー。
  コマンドや呪文の説明は日本語の遊び方ガイド（https://higesho.github.io/deathlord-relorded-jp/guide.html）に
  まとめています。英語の原本は https://archive.org/download/Deathlord/Deathlord.pdf です。


■ インストール
  ZIP の中身（dlrl_ja.exe、assets フォルダ、DLRLAssets フォルダ）を、
  Deathlord Relorded のフォルダ（dlrl.exe のある場所）にそのままコピーします。
  上書きされるファイルはありません（追加されるだけです）。

  あとは dlrl_ja.exe を起動してください。元の dlrl.exe もそのまま使えます。
  セーブデータは英語版と共通なので、英語版の続きをそのまま日本語で遊べます。


■ アンインストール（元に戻す）
  コピーした次のファイルを削除します。
    dlrl_ja.exe
    assets\misaki_gothic_2nd.ttf
    assets\misaki-LICENSE.txt
    DLRLAssets\ja フォルダ


■ 操作
  F9      日本語表示のオン/オフ（メニュー：Relorded → 日本語表示）
  F10     職業・種族名を疑似日本語名／英語の D&D 名で切り替え（原作の機能）
  F11     オリジナル画面（Apple II の画面）の表示切り替え
  Ctrl-P  キャンプ　　Alt-P  一時停止
  そのほかの操作は Deathlord Relorded の DOCUMENTATION.md と原作のマニュアルを見てください。


■ しくみ
  ゲーム本体（6502 のプログラムとディスクイメージ）には手を加えていません。
  ゲームが表示した英語を画面から読み取り、その上に日本語を重ねて表示します。
  日本語には、原作の 7×8 ドットの文字に合わせて 8×8 ドットの「美咲ゴシック第2」を使っています。


■ 遊ぶときの注意
  ・会話のキーワード、呪文名、合言葉は英語（ローマ字）で入力します。
    台詞の中のキーワードになりそうな語には「塔(TOWER)」のように英語を添えています。
    呪文名（AKARI、ZUMA など）や「七つの言葉」（YOKUSEI など）はローマ字のままです。
  ・呪文一覧ウィンドウ（Alt-S）は画像なので英語のままです。
  ・キャラクター名・パーティ名はプレイヤーが付けた英字のまま表示します。
  ・訳のない文や、数値・名前を組み合わせた文の一部が英語のまま出ることがあります。
  ・ベータ版です。全編を通したプレイでの確認はまだ済んでいません（エンディングは未確認です）。
  ・誤訳や不自然な箇所、英語のまま残る文があれば GitHub の Issues でお知らせください。
    場面とスクリーンショットがあると助かります。


■ 翻訳データ
  DLRLAssets\ja\game.json   ゲーム内の文の訳と、数値入りの文のパターン
  DLRLAssets\ja\ui.json     Deathlord Relorded の画面の訳
  原文はハッシュ値でだけ記録しています。訳の直し方はリポジトリの README を見てください。


■ ライセンス・クレジット
  ・dlrl_ja.exe は Deathlord Relorded（Rikkles、協力 qkumba・BillG）を改変したもので、
    GNU Affero General Public License v3 に従います（LICENSE-AGPL.txt）。
    改変を含むソースコードは __REPO_URL__ で公開しています。
  ・美咲フォント（美咲ゴシック第2）門真 なむ 様 https://littlelimit.net/misaki.htm
    自由に利用・改変・再配布できます（assets\misaki-LICENSE.txt）。


■ 免責
  本パッチは非公式のファン翻訳であり、Electronic Arts、原作者、Deathlord Relorded の作者とは関係ありません。
  使用は自己責任でお願いします。本パッチの使用により生じたいかなる損害についても責任を負いません。
  Deathlord (c) 1987 Al Escudero, David Wong / Electronic Arts.
