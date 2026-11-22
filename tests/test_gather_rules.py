"""Test luật GATHER do nhóm MotTV viết (lát 1: oxy/ngạt/choke/faint/giỏ; lát 2: hái/bắt cá/cập bến).

Kiểu HỘP ĐEN: chỉ chạy `headless_cmd` rồi đọc JSONL — dùng được với mọi ngôn ngữ giữ Test Contract.
Chạy: PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
"""

import json
import unittest

from helpers import Workdir, events, read_jsonl, run_headless, snapshots, write_json


def tuning_gather():
    with open("game.contract.json", encoding="utf-8") as f:
        return json.load(f)["tuning"]["gather"]


def frames(*fr):
    return {"frames": list(fr)}


class Oxygen(unittest.TestCase):
    def test_duoi_nuoc_tru_oxy_mat_nuoc_hoi(self):
        g = tuning_gather()
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [50, 10], "oxygen_ticks": 100}}})
            code, err = run_headless("--mode", "gather", "--seed", "1", "--ticks", "10", "--scenario", sc,
                                     "--snapshot-every", "1", "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            s = {r["tick"]: r for r in snapshots(read_jsonl(w.path("o.jsonl")))}
            self.assertEqual(s[10]["player"]["oxygen_ticks"], 90)  # dưới nước: -1/tick
        with Workdir() as w:  # ở mặt nước: hồi oxygen_refill_per_tick, kẹp trần
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [50, 0], "oxygen_ticks": 100}}})
            run_headless("--mode", "gather", "--seed", "1", "--ticks", "5", "--scenario", sc,
                         "--snapshot-every", "1", "--out", w.path("o.jsonl"))
            s = {r["tick"]: r for r in snapshots(read_jsonl(w.path("o.jsonl")))}
            self.assertEqual(s[5]["player"]["oxygen_ticks"], 100 + 5 * g["oxygen_refill_per_tick"])

    def test_oxygen_empty_event_mot_lan(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [50, 10], "oxygen_ticks": 3}}})
            run_headless("--mode", "gather", "--seed", "1", "--ticks", "10", "--scenario", sc, "--out", w.path("o.jsonl"))
            ev = events(read_jsonl(w.path("o.jsonl")), "oxygen_empty")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["tick"], 3)

    def test_choke_tru_mau_va_faint_mat_gio(self):
        g = tuning_gather()
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [50, 10], "oxygen_ticks": 0, "hp": 1},
                                                           "hold": ["ca_loc"]}})
            inv = w.path("inv.json")
            code, err = run_headless("--mode", "gather", "--seed", "1", "--ticks", str(g["choke_interval_ticks"] + 5),
                                     "--scenario", sc, "--inventory-out", inv, "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            rows = read_jsonl(w.path("o.jsonl"))
            self.assertEqual(len(events(rows, "choke")), 1)
            self.assertEqual(len(events(rows, "faint")), 1)
            end = events(rows, "gather_end")[0]["data"]
            self.assertEqual(end["reason"], "fainted")
            self.assertEqual(end["inventory"], {"items": {}})  # ngất -> giỏ rỗng
            with open(inv, encoding="utf-8") as f:
                self.assertEqual(json.load(f), {"items": {}})

    def test_dive_surface_events(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [50, 0]}}})
            inp = write_json(w.path("in.json"), frames({"tick": 0, "move": [0, 1]}, {"tick": 40, "move": [0, -1]}))
            run_headless("--mode", "gather", "--seed", "1", "--ticks", "120", "--scenario", sc,
                         "--inputs", inp, "--out", w.path("o.jsonl"))
            rows = read_jsonl(w.path("o.jsonl"))
            self.assertGreaterEqual(len(events(rows, "dive")), 1)
            self.assertGreaterEqual(len(events(rows, "surface")), 1)


class GatherCatch(unittest.TestCase):
    def test_hai_nut_o_mat_nuoc_va_regrow(self):
        g = tuning_gather()
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [12, 0]}}})
            inp = write_json(w.path("in.json"), frames({"tick": 1, "interact": True}))
            run_headless("--mode", "gather", "--seed", "1", "--ticks", "3", "--scenario", sc,
                         "--inputs", inp, "--snapshot-every", "1", "--out", w.path("o.jsonl"))
            rows = read_jsonl(w.path("o.jsonl"))
            ev = events(rows, "gather")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["data"]["node_id"], "N1")
            self.assertEqual(ev[0]["data"]["kind"], "bong_dien_dien")
            last = snapshots(rows)[-1]
            n1 = [n for n in last["nodes"] if n["id"] == "N1"][0]
            self.assertFalse(n1["ready"])  # đã hái -> đang mọc lại
            self.assertEqual(n1["regrow_ticks"], g["regrow_s"] * 60 - 1)

    def test_khong_hai_duoc_duoi_nuoc(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [12, 2]}}})
            inp = write_json(w.path("in.json"), frames({"tick": 1, "interact": True}))
            run_headless("--mode", "gather", "--seed", "1", "--ticks", "3", "--scenario", sc,
                         "--inputs", inp, "--out", w.path("o.jsonl"))
            self.assertEqual(len(events(read_jsonl(w.path("o.jsonl")), "gather")), 0)

    def test_bat_ca_duoi_nuoc_yield_va_bien_mat(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [15, 3.5]}}})
            inp = write_json(w.path("in.json"), frames({"tick": 1, "catch": True}))
            run_headless("--mode", "gather", "--seed", "1", "--ticks", "4", "--scenario", sc,
                         "--inputs", inp, "--snapshot-every", "1", "--out", w.path("o.jsonl"))
            rows = read_jsonl(w.path("o.jsonl"))
            ev = events(rows, "fish_caught")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["data"]["kind"], "ca_linh")
            self.assertEqual(ev[0]["data"]["count"], 3)
            last = snapshots(rows)[-1]
            self.assertEqual(len(last["fish"]), 5)  # F1 đã bị bắt
            self.assertEqual(last["hold"].count("ca_linh"), 3)

    def test_khong_bat_ca_o_mat_nuoc(self):
        with Workdir() as w:  # cá ở dưới nước; người chơi ở mặt nước -> không bắt
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [15, 0]},
                                                           "fish": [{"id": "F1", "kind": "ca_linh", "pos": [15, 1]}]}})
            inp = write_json(w.path("in.json"), frames({"tick": 1, "catch": True}))
            run_headless("--mode", "gather", "--seed", "1", "--ticks", "3", "--scenario", sc,
                         "--inputs", inp, "--out", w.path("o.jsonl"))
            self.assertEqual(len(events(read_jsonl(w.path("o.jsonl")), "fish_caught")), 0)

    def test_gio_day_hold_full(self):
        g = tuning_gather()
        cap = g["hold_capacity"]
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"player": {"pos": [12, 0]}, "hold": ["ca_loc"] * cap}})
            inp = write_json(w.path("in.json"), frames({"tick": 1, "interact": True}))
            run_headless("--mode", "gather", "--seed", "1", "--ticks", "3", "--scenario", sc,
                         "--inputs", inp, "--out", w.path("o.jsonl"))
            rows = read_jsonl(w.path("o.jsonl"))
            self.assertEqual(len(events(rows, "hold_full")), 1)
            self.assertEqual(len(events(rows, "gather")), 0)


if __name__ == "__main__":
    unittest.main()
