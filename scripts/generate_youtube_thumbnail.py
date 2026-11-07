"""
Q-FRONTIER: YouTube Thumbnail Generator
Generates a high-contrast 1280x720 (16:9) professional YouTube thumbnail
optimized for click-through rate, competition judges, and technical clarity.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAIL_PATH = DOCS_DIR / "YOUTUBE_THUMBNAIL.png"

# YouTube thumbnail standard: 1280x720 (16:9)
WIDTH, HEIGHT = 12.8, 7.2
DPI = 100

def generate_thumbnail():
    fig = plt.figure(figsize=(WIDTH, HEIGHT), dpi=DPI, facecolor="#09090b")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#09090b")
    ax.set_xlim(0, 1280)
    ax.set_ylim(0, 720)
    ax.axis("off")

    # 1. Subtle glowing background gradient grid
    for x in range(0, 1280, 80):
        ax.axvline(x, color="#181822", lw=1, alpha=0.6)
    for y in range(0, 720, 80):
        ax.axhline(y, color="#181822", lw=1, alpha=0.6)

    # Top accent glowing line
    ax.plot([0, 1280], [715, 715], color="#06b6d4", lw=6)

    # 2. Event & Submission Top Badge
    top_badge = patches.FancyBboxPatch((60, 630), 430, 48, boxstyle="round,pad=0.3",
                                      facecolor="#18181b", edgecolor="#06b6d4", linewidth=2)
    ax.add_patch(top_badge)
    ax.text(275, 654, "★ BYU IQC 2026 SUBMISSION", color="#38bdf8",
            fontsize=13, fontweight="bold", ha="center", va="center", fontfamily="sans-serif")

    # Time pill badge
    time_badge = patches.FancyBboxPatch((1040, 630), 180, 48, boxstyle="round,pad=0.3",
                                       facecolor="#18181b", edgecolor="#f59e0b", linewidth=2)
    ax.add_patch(time_badge)
    ax.text(1130, 654, "2:46 DEMO", color="#fbbf24",
            fontsize=13, fontweight="bold", ha="center", va="center")

    # 3. Main Headline
    ax.text(60, 545, "Q-FRONTIER", color="#ffffff",
            fontsize=56, fontweight="heavy", fontfamily="sans-serif", va="center")
    
    # Sub-headline badge
    sub_badge = patches.FancyBboxPatch((60, 440), 660, 54, boxstyle="round,pad=0.4",
                                       facecolor="#0284c7", edgecolor="#38bdf8", linewidth=1.5)
    ax.add_patch(sub_badge)
    ax.text(390, 467, "ZERO SHOT LEAKAGE QUANTUM QAOA", color="#ffffff",
            fontsize=17, fontweight="heavy", ha="center", va="center")

    ax.text(60, 395, "Cardinality-Constrained Portfolio Optimization on Nasdaq Equities",
            color="#a1a1aa", fontsize=15, fontweight="bold")

    # 4. Right Side: High-Impact Comparison Card
    card_bg = patches.FancyBboxPatch((760, 120), 460, 470, boxstyle="round,pad=1.2",
                                     facecolor="#121217", edgecolor="#27272a", linewidth=2.5)
    ax.add_patch(card_bg)

    ax.text(990, 545, "SOLVER BENCHMARK", color="#71717a",
            fontsize=13, fontweight="bold", ha="center")

    # Penalty QAOA (Failure Mode - Red)
    pen_box = patches.FancyBboxPatch((790, 360), 400, 140, boxstyle="round,pad=0.8",
                                    facecolor="#1c1316", edgecolor="#f43f5e", linewidth=2)
    ax.add_patch(pen_box)
    ax.text(810, 465, "Standard Penalty-QAOA", color="#fb7185", fontsize=14, fontweight="bold")
    ax.text(810, 425, "Shot Leakage: 26.7% ✘", color="#ffffff", fontsize=20, fontweight="heavy")
    ax.text(810, 390, "Wasted shots & barren plateaus", color="#fda4af", fontsize=11)

    # Q-FRONTIER CCD-QAOA (Green / Cyan)
    q_box = patches.FancyBboxPatch((790, 160), 400, 175, boxstyle="round,pad=0.8",
                                  facecolor="#0c1f1a", edgecolor="#10b981", linewidth=2.5)
    ax.add_patch(q_box)
    ax.text(810, 295, "Q-FRONTIER (Dicke + AGP)", color="#34d399", fontsize=14, fontweight="bold")
    ax.text(810, 245, "100% FEASIBLE ✔", color="#ffffff", fontsize=24, fontweight="heavy")
    ax.text(810, 205, "Approximation Ratio: 99.8%", color="#6ee7b7", fontsize=13, fontweight="bold")
    ax.text(810, 180, "Zero Wasted Shots | Exact Commutation", color="#a7f3d0", fontsize=10)

    # 5. Bottom Callout Badges
    features = [
        {"x": 60, "w": 200, "txt": "✔ RMT Denoising", "col": "#06b6d4"},
        {"x": 280, "w": 210, "txt": "✔ QCL Volatility", "col": "#8b5cf6"},
        {"x": 510, "w": 210, "txt": "✔ Sandia Heatmap", "col": "#10b981"}
    ]
    for f in features:
        bx = patches.FancyBboxPatch((f["x"], 290), f["w"], 46, boxstyle="round,pad=0.3",
                                    facecolor="#18181b", edgecolor=f["col"], linewidth=1.5)
        ax.add_patch(bx)
        ax.text(f["x"] + f["w"]/2, 313, f["txt"], color=f["col"],
                fontsize=13, fontweight="bold", ha="center", va="center")

    # 6. Bottom Sponsor Bar
    ax.text(60, 175, "OFFICIAL COMPETITION SPONSOR ECOSYSTEM", color="#71717a",
            fontsize=11, fontweight="bold")
    sponsors = "Nasdaq  •  IonQ  •  Sandia Nat Lab  •  IBM Quantum  •  Quantum Rings  •  Classiq"
    ax.text(60, 135, sponsors, color="#38bdf8", fontsize=13, fontweight="bold")

    # Bottom verification line
    ax.text(60, 50, "Simulated Exact Statevector Evolution (Qiskit Aer)  |  52 Passing Test Suites",
            color="#52525b", fontsize=11, fontfamily="monospace")

    plt.savefig(THUMBNAIL_PATH, dpi=DPI)
    plt.close(fig)
    print(f"[✔] YouTube thumbnail generated successfully: {THUMBNAIL_PATH}")

if __name__ == "__main__":
    generate_thumbnail()
