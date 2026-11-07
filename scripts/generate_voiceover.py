"""
Q-FRONTIER: Studio Voiceover Generator
Uses Microsoft Azure Neural TTS (ChristopherNeural / Marcus Wispr Flow style)
to generate scene-by-scene audio tracks and full merged audio.
"""

import os
import asyncio
from pathlib import Path
import edge_tts

AUDIO_DIR = Path(__file__).resolve().parent.parent / "docs" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Voice configuration matching Wispr Flow Persona: Marcus / ChristopherNeural
VOICE = "en-US-ChristopherNeural"
RATE = "+2%"   # 138 WPM optimal technical cadence
PITCH = "+0Hz"

SCENES = [
    {
        "id": 1,
        "filename": "scene1.mp3",
        "title": "Introduction & Competition Context",
        "text": (
            "Welcome to Q-FRONTIER, our submission for the 2026 Intermountain Quantum Competition "
            "at Brigham Young University. When solving cardinality-constrained portfolio optimization "
            "for Nasdaq equities, NISQ algorithms face a critical bottleneck: quadratic penalties "
            "leak measurement shots, static clustering ignores cross-cluster risk, and unconstrained "
            "rebalancing destroys capital through fees. Q-FRONTIER eliminates all three challenges "
            "in a single auditable workbench."
        )
    },
    {
        "id": 2,
        "filename": "scene2.mp3",
        "title": "Stage 1: RMT Spectral Denoising & Clustering",
        "text": (
            "We start with real Nasdaq-12 market data. We compute the Ledoit-Wolf shrinkage covariance "
            "and apply Random Matrix Theory Marchenko-Pastur filtering. All eigenvalues below lambda-plus "
            "represent empirical noise and are filtered out, preserving genuine economic signal. "
            "Our hardware-aware clustering algorithm then partitions the 12-asset universe into 3 clusters "
            "of at most 4 qubits each, ideally sized for near-term quantum processors."
        )
    },
    {
        "id": 3,
        "filename": "scene3.mp3",
        "title": "Stages 2 & 3: QCL Sensor & CCD-QAOA Engine",
        "text": (
            "In Stage 2, our 4-qubit data-reuploading QCL sensor encodes four primitive market signals "
            "and dynamically calibrates portfolio risk aversion q_t. In Stage 3, we execute our "
            "Constrained Counterdiabatic QAOA solver. Look closely at this comparison: standard "
            "Penalty-QAOA leaks over 26% of all shots into illegal portfolio sizes. By initializing "
            "registers in exact Dicke states with complete-graph XY mixers, Q-FRONTIER mathematically "
            "guarantees 100% feasibility with zero leakage. Adding 3-body Adiabatic Gauge Potential "
            "driving boosts the approximation ratio to 95.7% at single depth, and over 99.7% at depth two."
        )
    },
    {
        "id": 4,
        "filename": "scene4.mp3",
        "title": "Stage 4: SLSQP Continuous Allocation & Backtest",
        "text": (
            "Stage 4 takes the quantum-selected asset subset and optimizes continuous weights for "
            "maximum Sharpe ratio using SLSQP. In our monthly walk-forward simulation, all returns "
            "are evaluated strictly net of five basis points transaction costs. By incorporating "
            "our turnover continuity parameter kappa, Q-FRONTIER suppresses costly portfolio churning, "
            "outperforming the benchmark by over 24% cumulative return with less than half the maximum drawdown."
        )
    },
    {
        "id": 5,
        "filename": "scene5.mp3",
        "title": "Hardware Topologies, Sandia Heatmap & Conclusion",
        "text": (
            "Finally, we benchmark physical hardware topologies. On IonQ's trapped-ion architecture, "
            "all-to-all connectivity compiles our complete-graph mixers with zero routing SWAPs, "
            "while heavy-hex grids require 18 additional SWAPs. Following Sandia National Laboratories' "
            "volumetric benchmarking framework, our 2D heatmap maps circuit capability under noise. "
            "Q-FRONTIER is fully verifiable, backed by 43 automated tests and one-click reproducibility. "
            "Thank you!"
        )
    }
]


async def generate_scene(scene: dict):
    out_path = AUDIO_DIR / scene["filename"]
    print(f"[*] Generating {scene['filename']} ({scene['title']})...")
    communicate = edge_tts.Communicate(scene["text"], VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(out_path))
    print(f"[+] Saved {out_path} ({os.path.getsize(out_path):,} bytes)")


async def generate_full_track():
    full_text = " ... ".join([s["text"] for s in SCENES])
    out_path = AUDIO_DIR / "full_voiceover.mp3"
    print(f"\n[*] Generating merged audio: full_voiceover.mp3...")
    communicate = edge_tts.Communicate(full_text, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(out_path))
    print(f"[+] Saved {out_path} ({os.path.getsize(out_path):,} bytes)")


async def main():
    print(f"=== Q-FRONTIER Voiceover Synthesis ===")
    print(f"Voice: {VOICE} | Rate: {RATE} | Target: {AUDIO_DIR}\n")
    for scene in SCENES:
        await generate_scene(scene)
    await generate_full_track()
    print("\n[✔] All audio tracks successfully generated!")


if __name__ == "__main__":
    asyncio.run(main())
