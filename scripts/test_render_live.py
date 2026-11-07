import urllib.request
import json

BASE = "https://q-frontier.onrender.com"

def test_routes():
    print(f"=== TESTING LIVE DEPLOYMENT AT {BASE} ===")
    
    # 1. Root SPA HTML
    with urllib.request.urlopen(BASE + "/") as res:
        html = res.read().decode("utf-8")
        print(f"[PASS] GET / -> Status {res.status}, Length: {len(html)}")

    # 2. Check Static Assets
    for token in html.split():
        if "/assets/" in token:
            start = token.find("/assets/")
            end = token.find('"', start)
            if end == -1:
                end = token.find("'", start)
            asset_path = token[start:end]
            with urllib.request.urlopen(BASE + asset_path) as a_res:
                print(f"[PASS] Static Asset {asset_path} -> Status {a_res.status}, Size: {len(a_res.read())} bytes")

    # 3. /api/health
    with urllib.request.urlopen(BASE + "/api/health") as res:
        data = json.loads(res.read())
        print(f"[PASS] /api/health -> Status {res.status}, Backend Aer: {data['backends']['qiskit_aer']}, Python: {data['python_version']}")

    # 4. /api/datasets
    with urllib.request.urlopen(BASE + "/api/datasets") as res:
        datasets = json.loads(res.read())
        print(f"[PASS] /api/datasets -> Status {res.status}, Count: {len(datasets)}")

    # 5. /api/market/clusters
    with urllib.request.urlopen(BASE + "/api/market/clusters") as res:
        clusters = json.loads(res.read())
        print(f"[PASS] /api/market/clusters -> Status {res.status}, Assets: {len(clusters['tickers'])}, Clusters: {len(clusters['clusters'])}")

    # 6. /api/hardware/benchmarks
    with urllib.request.urlopen(BASE + "/api/hardware/benchmarks") as res:
        hw = json.loads(res.read())
        print(f"[PASS] /api/hardware/benchmarks -> Status {res.status}, IonQ SWAPs: {hw['hardware_comparison']['ionq_trapped_ion']['routing_swaps']}, IBM SWAPs: {hw['hardware_comparison']['ibm_heavy_hex']['routing_swaps']}")

    # 7. /api/runs (GET)
    with urllib.request.urlopen(BASE + "/api/runs") as res:
        runs = json.loads(res.read())
        print(f"[PASS] /api/runs -> Status {res.status}, History Count: {len(runs)}")

    print("=== ALL LIVE TESTS ON RENDER PASSED SUCCESSFULLY ===")

if __name__ == "__main__":
    test_routes()

