"""
Q-FRONTIER: Automated End-to-End Smoke Test & System Verification
Verifies test suites, API endpoints, pre-rendered notebook, and presentation deck.
"""

import sys
import subprocess
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "backend"
sys.path.insert(0, str(backend_dir))

def test_step(step_name, fn):
    print(f"\n[CHECK] {step_name}...")
    try:
        fn()
        print(f"  [PASS] {step_name} passed.")
        return True
    except Exception as e:
        print(f"  [FAIL] {step_name} failed: {e}")
        return False

def check_imports():
    import qiskit
    import qiskit_aer
    import QuantumRingsLib
    import fastapi
    import numpy as np
    import scipy
    import pandas as pd
    assert qiskit.__version__ is not None
    assert QuantumRingsLib is not None

def check_pytest():
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-o", "pythonpath=backend", "backend/tests/"],
        cwd=str(root_dir),
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        raise RuntimeError(f"Pytest failed:\n{res.stdout}\n{res.stderr}")
    print(f"  Pytest Output: {res.stdout.splitlines()[-1]}")

def check_spa_and_api():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)

    # 1. Root SPA HTML check
    res_root = client.get("/")
    assert res_root.status_code == 200, f"Expected 200 from root, got {res_root.status_code}"
    assert "Q-FRONTIER" in res_root.text or "root" in res_root.text

    # 2. Health API check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    data = res_health.json()
    assert data["status"] == "healthy"
    assert "Nasdaq" in data["sponsors"]

    # 3. Market Clusters check
    res_clusters = client.get("/api/market/clusters")
    assert res_clusters.status_code == 200
    assert len(res_clusters.json()["clusters"]) == 3

    # 4. Hardware Benchmarks check
    res_hw = client.get("/api/hardware/benchmarks")
    assert res_hw.status_code == 200
    assert res_hw.json()["hardware_comparison"]["ionq_trapped_ion"]["routing_swaps"] == 0

def check_notebook():
    nb_path = root_dir / "notebooks" / "IQC_Q_FRONTIER_Master.ipynb"
    assert nb_path.exists(), "Notebook does not exist!"
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    assert len(code_cells) >= 8, f"Expected at least 8 code cells, found {len(code_cells)}"
    
    for idx, c in enumerate(code_cells):
        assert len(c.get("outputs", [])) > 0, f"Code cell {idx + 1} has no pre-rendered outputs!"

def check_docs_and_slides():
    devpost = root_dir / "docs" / "DEVPOST_SUBMISSION.md"
    slides = root_dir / "docs" / "slides.html"
    pitch = root_dir / "docs" / "PITCH_DECK_SCRIPT.md"
    video = root_dir / "docs" / "DEMO_VIDEO_SCRIPT.md"
    
    for f in [devpost, slides, pitch, video]:
        assert f.exists(), f"Missing required file: {f.name}"
        assert f.stat().st_size > 500, f"File {f.name} is suspiciously small!"

def main():
    print("========================================================================")
    print(" Q-FRONTIER: Automated End-to-End Verification & Health Inspection")
    print("========================================================================")
    
    checks = [
        ("Python & Quantum Dependencies", check_imports),
        ("Full Backend Test Suite (37 Tests)", check_pytest),
        ("Single-Port FastAPI & React SPA Endpoints", check_spa_and_api),
        ("Pre-Rendered Master Jupyter Notebook", check_notebook),
        ("Judging Pitch Deck, Slides, & Devpost Docs", check_docs_and_slides)
    ]
    
    results = [test_step(name, fn) for name, fn in checks]
    
    print("\n========================================================================")
    if all(results):
        print(" [SUCCESS] ALL 5 VERIFICATION CHECKS PASSED WITH 100% INTEGRITY!")
        print(" The Q-FRONTIER project is fully ready for IQC 2026 submission.")
    else:
        print(" [WARNING] Some verification checks failed. Review the logs above.")
    print("========================================================================\n")

if __name__ == "__main__":
    main()

