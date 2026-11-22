# Ma trận truy vết Phase 4 (hoàn thiện + release)

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| Tích hợp sáng → tối (Contract G) chạy thông | pipeline gather→kho→quan | `docs/proof/phase-4/demo.md`; smoke `Integration.test_inv_01_*` | ✅ Đạt |
| Toàn bộ test xanh ở tag cuối | `python3 -m unittest discover -s tests` | 46 pass | ✅ Đạt |
| Kiểm lại phase trước (hồi quy) | gather + quan + khung đều trong cùng suite | 46 pass | ✅ Đạt |
| CHANGELOG + Release v1.0.0 | `CHANGELOG.md`, tag `v1.0.0` | đã tạo | ✅ Đạt |
| Retro đầy đủ (gồm 1 lần AI sai) | `docs/retro.md` | đã viết | ✅ Đạt |
| CREDITS (không asset ngoài, ghi công cụ AI) | `CREDITS.md` | đã viết | ✅ Đạt |

## Tổng kết trung thực
- **Đạt lõi:** 4 phase gameplay đúng Test Contract công khai, tất định, tích hợp thông suốt.
- **Hạn chế:** bài **solo** (điểm teamwork hạn chế; `check_team` cảnh báo); `data` của test ẩn là suy luận
  do không truy cập được PRD board (xem `docs/clarify.md`, `docs/retro.md`).
