# Ma trận truy vết Phase 3 (harness AI + sáng tạo)

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| ≥ 2 skill nhóm, chạy được | `bash .agents/skills/verify-phase/scripts/verify.sh` in "SẴN SÀNG"; `add-menu-dish/SKILL.md` | chạy tay OK | ✅ Đạt |
| AGENTS.md ghi skill + tiến độ phase | `AGENTS.md` mục "Skills / hooks của nhóm" + "Tiến độ theo phase" | đã cập nhật | ✅ Đạt |
| Sáng tạo tắt ở headless (không đổi hợp đồng) | HUD chỉ ở `chonoi/web/index.html`; 46 test headless vẫn xanh; `test_live` vẫn xanh (còn `<canvas>`) | test xanh | ✅ Đạt |
| Nhật ký AI theo phase/người | `docs/ai-usage-log.md` | đã cập nhật | ✅ Đạt |

## Đánh giá ngắn
- **Đạt:** harness AI (2 skill + AGENTS.md), đồ họa sáng tạo cho cửa sổ chơi thử, không phá lõi.
- **Chỉnh cho phase sau:** chốt release `v1.0.0`, retro, CHANGELOG.
