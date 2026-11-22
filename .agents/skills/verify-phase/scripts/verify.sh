#!/usr/bin/env bash
# verify-phase: cổng kiểm trước khi gắn tag phase-n (nhóm MotTV).
# Chạy: bash .agents/skills/verify-phase/scripts/verify.sh
set -u
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python   # Windows: chỉ có `python`

fail=0
echo "== 1) Test Contract (headless hộp đen + unit nhóm) =="
PYTHONPATH=tests:. "$PY" -m unittest discover -s tests || fail=1

echo; echo "== 2) Kiểm danh sách thành viên (cảnh báo, không chặn) =="
"$PY" tools/check_team.py || echo "  (cảnh báo check_team — bỏ qua nếu là bài nộp solo đã ghi rõ)"

echo; echo "== 3) Hợp đồng build/headless =="
"$PY" - <<'PYEOF'
import json, sys
c = json.load(open("game.contract.json", encoding="utf-8"))
for k in ("build_cmd", "headless_cmd", "run_cmd", "team", "team_size"):
    assert k in c, f"thiếu khoá {k} trong game.contract.json"
print("  OK:", {k: c[k] for k in ("team","team_size","build_cmd","headless_cmd")})
PYEOF
[ $? -eq 0 ] || fail=1

echo; echo "== 4) Smoke CLI headless --ticks 0 =="
for m in gather quan; do
  out="$(mktemp)"
  if PYTHONPATH=tests:. "$PY" -m chonoi.headless --mode "$m" --seed 1 --ticks 0 --out "$out"; then
    echo "  OK: $m"
  else
    echo "  LỖI: headless $m"; fail=1
  fi
  rm -f "$out"
done

echo
if [ "$fail" -eq 0 ]; then
  echo "✅ SẴN SÀNG gắn tag. Nhớ cập nhật docs/verification/phase-n.md rồi: git tag phase-n"
else
  echo "❌ CHƯA sẵn sàng — sửa test đỏ, KHÔNG gắn tag. Ghi trung thực chỗ chưa xong."
fi
exit $fail
