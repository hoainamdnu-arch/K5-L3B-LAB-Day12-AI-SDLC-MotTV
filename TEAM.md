# TEAM

**Tên nhóm:** MotTV  **Số người:** 1  (khớp `team_size` trong `game.contract.json`)

> **Ghi chú trung thực:** nhóm **MotTV làm một mình** (1 thành viên), tự đảm nhiệm **tất cả** vai
> (PO, Integrator, QA lead, Scrum/Release) và tất cả module. Vì vậy bảng dưới có 1 dòng thay vì 4–6;
> `tools/check_team.py` sẽ **cảnh báo** về số lượng (CI chỉ cảnh báo, không chặn) — đây là điều đã biết
> và chấp nhận cho bài nộp solo.

| Thành viên | GitHub handle | Module chính | Vai quy trình | Người dự phòng cho |
|---|---|---|---|---|
| Hoài Nam | hoainamdnu-arch | `sim/gather` + `sim/quan` + `qa` | PO · Integrator · QA · Scrum/Release | — (solo) |

**Vai quy trình:** PO (đầu mối hỏi giảng viên, giữ `docs/clarify.md`) · Integrator (giữ `docs/contracts/`, gắn tag) · QA lead · Scrum/Release. Một người kiêm hết.

## Thỏa thuận làm việc (solo — tự quản)

- Kênh liên lạc: tự ghi chú trong `docs/standup.md`.
- Khi bất đồng về thiết kế: ghi lựa chọn + lý do vào `docs/clarify.md` rồi đi tiếp (không ai để tranh luận).
- Khi vướng quá 10 phút: ghi rõ chỗ kẹt trong `docs/clarify.md`, chọn giả định an toàn nhất, ghi lại.
- Standup giữa phase: tự điểm lại todo + chạy test trước khi gắn tag.
- Đọc lại code: tự review diff trước khi commit; mọi commit kèm kết quả test.
- Git: push thẳng nhánh `main`, chạy test trước khi gắn tag `phase-n`.
