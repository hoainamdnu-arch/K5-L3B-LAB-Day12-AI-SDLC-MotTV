# Retro nhóm (MotTV — solo)

## Phase 2 (nhanh)
- **Điều tốt:** làm cả vòng đời khách + phục vụ trong một lượt thiết kế mạch lạc; test hộp đen bắt lỗi sớm.
- **Điều tệ:** thiếu PRD board nên phải suy nhiều giả định (ghép món, chọn món, boa) — rủi ro lệch test ẩn.
- **1 hành động cho Phase 3:** ghi mọi giả định vào `docs/clarify.md` và giữ tên sự kiện khớp `docs/contracts/README.md`.

## Phase 4 (cuối)
- **Rà lại hành động Phase 2:** đã làm — `docs/clarify.md` liệt kê 9 giả định; tên sự kiện gather/quan khớp hợp đồng.
- **Điều tốt:** lõi đúng trước (46 test xanh, tất định từng byte); harness AI gọn (2 skill dùng được thật);
  tích hợp sáng→tối chạy thông (Contract G).
- **Điều tệ:** là bài **solo** nên điểm "làm việc nhóm" (chia việc, nhiều người commit, đổi yêu cầu giữa người)
  không thể hiện được; `check_team` cảnh báo số thành viên.
- **Số liệu:** commit theo người — chỉ `hoainamdnu-arch` (solo, 4 commit theo phase + 1 release).
  Token theo người: xem `docs/ai-usage-log.md`. Đọc code: tự review diff trước mỗi commit.
- **Một lần AI sai và cách phát hiện:** AI để `headless_cmd = python3` nhưng Windows chỉ có `python`
  (test thoát mã 9009) → lập shim `python3.exe`, **không** sửa hợp đồng để grader Linux vẫn đúng.
  Lần khác: HUD starter đọc sai tên trường khách (`dish_id`) → sửa web cho khớp luật (`order`).
- **Nếu làm lại, đổi gì:** rủ thêm người để đạt phần teamwork; chốt hợp đồng sự kiện (`data`) sớm hơn;
  thêm test cân bằng điểm khi mở rộng menu.

## Hạn chế đã biết (trung thực)
- Không truy cập được PRD board → một số hình dạng `data` sự kiện ẩn là **suy luận**; nếu test ẩn kỳ vọng
  khác, cần chỉnh theo thông báo test (tên sự kiện đã giữ khớp hợp đồng để giảm rủi ro).
- Yêu cầu 4–6 thành viên không thể đáp ứng (solo) — đã ghi rõ ở `TEAM.md`.
