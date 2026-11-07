"""
Generates a unique, cool, modern 3:2 aspect ratio (1200x800) Devpost thumbnail for Q-FRONTIER.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1200
HEIGHT = 800  # Exact 3:2 ratio

# 1. Base Dark Canvas
img = Image.new("RGBA", (WIDTH, HEIGHT), (6, 9, 18, 255))
draw = ImageDraw.Draw(img)

# 2. Glowing Radial Background Gradients
# Top right quantum cyan glow
glow_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_overlay)

for r in range(450, 0, -5):
    alpha = int(45 * (1 - r / 450))
    glow_draw.ellipse([850 - r, 200 - r, 850 + r, 200 + r], fill=(0, 240, 255, alpha))

# Bottom left neon violet glow
for r in range(500, 0, -6):
    alpha = int(40 * (1 - r / 500))
    glow_draw.ellipse([250 - r, 650 - r, 250 + r, 650 + r], fill=(168, 85, 247, alpha))

# Center golden finance bloom
for r in range(350, 0, -5):
    alpha = int(35 * (1 - r / 350))
    glow_draw.ellipse([600 - r, 420 - r, 600 + r, 420 + r], fill=(245, 158, 11, alpha))

img = Image.alpha_composite(img, glow_overlay)
draw = ImageDraw.Draw(img)

# 3. Geometric Quantum Grid Lines
grid_color = (255, 255, 255, 12)
for x in range(0, WIDTH, 60):
    draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
for y in range(0, HEIGHT, 60):
    draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)

# 4. Stylized Financial Market Candlesticks in the background
import random
random.seed(42)

candle_x_start = 680
candle_base_y = 520
candles = [
    (20, 45, 15, 50, True),
    (18, 30, 10, 35, True),
    (32, 20, 15, 38, False),
    (22, 55, 18, 62, True),
    (40, 25, 20, 45, False),
    (30, 68, 25, 75, True),
    (45, 80, 35, 90, True),
    (70, 110, 60, 125, True),
    (95, 140, 85, 150, True),
]

for idx, (open_p, close_p, low_p, high_p, is_up) in enumerate(candles):
    cx = candle_x_start + idx * 48
    color = (52, 211, 153, 180) if is_up else (248, 113, 113, 180)
    wick_color = (52, 211, 153, 100) if is_up else (248, 113, 113, 100)
    
    # Wick
    y_high = candle_base_y - high_p * 1.8
    y_low = candle_base_y - low_p * 1.8
    draw.line([(cx + 10, y_high), (cx + 10, y_low)], fill=wick_color, width=2)
    
    # Body
    top_y = candle_base_y - max(open_p, close_p) * 1.8
    bot_y = candle_base_y - min(open_p, close_p) * 1.8
    draw.rounded_rectangle([cx, top_y, cx + 20, bot_y], radius=3, fill=color)

# 5. Glowing Quantum Wave / Equity Curve
curve_points = []
for x in range(0, WIDTH, 10):
    # Sinusoidal quantum wave evolving into an exponential financial growth trajectory
    prog = x / WIDTH
    y = 540 - 240 * (prog ** 1.8) + math.sin(x * 0.02) * 28 * (1 - prog * 0.5)
    curve_points.append((x, y))

# Draw curve glow
for w, a in [(12, 20), (8, 40), (4, 120), (2, 255)]:
    curve_color = (0, 240, 255, a)
    for i in range(len(curve_points) - 1):
        draw.line([curve_points[i], curve_points[i+1]], fill=curve_color, width=w)

# 6. Quantum Circuit / Bloch Entanglement Graphic Ring
center_ring = (940, 250)
ring_r = 130
for r in [ring_r + 20, ring_r, ring_r - 25, ring_r - 50]:
    draw.ellipse([center_ring[0] - r, center_ring[1] - r, center_ring[0] + r, center_ring[1] + r],
                 outline=(0, 240, 255, 45 if r == ring_r else 20), width=2)

# Nodes on the ring (representing K-of-N qubits)
for i in range(8):
    theta = i * (2 * math.pi / 8)
    nx = center_ring[0] + ring_r * math.cos(theta)
    ny = center_ring[1] + ring_r * math.sin(theta)
    # Active qubits in gold, idle in cyan
    node_color = (250, 204, 21, 255) if i in [0, 2, 5] else (56, 189, 248, 180)
    draw.ellipse([nx - 9, ny - 9, nx + 9, ny + 9], fill=node_color)
    # Interconnecting chord lines (XY mixer K_n)
    for j in range(i + 1, 8):
        theta2 = j * (2 * math.pi / 8)
        nx2 = center_ring[0] + ring_r * math.cos(theta2)
        ny2 = center_ring[1] + ring_r * math.sin(theta2)
        chord_color = (168, 85, 247, 35) if (i in [0, 2, 5] and j in [0, 2, 5]) else (255, 255, 255, 10)
        draw.line([(nx, ny), (nx2, ny2)], fill=chord_color, width=2 if (i in [0, 2, 5] and j in [0, 2, 5]) else 1)

# Center QPU Core icon
draw.ellipse([center_ring[0] - 28, center_ring[1] - 28, center_ring[0] + 28, center_ring[1] + 28], fill=(13, 20, 38, 230), outline=(0, 240, 255, 200), width=2)
draw.ellipse([center_ring[0] - 12, center_ring[1] - 12, center_ring[0] + 12, center_ring[1] + 12], fill=(0, 240, 255, 255))

# 7. Typography
try:
    font_hero = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 64)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)
    font_body = ImageFont.truetype("C:/Windows/Fonts/calibri.ttf", 20)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
    font_bold_badge = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 15)
except Exception:
    font_hero = font_sub = font_body = font_badge = font_bold_badge = ImageFont.load_default()

# Event Badge
badge_box = [80, 80, 480, 120]
draw.rounded_rectangle(badge_box, radius=8, fill=(15, 23, 42, 220), outline=(56, 189, 248, 120), width=1)
draw.text((95, 90), "IQC 2026 | BRIGHAM YOUNG UNIVERSITY", font=font_bold_badge, fill=(56, 189, 248, 255))

# Title: Q-FRONTIER
# Glow layer for title
title_glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
title_draw = ImageDraw.Draw(title_glow)
title_draw.text((80, 142), "Q-FRONTIER", font=font_hero, fill=(0, 240, 255, 100))
blurred_title = title_glow.filter(ImageFilter.GaussianBlur(10))
img = Image.alpha_composite(img, blurred_title)
draw = ImageDraw.Draw(img)

# Crisp Title Text
draw.text((80, 140), "Q-FRONTIER", font=font_hero, fill=(255, 255, 255, 255))

# Subtitle
draw.text((82, 220), "Auditable Hybrid Quantum Optimization Workbench", font=font_sub, fill=(226, 232, 240, 240))
draw.text((82, 255), "Subspace-Preserving CCD-QAOA  *  QCL Rough Volatility  *  SLSQP", font=font_body, fill=(148, 163, 184, 230))

# 8. Feature Highlight Badges (3 Glassmorphic Cards)
cards = [
    ("100% FEASIBILITY", "Zero Shot Leakage\nExact Dicke |D_K^N>", (52, 211, 153)),
    ("95.7% AR @ p=1", "Counterdiabatic AGP\nSupercharged Trotter", (56, 189, 248)),
    ("+31.4% RESILIENCE", "QCL Volatility Tuning\nCrisis Drawdown Guard", (250, 204, 21)),
]

for idx, (heading, desc, accent) in enumerate(cards):
    bx = 80 + idx * 260
    by = 320
    bw = 240
    bh = 110
    
    # Card background
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(15, 23, 42, 190), outline=(accent[0], accent[1], accent[2], 90), width=1)
    
    # Top accent bar
    draw.rounded_rectangle([bx + 16, by + 12, bx + 50, by + 16], radius=2, fill=(accent[0], accent[1], accent[2], 255))
    
    # Heading & description
    draw.text((bx + 16, by + 26), heading, font=font_bold_badge, fill=(accent[0], accent[1], accent[2], 255))
    draw.text((bx + 16, by + 50), desc, font=font_body, fill=(203, 213, 225, 220))

# 9. Bottom Sponsor Bar
sponsor_bar_y = 710
draw.line([(80, sponsor_bar_y), (WIDTH - 80, sponsor_bar_y)], fill=(255, 255, 255, 25), width=1)
draw.text((80, sponsor_bar_y + 18), "PARTNERS & TECHNOLOGIES:", font=font_bold_badge, fill=(148, 163, 184, 200))

sponsors = [
    "Nasdaq",
    "Quantum Rings",
    "IonQ",
    "Sandia National Labs",
    "IBM Quantum",
    "Classiq",
    "qBraid"
]

sx = 340
for sp in sponsors:
    draw.rounded_rectangle([sx, sponsor_bar_y + 12, sx + len(sp) * 10 + 20, sponsor_bar_y + 38],
                           radius=6, fill=(30, 41, 59, 160), outline=(255, 255, 255, 25), width=1)
    draw.text((sx + 10, sponsor_bar_y + 17), sp, font=font_badge, fill=(241, 245, 249, 230))
    sx += len(sp) * 10 + 32

# Output files
out_path_png = Path(__file__).resolve().parent.parent / "docs" / "thumbnail_qfrontier.png"
out_path_jpg = Path(__file__).resolve().parent.parent / "docs" / "thumbnail_qfrontier.jpg"

# Convert to RGB for JPG
rgb_img = img.convert("RGB")
img.save(out_path_png, "PNG")
rgb_img.save(out_path_jpg, "JPEG", quality=95)

print(f"Generated PNG thumbnail: {out_path_png} ({out_path_png.stat().st_size / 1024:.1f} KB)")
print(f"Generated JPG thumbnail: {out_path_jpg} ({out_path_jpg.stat().st_size / 1024:.1f} KB)")
