# Bằng chứng demo — tích hợp buổi sáng → buổi tối (Contract G)

Lệnh (tất định, cùng seed → giống từng byte):

```bash
# Buổi sáng: cập bến tick 0 → xuất kho
python3 -m chonoi.headless --mode gather --seed 1 --ticks 1 \
  --scenario g.json --inputs gin.json --inventory-out kho.json --out g.jsonl
# g.json  = {"gather": {"hold": ["ca_loc","bong_sung","bong_sung","ca_linh","ca_linh","ca_linh","bong_dien_dien"]}}
# gin.json= {"frames": [{"tick": 0, "interact": true}]}

# Buổi tối: nạp kho
python3 -m chonoi.headless --mode quan --seed 1 --ticks 0 --inventory kho.json --out q.jsonl
```

Kết quả:

```
kho.json  = {"items":{"bong_dien_dien":1,"bong_sung":2,"ca_linh":3,"ca_loc":1}}
quán stock (tick 0) = {"bong_dien_dien":1,"bong_sung":2,"ca_linh":3,"ca_linh":3,...}
```

Kho này đủ nấu cả **`lau_ca_linh_dien_dien`** (ca_linh×3 + bong_dien_dien×1, giá 120) — món đắt nhất,
nên khách sẽ ưu tiên gọi món này (luật chọn món giá cao nhất).

## Vòng phục vụ đầy đủ (nấu→bưng→phục vụ→trả tiền + boa)
Chứng minh bằng test hộp đen `tests/test_quan_rules.py::Serving::test_nau_phuc_vu_tra_tien_co_boa`:
khách gọi `goi_bong_sung`, nấu 4s, phục vụ khi còn nhiều kiên nhẫn → boa 8, tổng thu 48, uy tín 3.0→3.2.

Chạy lại toàn bộ: `PYTHONPATH=tests:. python3 -m unittest discover -s tests` → **46 pass**.
