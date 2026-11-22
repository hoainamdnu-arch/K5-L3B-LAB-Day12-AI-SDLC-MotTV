"""Test luật QUÁN do nhóm MotTV viết (lát 3: khách/giữ chỗ/kiên nhẫn/bỏ đi/no_dish;
lát 4: nấu/bưng/phục vụ/trả tiền/boa/uy tín). Kiểu HỘP ĐEN qua headless_cmd.

Chạy: PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
"""

import json
import unittest

from helpers import Workdir, events, read_jsonl, run_headless, snapshots, write_json


def frames(*fr):
    return {"frames": list(fr)}


def last_snap(w):
    return snapshots(read_jsonl(w))[-1]


class Customers(unittest.TestCase):
    def test_khach_den_theo_lich_va_giu_cho(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"quan": {"stock": {"bong_sung": 2}}})
            code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "121", "--scenario", sc,
                                     "--snapshot-every", "1", "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            rows = read_jsonl(w.path("o.jsonl"))
            ev = events(rows, "customer_arrived")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["tick"], 120)  # first_customer_tick
            self.assertEqual(ev[0]["data"]["order"], "goi_bong_sung")
            # giữ chỗ: kho bong_sung đã bị trừ 2 -> không còn trong stock (>0)
            self.assertNotIn("bong_sung", last_snap(w.path("o.jsonl"))["stock"])

    def test_no_dish_khi_kho_rong(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"quan": {"stock": {}}})
            run_headless("--mode", "quan", "--seed", "1", "--ticks", "121", "--scenario", sc, "--out", w.path("o.jsonl"))
            rows = read_jsonl(w.path("o.jsonl"))
            self.assertEqual(len(events(rows, "no_dish")), 1)
            self.assertEqual(len(events(rows, "customer_arrived")), 0)

    def test_customer_left_tru_uy_tin_va_tra_lai_nguyen_lieu(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"quan": {
                "stock": {"bong_sung": 2}, "random_customers": False,
                "customers": [{"id": "C1", "table_id": "T1", "order": "goi_bong_sung", "patience_ticks": 3}]}})
            run_headless("--mode", "quan", "--seed", "1", "--ticks", "10", "--scenario", sc,
                         "--snapshot-every", "1", "--out", w.path("o.jsonl"))
            rows = read_jsonl(w.path("o.jsonl"))
            ev = events(rows, "customer_left")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["tick"], 3)
            self.assertAlmostEqual(ev[0]["data"]["reputation"], 3.0 - 0.5)  # left_reputation_delta
            last = last_snap(w.path("o.jsonl"))
            self.assertEqual(last["stock"].get("bong_sung"), 2)  # nguyên liệu trả lại kho
            self.assertEqual(last["customers"], [])


class Serving(unittest.TestCase):
    def test_nau_phuc_vu_tra_tien_co_boa(self):
        with Workdir() as w:
            # bếp & bàn đặt tiện cho test; khách dựng sẵn kiên nhẫn đầy -> được boa
            sc = write_json(w.path("sc.json"), {"quan": {
                "stock": {"bong_sung": 2}, "random_customers": False,
                "player": {"pos": [5, 5]},
                "stoves": [{"id": "B1", "pos": [5, 5]}], "tables": [{"id": "T1", "pos": [12, 5]}],
                "customers": [{"id": "C1", "table_id": "T1", "order": "goi_bong_sung"}]}})
            inp = write_json(w.path("in.json"), frames(
                {"tick": 0, "interact": True},                 # cook_started tại bếp
                {"tick": 1, "interact": False, "move": [1, 0]},  # (giữ chỗ chờ chín)... thực ra đứng yên nấu
                {"tick": 2, "move": [0, 0]},
                {"tick": 240, "interact": True},               # dish_ready + dish_picked
                {"tick": 241, "interact": False, "move": [1, 0]},  # đi tới bàn T1
                {"tick": 360, "move": [0, 0]},
                {"tick": 362, "interact": True},               # served
                {"tick": 363, "interact": False}))
            code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "1000", "--scenario", sc,
                                     "--inputs", inp, "--snapshot-every", "30", "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            rows = read_jsonl(w.path("o.jsonl"))
            for name in ("cook_started", "dish_ready", "dish_picked", "served", "paid"):
                self.assertEqual(len(events(rows, name)), 1, name)
            paid = events(rows, "paid")[0]["data"]
            self.assertEqual(paid["dish"], "goi_bong_sung")
            self.assertEqual(paid["tip"], 8)       # round(0.2 * 40)
            self.assertEqual(paid["amount"], 48)   # 40 + 8
            end = [r for r in rows if r["type"] == "end"][-1]
            self.assertEqual(end["earned"], 48)
            self.assertAlmostEqual(end["reputation"], 3.0 + 0.2)  # tip_reputation

    def test_phuc_vu_sai_mon_khong_duoc(self):
        with Workdir() as w:  # cầm sẵn món khác với đơn của khách -> không phục vụ
            sc = write_json(w.path("sc.json"), {"quan": {
                "stock": {}, "random_customers": False, "hand": "ca_loc_nuong_trui",
                "player": {"pos": [12, 5]}, "tables": [{"id": "T1", "pos": [12, 5]}],
                "customers": [{"id": "C1", "table_id": "T1", "order": "goi_bong_sung", "reserved": {"bong_sung": 2}}]}})
            inp = write_json(w.path("in.json"), frames({"tick": 0, "interact": True}))
            run_headless("--mode", "quan", "--seed", "1", "--ticks", "5", "--scenario", sc,
                         "--inputs", inp, "--out", w.path("o.jsonl"))
            self.assertEqual(len(events(read_jsonl(w.path("o.jsonl")), "served")), 0)


if __name__ == "__main__":
    unittest.main()
