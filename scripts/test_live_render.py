"""
Diagnostic script testing all live API endpoints on Render.
"""

import urllib.request
import urllib.error
import json
import time

BASE_URL = "https://q-frontier.onrender.com"

endpoints_to_test = [
    ("GET", "/api/health", None),
    ("GET", "/api/datasets", None),
    ("GET", "/api/market/clusters", None),
    ("GET", "/api/hardware/benchmarks?n_qubits=4", None),
    (
        "POST",
        "/api/stress-test",
        {
            "scenario": "CRISIS_2026_LIQUIDITY",
            "k_cardinality": 2,
            "asset_count": 4,
            "transaction_cost_bps": 5.0,
        },
    ),
    (
        "POST",
        "/api/runs",
        {
            "dataset_id": "synthetic_tech_4",
            "asset_count": 4,
            "k_cardinality": 2,
            "lambda_risk": 0.5,
            "covariance_method": "ledoit_wolf",
            "solvers": ["exact", "annealing", "xy_qaoa", "ccd_qaoa", "gnn_xy_qaoa", "penalty_qaoa"],
            "circuit_depth": 1,
            "seeds": [42],
            "transaction_cost_bps": 5.0,
            "turnover_penalty": 0.05,
        },
    ),
]

print(f"Connecting to live Render deployment: {BASE_URL}...")
success_count = 0

for method, path, payload in endpoints_to_test:
    url = BASE_URL + path
    headers = {"User-Agent": "Mozilla/5.0"}
    data_bytes = None
    if payload:
        headers["Content-Type"] = "application/json"
        data_bytes = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            elapsed = (time.perf_counter() - t0) * 1000.0
            data = resp.read()
            ct = resp.headers.get("Content-Type", "")
            print(f"  [PASS {resp.status}] {method:4} {path:35} -> {elapsed:6.1f}ms ({len(data)} bytes, {ct.split(';')[0]})")
            success_count += 1
    except urllib.error.HTTPError as e:
        elapsed = (time.perf_counter() - t0) * 1000.0
        err_msg = e.read().decode("utf-8", errors="replace")[:200]
        print(f"  [HTTP {e.code}] {method:4} {path:35} -> {elapsed:6.1f}ms | Error: {err_msg}")
    except Exception as e:
        elapsed = (time.perf_counter() - t0) * 1000.0
        print(f"  [ERROR]     {method:4} {path:35} -> {elapsed:6.1f}ms | Exception: {e}")

print(f"\nCompleted live audit: {success_count}/{len(endpoints_to_test)} endpoints passed.")
