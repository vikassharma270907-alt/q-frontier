"""
Q-FRONTIER: Unified Application Launcher
Launches FastAPI backend on http://localhost:8000 serving both API and React Dashboard.
"""

import sys
import os
from pathlib import Path
import uvicorn

# Ensure backend is on PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "backend"
sys.path.insert(0, str(backend_dir))
os.environ["PYTHONPATH"] = str(backend_dir)

if __name__ == "__main__":
    print("=" * 70)
    print("  Q-FRONTIER: Auditable Hybrid Optimization Research Workbench")
    print("  Intermountain Quantum Competition (IQC) 2026")
    print("=" * 70)
    print("  Dashboard UI: http://localhost:8000")
    print("  Interactive OpenAPI Docs: http://localhost:8000/docs")
    print("  Mode: SIMULATED (Exact Statevector)")
    print("  Scientific Integrity: Active (Fair Classical vs Quantum Comparison)")
    print("=" * 70)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
