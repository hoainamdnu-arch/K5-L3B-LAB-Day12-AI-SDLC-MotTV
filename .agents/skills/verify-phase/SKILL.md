---
name: verify-phase
description: Chạy trước khi gắn tag phase-n. Chạy toàn bộ Test Contract (headless + unit nhóm), kiểm danh sách thành viên, và in bản tóm tắt "sẵn sàng gắn tag chưa". Dùng khi người dùng nói "kiểm tra trước khi tag", "verify phase", "chuẩn bị release", hoặc sắp chạy `git tag phase-n`.
---

# verify-phase — cổng kiểm trước khi gắn tag

Nhóm MotTV dùng skill này làm **cổng chất lượng** trước mỗi `git tag phase-n` và trước release.
Mục tiêu: nhánh chính luôn **chạy được tại tag** (yêu cầu bắt buộc của lab).

## Khi nào dùng
- Ngay trước khi gắn `phase-1` … `phase-4` hoặc tạo Release `v1.0.0`.
- Sau khi tích hợp một thay đổi lớn vào `main`.

## Các bước
1. Chạy script tổng hợp:
   ```bash
   bash .agents/skills/verify-phase/scripts/verify.sh
   ```
   Script sẽ:
   - Chạy `PYTHONPATH=tests:. python3 -m unittest discover -s tests` (Test Contract hộp đen + unit nhóm).
   - Chạy `python3 tools/check_team.py` (cảnh báo danh sách thành viên — không chặn).
   - Kiểm `game.contract.json` đọc được và có `headless_cmd`, `build_cmd`.
   - Chạy nhanh headless gather + quan `--ticks 0` để chắc CLI không vỡ.
2. Nếu **tất cả test xanh** → báo "SẴN SÀNG gắn tag", nhắc cập nhật `docs/verification/phase-n.md`.
3. Nếu có test đỏ → **không gắn tag**; ghi trung thực chỗ chưa xong vào `docs/verification/phase-n.md`
   (lab chấm trung thực, không chấm "giả xanh").

## Lưu ý Windows
Máy chỉ có `python` (không có `python3`): tạo shim `python3.exe` trỏ tới `python`, hoặc chạy script bằng
`python` rồi vẫn giữ `headless_cmd = python3 ...` để grader Linux chạy đúng.
