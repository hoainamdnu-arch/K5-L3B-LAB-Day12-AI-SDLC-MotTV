# Changelog

## v1.0.0 — 2026-11-22
Bản hoàn chỉnh 4 phase của nhóm **MotTV** (solo).

### Buổi sáng — Lặn & Hái (`gather`)
- Oxy: dưới nước −1/tick, mặt nước hồi `oxygen_refill_per_tick`, kẹp trần; `oxygen_empty` khi cạn.
- Ngạt → `choke` (−Máu) sau `choke_interval_ticks`; Máu 0 → `faint`, `gather_end(fainted)`, mất giỏ.
- `dive`/`surface`; hái nút `ready` ở mặt nước (`gather`, mọc lại), bắt cá dưới nước (`fish_caught`, hồi chiêu),
  `hold_full` khi giỏ đầy; cập bến xuất kho (Contract G).

### Buổi tối — Mở Quán (`quan`)
- Khách đến theo lịch, chọn món giá cao nấu được, giữ chỗ nguyên liệu; kiên nhẫn; `customer_left` (−uy tín),
  `no_dish` khi không nấu được.
- Nấu/bưng/phục vụ: `cook_started`/`dish_ready`/`dish_picked`/`served`/`paid`; boa khi kiên nhẫn đủ;
  uy tín kẹp `[0,5]`; `quan_end` hết ca. Điểm = `earned + 100×⌊uy tín⌋`.

### Harness AI & sáng tạo
- 2 skill nhóm: `verify-phase`, `add-menu-dish` (`.agents/skills/`).
- HUD "Chợ Nổi về đêm" cho cửa sổ chơi thử (sao uy tín, đơn món + kiên nhẫn khách) — tắt ở headless.

### Kiểm thử
- 46 test hộp đen + unit đều xanh; tất định cùng seed (giống từng byte).

## Unreleased
