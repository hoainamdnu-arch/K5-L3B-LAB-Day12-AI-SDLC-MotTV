# hoainamdnu-arch — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm:** nhóm solo MotTV, tự làm toàn bộ — luật `sim/gather.py` (oxy/ngạt/choke/faint/giỏ,
  hái nút, bắt cá, cập bến) và `sim/quan.py` (khách, nấu, phục vụ, tiền, uy tín), test luật
  (`tests/test_gather_rules.py`, `tests/test_quan_rules.py`), skill/hook nhóm, và toàn bộ tài liệu.
- **Tôi đã review:** tự đọc lại diff trước mỗi commit; chạy `unittest discover` trước mỗi tag `phase-n`.
- **AI sai ở đâu và tôi phát hiện thế nào:** xem `docs/ai-usage-log.md`. Đáng nhớ nhất: AI ban đầu định
  cho `python3` nhưng máy Windows chỉ có `python`; phát hiện khi test thoát mã 9009 → lập shim `python3.exe`.
- **Điều tôi học được:** khi không có PRD gốc, Test Contract + các khối `TODO` là nguồn sự thật đủ chặt để
  dựng luật tất định; ghi rõ giả định (`docs/clarify.md`) quan trọng ngang code.
