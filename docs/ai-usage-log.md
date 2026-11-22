# Nhật ký dùng AI (theo phase và theo người)

> Nhóm MotTV dùng **Claude Code (model Claude Opus 4.8)** làm cặp lập trình cho toàn bộ bài lab.

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| 1 | hoainamdnu-arch | Claude Code (Opus 4.8) | Đọc khung, viết luật gather lát 1+2, test gather | ~vài chục K token | Định dùng `python3` nhưng Windows chỉ có `python` (thoát 9009) → tự lập shim `python3.exe`; không sửa `headless_cmd` để grader Linux vẫn chạy. |
| 1 | hoainamdnu-arch | Claude Code (Opus 4.8) | Thử truy cập PRD board | — | Không vào được artifact (cần đăng nhập account khác) → chuyển sang suy luật từ Test Contract + TODO, ghi giả định ở `docs/clarify.md`. |
| 2 | hoainamdnu-arch | Claude Code (Opus 4.8) | Luật quán lát 3+4 (khách, giữ chỗ, kiên nhẫn, bỏ đi, nấu/bưng/phục vụ/tiền/boa/uy tín) + test | ~vài chục K token | AI ban đầu định cho cá bị bắt "ở lại" → review thấy sẽ farm vô hạn, chốt cho cá biến mất; ghi giả định vào clarify #5. |
| 3 | hoainamdnu-arch | Claude Code (Opus 4.8) | 2 skill harness (verify-phase, add-menu-dish), HUD sáng tạo, AGENTS.md | ~vài chục K token | Phát hiện HUD starter đọc sai tên trường (`dish_id`/`patience_ticks_left`) khác luật nhóm (`order`/`patience_ticks`) → sửa web cho khớp. |
| 4 | hoainamdnu-arch | Claude Code (Opus 4.8) | Rà soát, retro, CHANGELOG, Release v1.0.0 | ~vài chục K token | (điền khi làm) |

## Cách kiểm chứng đầu ra của AI
- Mọi luật kèm test hộp đen chạy qua `headless_cmd` (đúng Test Contract).
- Chạy lại `unittest discover` trước mỗi commit/tag; xác nhận cùng seed → giống từng byte.
- Giả định (khi thiếu PRD) ghi ở `docs/clarify.md` để người đọc đối chiếu.
