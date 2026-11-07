"""
Q-FRONTIER: One-Click Interactive Video Demo Launcher (Python)
Opens the animated video demo player directly in the default browser.
"""

import sys
import webbrowser
from pathlib import Path

def main():
    print("=" * 74)
    print(" Q-FRONTIER: Animated Video Demo & Neural Studio Narration Launcher")
    print(" Intermountain Quantum Competition (IQC) 2026 — Brigham Young University")
    print("=" * 74)
    
    demo_file = Path(__file__).resolve().parent.parent / "docs" / "video_demo_player.html"
    if not demo_file.exists():
        print(f"[!] Error: Demo file not found at {demo_file}")
        sys.exit(1)
        
    url = demo_file.as_uri()
    print(f"\n[+] Launching Video Demo Player:")
    print(f"    {url}")
    print("\n[*] Click the Play button in the player to start the 2:46 walkthrough.")
    print("=" * 74 + "\n")
    
    webbrowser.open(url)

if __name__ == "__main__":
    main()
