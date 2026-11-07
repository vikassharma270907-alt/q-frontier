"""
Q-FRONTIER: Automated Submission Packaging Script
Packages the repository into a clean, zero-bloat ZIP archive ready for Devpost and Aqora upload.
"""

import os
import zipfile
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
dist_dir = root_dir / "dist"
dist_dir.mkdir(parents=True, exist_ok=True)

zip_filename = dist_dir / "Q-FRONTIER-Submission-IQC2026.zip"

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".vscode",
    ".idea"
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".DS_Store"
}

print(f"Creating submission package: {zip_filename.name}...")

with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(root_dir):
        # Prune unwanted directories
        subfolders[:] = [d for d in subfolders if d not in EXCLUDE_DIRS and not d.startswith(".")]
        
        # Don't package the output dist directory into itself
        if Path(foldername) == dist_dir:
            continue
            
        for filename in filenames:
            ext = Path(filename).suffix
            if ext in EXCLUDE_EXTS or filename.startswith("."):
                continue
                
            filepath = Path(foldername) / filename
            arcname = filepath.relative_to(root_dir)
            zipf.write(filepath, arcname)

size_mb = zip_filename.stat().st_size / (1024 * 1024)
print(f"Successfully created: {zip_filename} ({size_mb:.2f} MB)")

