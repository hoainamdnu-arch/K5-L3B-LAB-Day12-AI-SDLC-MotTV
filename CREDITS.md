# Credits

## Asset ngoài
Không dùng asset ngoài. Toàn bộ đồ họa buổi sáng/buổi tối là **hình khối vẽ bằng Canvas 2D**
trong `chonoi/web/index.html` (tự vẽ), dùng emoji Unicode (🏮 ★ 🍚 🍲) cho HUD. Không ảnh/âm thanh bên thứ ba.

## Nhân vật & bối cảnh
Nhân vật Út Sen, bối cảnh "Quán Ăn Chợ Nổi" là bản gốc của lab (giảng viên cấp). Nhóm MotTV không thêm asset ngoài.

## Công cụ AI
- **Claude Code (model Claude Opus 4.8)** — cặp lập trình cho luật game, test, skill, tài liệu.
  Chi tiết: `docs/ai-usage-log.md`.

## Khung kỹ thuật
Khung Python `chonoi/` (CLI, runner, rng, ids, jsonl, inventory, live window) do giảng viên cấp;
nhóm viết luật `chonoi/sim/gather.py`, `chonoi/sim/quan.py` và test của nhóm.
