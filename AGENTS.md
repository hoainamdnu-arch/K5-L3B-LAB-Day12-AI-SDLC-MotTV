# AGENTS.md — hướng dẫn chung cho mọi agent AI của nhóm

> Cập nhật file này qua các phase (lịch sử git phải cho thấy điều đó). Ngắn gọn, có lệnh chạy thật.

## Lệnh
- Test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`
- Headless: `python3 -m chonoi.headless --mode gather|quan --seed 1 --ticks 600 --out out.jsonl`
- Chơi thử trên trình duyệt: `python3 -m chonoi.live --mode gather|quan` (mở địa chỉ in ra; WASD, E, Space, R)

## Cấu trúc & quy ước
- (Starter Python là TÙY CHỌN; nhóm có thể dùng ngôn ngữ khác nếu giữ Test Contract.) Khung do giảng viên cấp: `chonoi/{headless,inputs,scenario,contract,rng,ids,jsonl,inventory,runner,live}.py` và `chonoi/web/`. Hạn chế sửa; nếu phải sửa thì báo cả nhóm và ghi lại lý do.
- Luật chơi của nhóm: `chonoi/sim/gather.py`, `chonoi/sim/quan.py` (tìm `TODO(nhóm)`).
- **Số liệu chỉ đọc từ `game.contract.json` / dữ liệu**, không hard-code trong luật.
- Mọi số ngẫu nhiên đi qua `Streams` (`chonoi/rng.py`); không dùng `random` toàn cục, không dùng đồng hồ hệ thống.
- Sắp danh sách thực thể bằng `ids.sort_by_id`; cấp id bằng `IdAllocator`.

## Nên tránh
- Không sửa `docs/contracts/`, `game.contract.json` (khóa contract) hoặc schema kho khi chưa báo cả nhóm (đổi hợp đồng ảnh hưởng mọi module).
- Không làm hỏng nhánh chính: trước khi đẩy, chạy test.
- Không bịa yêu cầu: chỗ mơ hồ thì ghi `docs/clarify.md` và hỏi PO.
- Không sửa test cho xanh khi luật sai; phải sửa luật hoặc ghi lý do đổi test trong commit.

## Quy tắc làm việc với agent
- Mỗi agent một việc rõ ràng (một lát). Cho agent đọc PRD/ticket đúng phase và hợp đồng kho trước.
- Agent làm xong phải chạy test và ghi kết quả vào mô tả commit hoặc `docs/proof/`; người đọc lại thay đổi trước khi đẩy.
- Sáng tạo thêm được khuyến khích nhưng phải tắt ở headless (xem README, mục "Tự do sáng tạo").

## Skills / hooks của nhóm
Đặt ở `.agents/skills/`. Nhóm MotTV tự viết:
- **`verify-phase`** (`.agents/skills/verify-phase/`): cổng kiểm **trước khi gắn tag** `phase-n` / release.
  Chạy `bash .agents/skills/verify-phase/scripts/verify.sh` → chạy Test Contract (headless + unit nhóm),
  kiểm `check_team`, kiểm `game.contract.json`, smoke CLI; chỉ gắn tag khi **tất cả xanh**.
- **`add-menu-dish`** (`.agents/skills/add-menu-dish/`): thêm món ăn mới **đúng quy ước** — chỉ sửa dữ liệu
  trong `game.contract.json`, không hard-code số trong luật; nhắc khi nào là "đổi hợp đồng" (thêm nguyên liệu mới).

## Tiến độ theo phase (cập nhật qua từng phase — lịch sử git cho thấy)
- **Phase 1:** luật `gather` (oxy/ngạt/choke/faint/giỏ, hái nút, bắt cá) + test. Tag `phase-1`.
- **Phase 2:** luật `quan` (vòng đời khách, nấu/phục vụ/tiền/boa/uy tín) + test. Tag `phase-2`.
- **Phase 3:** harness AI của nhóm (2 skill trên), đồ họa/HUD sáng tạo cho cửa sổ chơi thử (tắt ở headless). Tag `phase-3`.
- **Phase 4:** rà soát, retro, Release `v1.0.0`. Tag `phase-4`.
