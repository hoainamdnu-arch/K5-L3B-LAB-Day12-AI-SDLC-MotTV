# Clarify — câu hỏi và câu trả lời (PO ghi, cả nhóm dùng chung)

> Nhóm solo MotTV **không truy cập được lab board PRD** (artifact claude.ai cần đăng nhập account khác).
> Vì vậy luật được suy ra **chặt chẽ từ**: (a) các khối `TODO(nhóm)` trong `chonoi/sim/*.py`,
> (b) Test Contract công khai `tests/test_smoke_p1.py`, (c) số liệu trong `game.contract.json`,
> (d) danh sách sự kiện trong `docs/contracts/README.md`. Mọi giả định ghi bên dưới.

| # | Ngày giờ | Câu hỏi | Trả lời / giả định | Ai quyết |
|---|---|---|---|---|
| 1 | 2026-11-22 | `oxygen_empty` phát khi nào? | Khi oxy **từ dương xuống 0** ở cuối bước, và đúng **một lần** cho mỗi lần cạn. | PO (solo) |
| 2 | 2026-11-22 | Đếm ngạt bắt đầu từ tick nào? | Ngay tick oxy = 0 và đang dưới nước: `zero_oxy_ticks += 1`; đủ `choke_interval_ticks` (60) → `choke` (−1 Máu) rồi reset về 0. Khớp ràng buộc scenario `zero_oxy_ticks ∈ [0,59]`. | PO |
| 3 | 2026-11-22 | Ngất (`faint`) thì giỏ ra sao? | Mất **toàn bộ** giỏ (`hold = []`), `gather_end` reason `fainted`, kho rỗng. | PO |
| 4 | 2026-11-22 | Hái nút cần điều kiện gì? | Chỉ khi **ở mặt nước**, nút `ready` (regrow = 0) **gần nhất** trong `interact_radius`, id nhỏ khi bằng khoảng cách; thêm `node_yield` item, đặt `regrow_ticks = regrow_s×60`. Xét **sau** cập bến. | PO |
| 5 | 2026-11-22 | Bắt cá cần điều kiện gì? | Chỉ khi `catch_cd_ticks == 0` và **đang dưới nước**; cá gần nhất trong `catch_radius` (id nhỏ khi bằng); thêm `fish_yield[kind]` item; **cá biến mất** sau khi bắt; đặt hồi chiêu `catch_cooldown_s×60`. | PO |
| 6 | 2026-11-22 | Giỏ đầy thì sao? | Phát `hold_full` (kèm id đối tượng), **không** hái/bắt, nút/cá giữ nguyên. Nếu còn chỗ nhưng không đủ cho cả yield thì nhận tối đa tới `hold_capacity`. | PO |
| 7 | 2026-11-22 | Quán: khách chọn món thế nào? | Khi tới lượt, khách chọn món **nấu được bằng kho hiện có** (giữ chỗ nguyên liệu); ưu tiên món **giá cao nhất**, hoà thì theo thứ tự khoá menu. Không món nào nấu được → `no_dish`, khách bỏ đi. | PO |
| 8 | 2026-11-22 | Quán: thứ tự xử lý khi `interact`? | Tối đa **một** interact/tick, chọn đối tượng theo (khoảng cách ≤ `interact_radius`, **bếp trước bàn**, id nhỏ). | PO |
| 9 | 2026-11-22 | Boa & uy tín tính sao? | Khách phục vụ khi còn ≥ `tip_min_patience_ratio` kiên nhẫn → boa `tip_rate×giá`, +`tip_reputation` uy tín. Khách bỏ đi vì hết kiên nhẫn → `left_reputation_delta` uy tín. Kẹp `[reputation_min, reputation_max]`. | PO |

## Mâu thuẫn scenario → mã 2 (bổ sung ở `scenario.py` nếu cần)
Khung đã kiểm phần lớn; nhóm giữ nguyên hành vi khung và chỉ thêm kiểm mức-luật khi test đòi.
