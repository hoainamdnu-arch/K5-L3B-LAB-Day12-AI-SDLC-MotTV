"""Buổi tối — Mở Quán. KHUNG: đi lại, chặn biên, đồng hồ, kho nạp từ file/scenario.

Luật nhóm MotTV:
  Lát 3 (khách): khách đến theo lịch, chọn món nấu được (ưu tiên giá cao), giữ chỗ nguyên liệu,
                 kiên nhẫn đếm ngược, hết kiên nhẫn -> customer_left (−uy tín, trả lại nguyên liệu),
                 không món nào nấu được -> no_dish.
  Lát 4 (phục vụ): interact tại bếp (cook_started -> dish_ready -> dish_picked) và bàn (served),
                   ăn xong trả tiền (paid) + boa + uy tín; hết ca -> quan_end.
"""

from ..ids import sort_by_id
from .ramp import ramp_velocity

TICK = 60.0


class QuanSim:
    mode = "quan"
    phase = "quan"

    def __init__(self, tuning, scenario, streams, ids, inventory=None):
        t = tuning["quan"]
        self.t = t
        self.menu = tuning["menu"]
        self.rng = streams
        self.ids = ids
        p = scenario.get("player", {})
        self.pos = list(p.get("pos", t["start_pos"]))
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        # kho: --inventory HOẶC scenario.stock (cả hai -> cli đã báo mã 2)
        self.stock = dict(inventory if inventory is not None else scenario.get("stock", {}))
        self.hand = scenario.get("hand")
        self.time_left_ticks = scenario.get("time_left_ticks", int(round(t["duration_s"] * 60)))
        self.reputation = scenario.get("reputation", t["reputation_initial"])
        self.stoves = [dict(s, state=s.get("state", "idle"), dish=s.get("dish"),
                            cook_ticks_left=s.get("cook_ticks_left", 0), ready_ticks=s.get("ready_ticks", 0))
                       for s in self._merge(t["stoves"], scenario.get("stoves", []))]
        self.tables = self._merge(t["tables"], scenario.get("tables", []))
        # lịch khách
        self.random_customers = scenario.get("random_customers", True)
        self.elapsed = int(round(t["duration_s"] * 60)) - self.time_left_ticks  # số tick đã trôi (hỗ trợ time_left tùy biến)
        self.patience_full = int(round(t["patience_s"] * TICK))
        # khách dựng sẵn từ scenario: suy ra giữ chỗ (reserved) nếu chưa có
        self.customers = []
        for c in scenario.get("customers", []):
            cust = {"id": c["id"], "table_id": c["table_id"], "state": c.get("state", "waiting"),
                    "order": c.get("order"), "reserved": dict(c.get("reserved", {})),
                    "patience_ticks": c.get("patience_ticks", self.patience_full),
                    "eat_ticks": c.get("eat_ticks", 0), "order_started": c.get("order_started", False),
                    "tip": c.get("tip", 0)}
            if cust["order"] is None:
                dish = self._cookable_dish()
                if dish is not None:
                    cust["order"] = dish
                    self._reserve_into(cust, dish)
            elif not cust["reserved"] and cust["state"] == "waiting":
                self._reserve_into(cust, cust["order"])
            ids.reserve(c["id"])
            self.customers.append(cust)
        self.money = 0
        self.earned = 0
        self.shift_earned = 0
        self.done = False
        self.reason = None

    @staticmethod
    def _merge(defaults, updates):
        by_id = {d["id"]: dict(d) for d in defaults}
        for u in updates:
            if u["id"] not in by_id:
                from ..errors import BadInput
                raise BadInput(f"id bếp/bàn không tồn tại: {u['id']}")
            by_id[u["id"]].update(u)
        return sort_by_id(list(by_id.values()))

    # --- giúp luật khách ------------------------------------------------------
    def _clamp_rep(self):
        self.reputation = max(self.t["reputation_min"], min(self.t["reputation_max"], self.reputation))

    def _cookable_dish(self):
        """Món nấu được từ kho hiện có; ưu tiên giá cao nhất, hoà thì theo thứ tự khoá menu."""
        best = None
        for name, d in self.menu.items():
            if all(self.stock.get(k, 0) >= n for k, n in d["recipe"].items()):
                if best is None or d["price"] > self.menu[best]["price"]:
                    best = name
        return best

    def _reserve_into(self, cust, dish):
        for k, n in self.menu[dish]["recipe"].items():
            self.stock[k] = self.stock.get(k, 0) - n
            cust["reserved"][k] = cust["reserved"].get(k, 0) + n

    def _release(self, cust):
        for k, n in cust["reserved"].items():
            self.stock[k] = self.stock.get(k, 0) + n
        cust["reserved"] = {}

    def _free_table(self):
        occ = {c["table_id"] for c in self.customers}
        for tb in self.tables:
            if tb["id"] not in occ:
                return tb["id"]
        return None

    def _spawn(self, events):
        tbl = self._free_table()
        if tbl is None:
            return  # hết bàn: khách này không vào
        dish = self._cookable_dish()
        if dish is None:
            events.append(("no_dish", {}))
            return
        cust = {"id": self.ids.new("C"), "table_id": tbl, "state": "waiting", "order": dish,
                "reserved": {}, "patience_ticks": self.patience_full, "eat_ticks": 0,
                "order_started": False, "tip": 0}
        self._reserve_into(cust, dish)
        self.customers.append(cust)
        events.append(("customer_arrived", {"customer_id": cust["id"], "table_id": tbl, "order": dish}))

    def snapshot(self) -> dict:
        occupied = {c["table_id"]: c["id"] for c in self.customers}
        return {
            "player": {"pos": self.pos},
            "stock": {k: self.stock[k] for k in sorted(self.stock) if self.stock[k] > 0},
            "hand": self.hand,
            "stoves": [{k: s.get(k) for k in ("id", "pos", "state", "dish", "cook_ticks_left", "ready_ticks")}
                       for s in self.stoves],
            "tables": [{"id": tb["id"], "pos": tb["pos"], "customer_id": occupied.get(tb["id"])} for tb in self.tables],
            "customers": [{k: c.get(k) for k in ("id", "table_id", "state", "order", "patience_ticks", "eat_ticks")}
                          for c in sort_by_id(self.customers)],
        }

    def step(self, inp):
        events = []
        self.time_left_ticks = max(0, self.time_left_ticks - 1)
        self.elapsed += 1
        # 1. đồng hồ các thực thể: bếp nấu, khách ăn, khách chờ mất kiên nhẫn
        for s in sort_by_id(self.stoves):
            if s["state"] == "cooking":
                s["cook_ticks_left"] = max(0, s["cook_ticks_left"] - 1)
                if s["cook_ticks_left"] == 0:
                    s["state"] = "ready"
                    events.append(("dish_ready", {"stove_id": s["id"], "dish": s["dish"]}))
        # khách ăn xong -> trả tiền
        for c in sort_by_id([c for c in self.customers if c["state"] == "eating"]):
            c["eat_ticks"] = max(0, c["eat_ticks"] - 1)
            if c["eat_ticks"] == 0:
                self._pay(c, events)
        # khách chờ hết kiên nhẫn -> bỏ đi
        leavers = []
        for c in sort_by_id([c for c in self.customers if c["state"] == "waiting"]):
            c["patience_ticks"] -= 1
            if c["patience_ticks"] <= 0:
                leavers.append(c)
        for c in leavers:
            self._release(c)
            self.reputation += self.t["left_reputation_delta"]
            self._clamp_rep()
            self.customers.remove(c)
            events.append(("customer_left", {"customer_id": c["id"], "table_id": c["table_id"],
                                              "reputation": self.reputation}))
        # 2. di chuyển
        self._move(inp)
        # 3. interact (tối đa một đối tượng)
        if inp.pressed("interact"):
            self._interact(events)
        # 4. khách mới theo lịch
        if self.random_customers and self.elapsed >= int(self.t["first_customer_tick"]):
            interval = int(round(self.t["customer_interval_s"] * TICK))
            if (self.elapsed - int(self.t["first_customer_tick"])) % interval == 0:
                self._spawn(events)
        # 5. hết ca
        if self.time_left_ticks <= 0:
            self.done = True
            self.reason = "time"
            events.append(("quan_end", {"reason": "time", "money": self.money, "earned": self.earned,
                                        "shift_earned": self.shift_earned, "reputation": self.reputation}))
        return events

    # --- phục vụ (lát 4) ------------------------------------------------------
    def _pay(self, cust, events):
        dish = cust["order"]
        price = self.menu[dish]["price"]
        tip = cust.get("tip", 0)
        amount = price + tip
        self.money += amount
        self.earned += amount
        self.shift_earned += amount
        if tip > 0:
            self.reputation += self.t["tip_reputation"]
            self._clamp_rep()
        self.customers.remove(cust)
        events.append(("paid", {"customer_id": cust["id"], "dish": dish, "amount": amount, "tip": tip,
                                "reputation": self.reputation}))

    def _nearest_interactable(self):
        """Đối tượng gần nhất trong interact_radius: bếp trước bàn, id nhỏ khi hoà."""
        import math
        r = self.t["interact_radius"]
        best = None  # (dist, rank, id, kind, obj) rank 0 bếp, 1 bàn
        for rank, (kind, coll) in enumerate((("stove", self.stoves), ("table", self.tables))):
            for o in coll:
                dd = math.dist(self.pos, o["pos"])
                if dd <= r:
                    key = (dd, rank, o["id"])
                    if best is None or key < best[0]:
                        best = (key, kind, o)
        return (best[1], best[2]) if best else (None, None)

    def _interact(self, events):
        kind, obj = self._nearest_interactable()
        if kind == "stove":
            self._interact_stove(obj, events)
        elif kind == "table":
            self._interact_table(obj, events)

    def _interact_stove(self, stove, events):
        if stove["state"] == "ready" and self.hand is None:
            self.hand = stove["dish"]
            events.append(("dish_picked", {"stove_id": stove["id"], "dish": stove["dish"]}))
            stove["state"] = "idle"
            stove["dish"] = None
        elif stove["state"] == "idle":
            cust = self._next_to_cook()
            if cust is not None:
                stove["state"] = "cooking"
                stove["dish"] = cust["order"]
                stove["cook_ticks_left"] = int(round(self.menu[cust["order"]]["cook_s"] * TICK))
                cust["order_started"] = True
                cust["reserved"] = {}  # nguyên liệu đã vào nồi
                events.append(("cook_started", {"stove_id": stove["id"], "dish": cust["order"],
                                                "customer_id": cust["id"]}))

    def _next_to_cook(self):
        """Khách đang chờ, chưa bắt đầu nấu, id bàn nhỏ nhất."""
        waiting = [c for c in self.customers if c["state"] == "waiting" and not c["order_started"]]
        return sort_by_id(waiting, key=lambda c: c["table_id"])[0] if waiting else None

    def _interact_table(self, table, events):
        if self.hand is None:
            return
        cust = next((c for c in self.customers if c["table_id"] == table["id"]), None)
        if cust is None or cust["state"] != "waiting" or cust["order"] != self.hand:
            return
        # phục vụ: tính boa theo kiên nhẫn còn lại lúc dọn món
        ratio = cust["patience_ticks"] / self.patience_full if self.patience_full else 0
        if ratio >= self.t["tip_min_patience_ratio"]:
            cust["tip"] = int(round(self.t["tip_rate"] * self.menu[self.hand]["price"]))
        cust["state"] = "eating"
        cust["eat_ticks"] = int(round(self.t["eat_s"] * TICK))
        events.append(("served", {"customer_id": cust["id"], "table_id": table["id"], "dish": self.hand}))
        self.hand = None

    def _move(self, inp):
        speed = self.t["walk_speed"]
        mx, mz = inp.move
        self.vel = ramp_velocity(self, (mx * speed, mz * speed), int(self.t.get("ramp_max_ticks", 6)))
        b = self.t["bounds"]
        for i, axis in enumerate(("x", "z")):
            self.pos[i] += self.vel[i] / TICK
            lo, hi = b[axis]
            if self.pos[i] <= lo:
                self.pos[i], self.vel[i] = lo, max(0.0, self.vel[i])
            elif self.pos[i] >= hi:
                self.pos[i], self.vel[i] = hi, min(0.0, self.vel[i])
