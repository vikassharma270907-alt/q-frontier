"""
Helper script to execute and pre-render IQC_Q_FRONTIER_Master.ipynb with full outputs.
"""

import json
import io
import contextlib
import sys
import os
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
nb_path = root_dir / "notebooks" / "IQC_Q_FRONTIER_Master.ipynb"

# Add backend to sys.path
backend_path = root_dir / "backend"
sys.path.insert(0, str(backend_path))

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Global execution scope
exec_globals = {"__name__": "__main__"}

exec_count = 1
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        # Ensure backend is in path in notebook code
        source = source.replace("os.path.abspath('../backend')", f"r'{str(backend_path)}'")
        stdout_capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stdout_capture):
                exec(source, exec_globals)
            out_str = stdout_capture.getvalue()
            cell["execution_count"] = exec_count
            cell["outputs"] = [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [line + "\n" for line in out_str.splitlines()]
                }
            ] if out_str else []
            print(f"Executed code cell {exec_count} successfully.")
        except Exception as e:
            err_str = f"Error executing cell: {e}\n"
            print(f"Error in cell {exec_count}: {e}")
            cell["execution_count"] = exec_count
            cell["outputs"] = [
                {
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [stdout_capture.getvalue(), err_str]
                }
            ]
        exec_count += 1

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Pre-rendered all notebook outputs into notebooks/IQC_Q_FRONTIER_Master.ipynb successfully!")
