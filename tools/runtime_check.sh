#!/usr/bin/env bash
# Drive the game through scripted scenarios and collect on-screen lines that
# found no translation (DLRL_DUMP_UNMATCHED). usage: runtime_check.sh <dlrl.exe> <hdv> <outdir>
EXE="$1"; HDV="$2"; OUT="$3"
mkdir -p "$OUT"

run() {
    local name="$1" frames="$2"; shift 2
    local args=()
    for ev in "$@"; do args+=(--key-event "$ev"); done
    DLRL_DUMP_UNMATCHED=1 timeout 900 "$EXE" --hdv "$HDV" --invincible --show-original-interface \
        --smoke-frames "$frames" "${args[@]}" --capture "$OUT/$name.bmp" 2>&1 \
        | grep '^UNMATCHED|' > "$OUT/$name.txt"
    echo "$name: $(wc -l < "$OUT/$name.txt") unmatched"
}

seq_keys() { # start step key...
    local f=$1 step=$2; shift 2
    for k in "$@"; do echo "$f:$k"; f=$((f + step)); done
}

BOOT=(3500:X)
run utilities 9000 "${BOOT[@]}" 4400:U 5200:DOWN 5500:RETURN 6500:ESC 7000:DOWN 7300:DOWN 7600:RETURN 8300:ESC
run conjure 14000 "${BOOT[@]}" 4400:C 5000:DOWN 5300:RETURN 6300:RETURN 7300:RETURN 8300:Y 9300:RETURN 10300:RETURN 11300:RETURN 12300:Q 12400:A 12500:RETURN
run assemble 9000 "${BOOT[@]}" 4400:C 5000:DOWN 5100:DOWN 5200:DOWN 5300:RETURN 6300:1 6800:RETURN 7500:ESC
run terminate 8000 "${BOOT[@]}" 4400:C 5000:DOWN 5100:DOWN 5300:RETURN 6300:ESC
mapfile -t CMDS < <(seq_keys 6500 450 A ESC B ESC C ESC D ESC E ESC F ESC G ESC H ESC I 1 ESC J ESC K ESC L ESC M ESC N 1 ESC O ESC Q ESC R ESC S T ESC U ESC V ESC W X ESC Y ESC Z 1 ESC)
run commands 26000 "${BOOT[@]}" 4400:P 5500:SPACE "${CMDS[@]}"
WALK=(); f=6500; keys=(RIGHT RIGHT DOWN DOWN LEFT UP F A F 1 RIGHT DOWN F F F LEFT LEFT UP S)
for i in $(seq 1 420); do WALK+=("$f:${keys[$((i % ${#keys[@]}))]}"); f=$((f + 80)); done
run walk 42000 "${BOOT[@]}" 4400:P 5500:SPACE "${WALK[@]}"
cat "$OUT"/*.txt | sort -u > "$OUT/all_unmatched.txt"
echo "total distinct: $(wc -l < "$OUT/all_unmatched.txt")"
