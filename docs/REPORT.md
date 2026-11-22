# Báo cáo dự án — Quán Ăn Chợ Nổi

| | |
|---|---|
| Nhóm | MotTV |
| Thành viên | 1 (`hoainamdnu-arch`), kiêm toàn bộ vai: PO, Integrator, QA, Release |
| Phiên bản | v1.0.0 (2026-11-22) |
| Ngôn ngữ / runtime | Python 3 (thư viện chuẩn), chạy headless + cửa sổ trình duyệt |
| Trạng thái kiểm thử | 46/46 test tự động xanh, output tất định cùng seed |

## Phạm vi đã giao# TECHNICAL REPORTING GUIDELINES
- **Audience:** Write strictly for the final reader (evaluators, stakeholders). Treat the output as a production-ready deliverable, never as an AI assistant's response to a user.
- **No Meta-Commentary:** Output ONLY the document content. Omit conversational fillers, preambles, closing remarks, or internal tool/CI warnings (e.g., do not mention linter warnings, script behaviors, or template mismatches).
- **Natural Adaptation:** Silently adapt the report structure to fit the actual project data (e.g., solo contributor vs. team) using confident, professional phrasing. Never include "honesty notes", apologies, or self-justifications for missing fields or scale differences.
- **Style:** Be concise, objective, and concrete. Prefer data, metrics, and bullet points over descriptive prose. Avoid AI clichés ("It is worth noting", "crucial", "delve", excessive em-dashes `—`) and omit "Summary/Conclusion" headers unless explicitly requested.

### Buổi sáng — `gather` (lặn & hái)
- Oxy: dưới nước `-1/tick`, mặt nước hồi `oxygen_refill_per_tick`, kẹp `[0, oxygen_max]`.
- Sự kiện sinh tồn: `oxygen_empty` (cạn oxy), `choke` (`-1` Máu sau `choke_interval_ticks` ngạt), `faint` (Máu `0` → `gather_end(fainted)`, mất toàn bộ giỏ).
- Vận động & vị trí: `dive`/`surface` theo mặt nước; giỏ LIFO giới hạn `hold_capacity`.
- Thu hoạch: hái nút `ready` ở mặt nước (`gather`, đặt `regrow_ticks`), bắt cá dưới nước (`fish_caught`, yield theo loài, hồi chiêu `catch_cooldown`, cá biến mất sau khi bắt), `hold_full` khi giỏ đầy.
- Kết nối: cập bến (`gather_end(docked)`) ghi file kho theo Contract G.

### Buổi tối — `quan` (mở quán)
- Khách: đến theo lịch (`first_customer_tick`, `customer_interval_s`), chọn món giá cao nấu được từ kho, giữ chỗ nguyên liệu (`reserved`).
- Kiên nhẫn: đếm ngược `patience_s`; hết → `customer_left` (`left_reputation_delta` uy tín, trả nguyên liệu về kho). Không món nào nấu được → `no_dish`.
- Phục vụ: một `interact`/tick (bếp trước bàn, id nhỏ) → `cook_started` → `dish_ready` → `dish_picked` → `served` → `paid`.
- Kinh tế: boa `tip_rate × giá` khi kiên nhẫn còn `≥ tip_min_patience_ratio`, cộng `tip_reputation`; uy tín kẹp `[reputation_min, reputation_max]`; điểm `= earned + 100 × ⌊uy tín⌋`; `quan_end` khi hết ca.

## Kết quả kiểm thử

| Bộ test | Số test | Kết quả |
|---|---|---|
| Khung hộp đen (Test Contract công khai) | 32 | PASS |
| Luật gather (nhóm viết) | 9 | PASS |
| Luật quán (nhóm viết) | 5 | PASS |
| **Tổng** | **46** | **PASS** |

- Tất định: cùng seed cho output giống từng byte (`test_con_02_deterministic_bytes`).
- Hồi quy: suite chạy lại toàn bộ gather + quan + khung ở mọi tag.
- Tích hợp sáng → tối: pipeline `gather → kho.json → quan` nạp đúng kho (`docs/proof/phase-4/demo.md`).

Lệnh kiểm chứng:
```bash
PYTHONPATH=tests:. python3 -m unittest discover -s tests
bash .agents/skills/verify-phase/scripts/verify.sh
```

## Lịch sử phase

| Tag | Nội dung | Trạng thái |
|---|---|---|
| `phase-1` | Luật gather + thiết lập nhóm | Chạy được, test xanh |
| `phase-2` | Luật quán (vòng đời khách + phục vụ) | Chạy được, test xanh |
| `phase-3` | Harness AI (2 skill) + HUD sáng tạo | Chạy được, test xanh |
| `phase-4` | Hoàn thiện + tài liệu | Chạy được, test xanh |
| `v1.0.0` | Release | Annotated tag |

## Harness AI

| Skill | Mục đích |
|---|---|
| `verify-phase` | Cổng chất lượng trước khi gắn tag: chạy Test Contract, `check_team`, smoke CLI; chỉ cho tag khi toàn bộ xanh. Có `scripts/verify.sh`. |
| `add-menu-dish` | Quy trình thêm món chỉ qua `game.contract.json` (không hard-code số trong luật); cảnh báo khi là "đổi hợp đồng". |

Công cụ: Claude Code (model Claude Opus 4.8). Nhật ký theo phase: `docs/ai-usage-log.md`.

## Mở rộng sáng tạo

HUD "Chợ Nổi về đêm" cho cửa sổ chơi thử (`chonoi/web/index.html`): xếp hạng sao uy tín, hiển thị đơn món và thanh kiên nhẫn từng khách, biểu tượng khách đang ăn, nhãn quán. Thuần đồ họa trình duyệt, không ảnh hưởng đường headless nên hợp đồng kiểm thử giữ nguyên.

## Quyết định thiết kế

| Hạng mục | Quyết định |
|---|---|
| Chọn mục tiêu hái/bắt | Đối tượng gần nhất trong bán kính, id nhỏ khi hoà khoảng cách |
| Cá sau khi bắt | Biến mất (tránh farm vô hạn khi cá đứng yên ở phase này) |
| Khách chọn món | Món nấu được có giá cao nhất; hoà theo thứ tự khoá menu |
| Ghép món khi phục vụ | Theo tên món tại đúng bàn khách gọi |
| Boa | Chỉ khi kiên nhẫn còn `≥ tip_min_patience_ratio` lúc dọn món |
| Hạch toán kho | `stock` lưu phần chưa giữ chỗ; đặt món trừ kho vào `reserved`, bỏ đi hoàn kho, bắt đầu nấu thì tiêu thụ |

Toàn bộ số liệu đọc từ `game.contract.json`; mọi ngẫu nhiên đi qua `Streams` (không dùng đồng hồ hệ thống).

## Tài liệu kèm theo
`TEAM.md`, `docs/clarify.md`, `docs/ai-usage-log.md`, `docs/retro.md`, `docs/verification/phase-1..4.md`, `docs/plan/*`, `docs/proof/phase-4/`, `CHANGELOG.md`, `CREDITS.md`.
