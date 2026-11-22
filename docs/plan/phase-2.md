# Kế hoạch Phase 2 (≤ 1 trang) — buổi tối "Quán"

- **Mục tiêu:** mở quán buổi tối chạy đủ vòng đời khách: đến → gọi món (giữ chỗ nguyên liệu) →
  nấu → bưng → phục vụ → ăn → trả tiền + boa + uy tín; khách hết kiên nhẫn thì bỏ đi.
- **Việc (solo — MotTV):** `chonoi/sim/quan.py`
  - Lát 3: lịch khách (`first_customer_tick`, `customer_interval_s`), chọn món giá cao nấu được,
    giữ chỗ (`reserved`), kiên nhẫn, `customer_left` (−uy tín, trả lại kho), `no_dish`.
  - Lát 4: interact 1 đối tượng (bếp trước bàn, id nhỏ) → `cook_started`/`dish_ready`/`dish_picked`/
    `served`/`paid`; boa khi kiên nhẫn ≥ `tip_min_patience_ratio`; `quan_end` hết ca.
  - Test: `tests/test_quan_rules.py`.
- **Rủi ro & giả định:** cơ chế ghép món khi phục vụ theo **tên món tại đúng bàn**; chọn món nấu
  ưu tiên **giá cao** (xem `docs/clarify.md` #7–#9). Không có PRD gốc để đối chiếu `data` sự kiện ẩn.
- **Determinism:** không RNG/đồng hồ; lịch khách theo `elapsed` tick → tất định.
