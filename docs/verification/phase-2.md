# Ma trận truy vết Phase 2 (buổi tối "Quán")

Chạy test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| Khách đến đúng `first_customer_tick`, chọn món nấu được, giữ chỗ nguyên liệu | `test_quan_rules.Customers.test_khach_den_theo_lich_va_giu_cho` | test xanh | ✅ Đạt |
| Kho rỗng → `no_dish`, không có khách ngồi | `...test_no_dish_khi_kho_rong` | test xanh | ✅ Đạt |
| Hết kiên nhẫn → `customer_left`, −uy tín, trả lại nguyên liệu | `...test_customer_left_tru_uy_tin_va_tra_lai_nguyen_lieu` | test xanh | ✅ Đạt |
| Nấu→bưng→phục vụ→trả tiền: `cook_started`/`dish_ready`/`dish_picked`/`served`/`paid`, boa + uy tín | `Serving.test_nau_phuc_vu_tra_tien_co_boa` | test xanh | ✅ Đạt |
| Phục vụ sai món thì không được | `...test_phuc_vu_sai_mon_khong_duoc` | test xanh | ✅ Đạt |
| Fixture quán sai (pos ngoài biên, thiếu/khớp bàn) → mã 2 | smoke `ScenarioModes.test_quan_fixture_khong_hop_le_exit_2` | test xanh | ✅ Đạt |
| `quan_end` khi hết ca; score = earned + 100×⌊uy tín⌋ | runner + `Serving` (end row) | test xanh | ✅ Đạt |

## Đánh giá ngắn
- **Đạt:** toàn bộ vòng đời khách + phục vụ + tiền/boa/uy tín. 46 test đều xanh (32 khung + 9 gather + 5 quan).
- **Giả định (thiếu PRD):** ghép món theo tên tại đúng bàn; chọn món giá cao; no_dish không trừ uy tín (xem `docs/clarify.md`).
- **Chỉnh cho phase sau:** thêm sáng tạo nhóm + kiểm tra bền (robustness) + release.
