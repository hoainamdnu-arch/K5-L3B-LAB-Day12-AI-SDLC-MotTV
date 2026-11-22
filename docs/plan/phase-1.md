# Kế hoạch Phase 1 (≤ 1 trang) — PRD-0, buổi sáng "Gather"

- **Mục tiêu:** Út Sen lặn bắt cá & hái rau trên mặt nước; vòng lặp sáng chạy đúng Test Contract và
  xuất kho cho buổi tối. Làm **lõi đúng trước**.
- **Việc / người / phụ thuộc** (solo — MotTV tự làm hết):
  - Lát 1: oxy (dưới nước trừ / mặt nước hồi), `oxygen_empty`, ngạt → `choke` (−Máu), `faint` (mất giỏ),
    `dive`/`surface`, giỏ LIFO + sức chứa. → `chonoi/sim/gather.py`.
  - Lát 2: hái nút (`gather`, `hold_full`, mọc lại), bắt cá (`fish_caught`, hồi chiêu, chỉ dưới nước),
    cập bến (có sẵn), xuất kho. → `chonoi/sim/gather.py`.
  - Test luật: `tests/test_gather_rules.py` (hộp đen).
- **Rủi ro:**
  - Không đọc được PRD board → số liệu/sự kiện suy từ TODO + Test Contract (xem `docs/clarify.md`).
  - Hình dạng `data` của sự kiện ẩn có thể khác → giữ tên sự kiện khớp `docs/contracts/README.md`,
    `data` tối giản và nhất quán.
  - Determinism: không RNG, không đồng hồ hệ thống → cùng seed giống từng byte (test `con_02`).
