---
name: add-menu-dish
description: Thêm một món ăn mới cho quán ĐÚNG quy ước lab — chỉ sửa dữ liệu trong game.contract.json (recipe/cook_s/price), KHÔNG hard-code số trong luật, kèm kiểm tra tất định. Dùng khi người dùng muốn "thêm món", "thêm công thức", "thêm đồ ăn mới", "mở rộng menu", hoặc chỉnh giá/thời gian nấu.
---

# add-menu-dish — thêm món mới an toàn

Quy tắc vàng của lab: **số liệu chỉ nằm trong `game.contract.json`; luật chỉ đọc từ đó.**
`QuanSim` đã đọc toàn bộ `tuning.menu` động, nên thêm món **không cần sửa luật**.

## Khi nào dùng
Khi muốn thêm/sửa món ăn, công thức, giá, thời gian nấu — phần "Tự do sáng tạo" của lab.

## Các bước
1. Mở `game.contract.json` → mục `tuning.menu`. Thêm một khoá món mới, ví dụ:
   ```json
   "canh_chua_ca_linh": { "recipe": { "ca_linh": 2, "bong_sung": 1 }, "cook_s": 8, "price": 90 }
   ```
   - `recipe`: chỉ dùng nguyên liệu hợp lệ (`ca_loc`, `ca_linh`, `bong_dien_dien`, `bong_sung`).
   - `cook_s` > 0; `price` nguyên dương.
2. KHÔNG thêm số (giá, thời gian) vào `chonoi/sim/quan.py`. Nếu luật cần số mới, đặt số đó trong
   `game.contract.json` rồi đọc qua `self.t` / `self.menu`.
3. Nếu thêm nguyên liệu HOÀN TOÀN mới (loài cá/rau mới): phải cập nhật danh sách hợp lệ
   `KINDS_P1` trong `chonoi/inventory.py` và `FISH_KINDS`/`NODE_KINDS` trong `chonoi/scenario.py`
   — đây là **đổi hợp đồng**, báo cả nhóm và ghi lý do (ADR/commit), vì ảnh hưởng mọi module.
4. Chạy kiểm tra:
   ```bash
   bash .agents/skills/verify-phase/scripts/verify.sh
   ```
   Viết thêm 1 test hộp đen cho món mới trong `tests/test_quan_rules.py` (khách gọi, nấu, phục vụ, trả tiền).
5. Giữ **tất định**: không RNG/đồng hồ; cùng seed phải cho output giống từng byte.

## Cạm bẫy
- Đổi `KINDS_P1` làm **mọi** file kho/scenario cũ có thể bị từ chối (mã 2) — chỉ làm khi cần.
- Giá quá cao có thể phá cân bằng điểm (`score = earned + 100×⌊uy tín⌋`); cân nhắc test cân bằng.
