# Ma trận truy vết Phase 1 (buổi sáng "Gather")

Chạy test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| Dưới nước oxy −1/tick; mặt nước hồi `oxygen_refill_per_tick`, kẹp trần | `test_gather_rules.Oxygen.test_duoi_nuoc_tru_oxy_mat_nuoc_hoi` | test xanh | ✅ Đạt |
| `oxygen_empty` đúng 1 lần khi oxy cạn | `...test_oxygen_empty_event_mot_lan` | test xanh | ✅ Đạt |
| Ngạt đủ 60 tick → `choke` (−Máu); Máu 0 → `faint`, `gather_end(fainted)`, kho rỗng | `...test_choke_tru_mau_va_faint_mat_gio` | test xanh | ✅ Đạt |
| `dive`/`surface` khi vượt mặt nước | `...test_dive_surface_events` | test xanh | ✅ Đạt |
| Hái nút ở mặt nước → `gather`, đặt mọc lại | `GatherCatch.test_hai_nut_o_mat_nuoc_va_regrow` | test xanh | ✅ Đạt |
| Không hái được khi dưới nước | `...test_khong_hai_duoc_duoi_nuoc` | test xanh | ✅ Đạt |
| Bắt cá dưới nước → `fish_caught`, yield đúng, cá biến mất | `...test_bat_ca_duoi_nuoc_yield_va_bien_mat` | test xanh | ✅ Đạt |
| Không bắt cá ở mặt nước | `...test_khong_bat_ca_o_mat_nuoc` | test xanh | ✅ Đạt |
| Giỏ đầy → `hold_full`, không hái | `...test_gio_day_hold_full` | test xanh | ✅ Đạt |
| Cập bến xuất kho; quán đọc đúng (Contract G) | smoke `Integration.test_inv_01_*` (khung, giữ xanh) | test xanh | ✅ Đạt |
| Cùng seed → giống từng byte | smoke `Contract.test_con_02_deterministic_bytes` | test xanh | ✅ Đạt |

## Đánh giá ngắn
- **Đạt:** toàn bộ luật gather lát 1 + lát 2; 32 smoke test khung + 9 test luật nhóm đều xanh.
- **Chưa đạt / rủi ro:** không có PRD board để đối chiếu hình dạng `data` sự kiện ẩn (xem `docs/clarify.md`).
- **Chỉnh cho phase sau:** sang buổi tối (`quan`) — khách, nấu, phục vụ, tiền, uy tín.
