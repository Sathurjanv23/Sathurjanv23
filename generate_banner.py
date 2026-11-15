"""
Generate pixel art animated banner in style of reference image:
- Dark purple night sky
- Pixel art portrait of Sathurjan
- Animated elements (stars, glow, scanlines)
- Text "hello_world()" 
- Purple color theme
"""

import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE = os.path.dirname(os.path.abspath(__file__))
AVATAR_PATH = os.path.join(BASE, "assets", "avatar.png")
ASSETS_DIR = os.path.join(BASE, "assets")

PURPLE_DARK   = (12,  8, 28)
PURPLE_MID    = (28, 15, 65)
PURPLE_BRIGHT = (60, 30, 130)
PURPLE_LIGHT  = (110, 60, 200)
PURPLE_GLOW   = (155, 95, 255)
MOON_COLOR    = (220, 200, 255)
STAR_COLOR    = (255, 255, 255)
PINK_ACCENT   = (255, 100, 180)
CYAN_ACCENT   = (80, 230, 255)
GOLD_ACCENT   = (255, 210, 60)
TEXT_WHITE    = (240, 230, 255)
TEXT_DIM      = (170, 150, 210)

W, H = 1200, 400

PIXEL = 4   # px per retro pixel

FONT_MONO = "C:/Windows/Fonts/consola.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_BODY = "C:/Windows/Fonts/segoeui.ttf"


def px(n):
    """snap to pixel grid"""
    return int(n) // PIXEL * PIXEL


def build_pixel_portrait():
    """Extract and pixelate Sathurjan with purple-tinted background."""
    avatar = Image.open(AVATAR_PATH).convert("RGB")
    crop = avatar.crop((60, 70, 400, 460))
    arr = np.array(crop).astype(np.float32)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    # Sky: G>160 and B>160 and B>(R+30)  -- true cyan-blue sky
    sky = (g > 160) & (b > 160) & (b > r + 30)
    # Buildings: sandy/beige regions - high R, mid G, mid B with low color variance
    bldg = (r > 165) & (g > 150) & (b > 130) & (np.abs(r-g) < 55) & ~sky
    # Pavement bottom: blueish grey
    road = (r > 165) & (g > 170) & (b > 185) & (b > r - 20) & (np.abs(r-g) < 30) & ~sky

    bg = sky | bldg | road

    new_r, new_g, new_b = r.copy(), g.copy(), b.copy()

    # Map background to dark purple palette
    bri = (r[bg] + g[bg] + b[bg]) / (3.0 * 255.0)
    new_r[bg] = (10 + 55 * bri**1.3).clip(0, 90)
    new_g[bg] = (5  + 20 * bri**1.5).clip(0, 40)
    new_b[bg] = (40 + 140 * bri**0.75).clip(0, 230)

    result = np.stack([new_r, new_g, new_b], axis=2).astype(np.uint8)
    img = Image.fromarray(result)

    # Boost contrast & saturation for vibrant pixel art look
    img = ImageEnhance.Contrast(img).enhance(1.55)
    img = ImageEnhance.Color(img).enhance(1.65)
    img = ImageEnhance.Sharpness(img).enhance(2.5)

    # Pixelate at PIXEL-size blocks
    pw, ph = img.size
    small = img.resize((pw // PIXEL, ph // PIXEL), Image.Resampling.LANCZOS)
    q = small.quantize(colors=56, dither=Image.Dither.NONE)
    rgb_q = q.convert("RGB")
    pixelated = rgb_q.resize((pw, ph), Image.Resampling.NEAREST)
    return pixelated   # 340 x 390


def draw_city_silhouette(draw, y_base, color=(30, 15, 70)):
    """Draw a simple pixel-art city skyline at the bottom."""
    buildings = [
        # (x, width, height)
        (0,   50, 60), (60,  30, 90), (100, 40, 50), (150, 60, 110),
        (220, 25, 70), (255, 35,  40),(300, 50, 130), (360, 30, 85),
        (400, 40, 60), (450, 60, 100),(520, 25, 50),  (555, 45, 80),
        (610, 30, 55), (650, 55, 95), (715, 40, 65),  (760, 30, 45),
        (800, 50, 120),(860, 35, 70), (905, 25, 55),  (940, 60, 85),
        (1010,30, 65), (1050,45,105), (1105,40,50),   (1155,45,70),
    ]
    for bx, bw, bh in buildings:
        # Main building
        draw.rectangle([bx, y_base - bh, bx + bw, y_base], fill=color)
        # Windows (lighter dots in a grid)
        for wy in range(y_base - bh + 8, y_base - 8, 12):
            for wx in range(bx + 5, bx + bw - 5, 10):
                lit = random.random() > 0.4
                wcol = (220, 200, 100) if lit else (50, 35, 90)
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=wcol)


def draw_moon(draw, cx, cy, radius=42):
    """Draw pixel-art moon."""
    for yy in range(cy - radius, cy + radius):
        for xx in range(cx - radius, cx + radius):
            d = math.sqrt((xx - cx)**2 + (yy - cy)**2)
            if d <= radius:
                # Base moon color
                t = 1.0 - d / radius
                lum = int(190 + 65 * t)
                col = (min(255, lum + 20), min(255, lum + 10), min(255, lum + 50))
                draw.point((xx, yy), fill=col)
    # Crater dots
    craters = [(cx - 10, cy - 8, 7), (cx + 12, cy + 10, 5), (cx - 5, cy + 15, 4)]
    for cxr, cyr, cr in craters:
        draw.ellipse([cxr - cr, cyr - cr, cxr + cr, cyr + cr], fill=(160, 145, 200))


def draw_stars(draw, seed=42):
    """Draw random twinkling stars."""
    rng = random.Random(seed)
    for _ in range(90):
        sx = rng.randint(10, W - 10)
        sy = rng.randint(5, H // 2 - 10)
        sz = rng.choice([1, 1, 1, 2])
        brightness = rng.randint(160, 255)
        col = (brightness, brightness - 10, brightness + 20)
        if sz == 1:
            draw.point((sx, sy), fill=col)
        else:
            draw.rectangle([sx, sy, sx + 1, sy + 1], fill=col)


def build_frame(portrait, frame_index, total_frames):
    """Build a single animation frame."""
    banner = Image.new("RGB", (W, H), PURPLE_DARK)
    draw = ImageDraw.Draw(banner)

    # --- Sky gradient ---
    for y in range(H):
        t = y / H
        rc = int(PURPLE_DARK[0] * (1 - t) + PURPLE_MID[0] * t)
        gc = int(PURPLE_DARK[1] * (1 - t) + PURPLE_MID[1] * t)
        bc = int(PURPLE_DARK[2] * (1 - t) + PURPLE_MID[2] * t)
        draw.line([(0, y), (W, y)], fill=(rc, gc, bc))

    # --- Stars (phase-shifted per frame for twinkle) ---
    rng = random.Random(42)
    for _ in range(90):
        sx = rng.randint(10, W - 10)
        sy = rng.randint(5, H // 2 - 10)
        sz = rng.choice([1, 1, 1, 2])
        phase = rng.random()
        # Twinkle: sin wave per frame
        t_val = math.sin(2 * math.pi * (frame_index / total_frames + phase))
        brightness = int(100 + 155 * (0.5 + 0.5 * t_val))
        col = (brightness, brightness - 10, min(255, brightness + 25))
        if sz == 1:
            draw.point((sx, sy), fill=col)
        else:
            draw.rectangle([sx, sy, sx + 1, sy + 1], fill=col)

    # --- Moon glow (pulsing) ---
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * frame_index / total_frames)
    moon_cx, moon_cy = 970, 90
    moon_r = 42
    glow_r = int(80 + 25 * pulse)
    for gr in range(glow_r, 0, -4):
        alpha_v = int(40 * (gr / glow_r) * pulse)
        gc = (max(0, 100 - alpha_v), max(0, 50 - alpha_v // 2), min(255, 170 + alpha_v))
        draw.ellipse([moon_cx - gr, moon_cy - gr, moon_cx + gr, moon_cy + gr], fill=gc)
    draw_moon(draw, moon_cx, moon_cy, moon_r)

    # --- City silhouette ---
    draw_city_silhouette(draw, H, color=PURPLE_MID)

    # --- Neon grid lines (perspective) ---
    grid_alpha = int(60 + 40 * math.sin(2 * math.pi * frame_index / total_frames * 0.5))
    grid_col = (20, grid_alpha // 3, grid_alpha)
    horizon_y = H - 100
    for xi in range(0, W + 100, 60):
        draw.line([(xi, horizon_y), (W // 2, H)], fill=grid_col, width=1)
    for yi_frac in [0.2, 0.4, 0.6, 0.8, 1.0]:
        yi = int(horizon_y + (H - horizon_y) * yi_frac)
        draw.line([(0, yi), (W, yi)], fill=grid_col, width=1)

    # --- Paste pixel-art portrait on right side ---
    # Portrait: 340x390; place at x:810, centered vertically
    pw, ph = portrait.size
    px_off = 820
    py_off = H - ph - 10
    banner.paste(portrait, (px_off, py_off))

    # Purple glow around portrait
    glow_col = (60 + int(30 * pulse), 20 + int(10 * pulse), 120 + int(50 * pulse))
    draw.rectangle([px_off - 4, py_off - 4, px_off + pw + 4, py_off + ph + 4],
                   outline=glow_col, width=2)

    # --- Typography ---
    try:
        f_tiny   = ImageFont.truetype(FONT_MONO, 14)
        f_code   = ImageFont.truetype(FONT_MONO, 20)
        f_name1  = ImageFont.truetype(FONT_BOLD, 58)
        f_name2  = ImageFont.truetype(FONT_BODY, 22)
        f_badge  = ImageFont.truetype(FONT_MONO, 13)
    except:
        f_tiny = f_code = f_name1 = f_name2 = f_badge = ImageFont.load_default()

    # hello_world() label
    draw.text((52, 50), "⬥  hello_world();", font=f_code, fill=PINK_ACCENT)

    # Main name
    draw.text((52, 94), "SATHURJAN", font=f_name1, fill=TEXT_WHITE)
    draw.text((52, 160), "VIJITHAKUMARASENA", font=f_name2, fill=(180, 155, 240))

    # Tagline
    draw.text((52, 200), "Full-Stack Developer  |  BSc IT @ University of Moratuwa", font=f_tiny, fill=TEXT_DIM)
    draw.text((52, 220), "Building Real-World Software Systems from Sri Lanka  🇱🇰", font=f_tiny, fill=TEXT_DIM)

    # Skill badge pills
    badges = [
        ("Software Engineering", PURPLE_BRIGHT, (200, 180, 255)),
        ("Full Stack", (60, 20, 100), (220, 160, 255)),
        ("AI / ML", (20, 50, 90),    (100, 200, 255)),
        ("Java & Spring Boot", (10, 50, 25), (80, 220, 130)),
        ("React & Next.js", (60, 25, 10),    (255, 150, 80)),
    ]
    bx, by = 52, 252
    for label, bg_col, text_col in badges:
        try:
            bbox = f_badge.getbbox(label)
            bw = bbox[2] - bbox[0] + 20
        except:
            bw = len(label) * 8 + 20
        bh = 24
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=4, fill=bg_col, outline=text_col, width=1)
        draw.text((bx + 10, by + 5), label, font=f_badge, fill=text_col)
        bx += bw + 8
        if bx > 720:
            bx = 52
            by += bh + 6

    # Connect badges row
    connect = [
        ("▶ LinkedIn", (20, 60, 150),   (100, 180, 255)),
        ("▶ GitHub",   (15, 15, 30),    (200, 200, 255)),
        ("▶ Email",    (100, 20, 20),   (255, 120, 120)),
    ]
    bx, by2 = 52, 345
    for label, bg_col, text_col in connect:
        try:
            bbox = f_badge.getbbox(label)
            bw = bbox[2] - bbox[0] + 24
        except:
            bw = len(label) * 8 + 24
        bh = 26
        draw.rounded_rectangle([bx, by2, bx + bw, by2 + bh], radius=13, fill=bg_col, outline=text_col, width=1)
        draw.text((bx + 12, by2 + 6), label, font=f_badge, fill=text_col)
        bx += bw + 10

    # Scanline overlay (retro CRT effect)
    if frame_index % 2 == 0:
        for scan_y in range(0, H, 4):
            draw.line([(0, scan_y), (W, scan_y)], fill=(0, 0, 0), width=1)

    # Animated cursor blink after name
    if frame_index % 2 == 0:
        cursor_x = 52 + 290  # approx after "SATHURJAN"
        draw.rectangle([cursor_x, 94, cursor_x + 5, 94 + 55], fill=PINK_ACCENT)

    return banner


def generate_animated_banner():
    print("Building pixel art portrait...")
    portrait = build_pixel_portrait()
    portrait_path = os.path.join(ASSETS_DIR, "portrait_pixel_art.png")
    portrait.save(portrait_path)

    print("Generating animation frames...")
    total_frames = 30
    frames = []
    for fi in range(total_frames):
        frame = build_frame(portrait, fi, total_frames)
        frames.append(frame)
        if fi % 5 == 0:
            print(f"  Frame {fi + 1}/{total_frames}")

    out_gif = os.path.join(ASSETS_DIR, "banner_animated.gif")
    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=80,       # ms per frame
        loop=0,
    )
    print(f"Saved animated GIF: {out_gif}")

    # Also save first frame as static PNG
    out_png = os.path.join(ASSETS_DIR, "banner.png")
    frames[0].save(out_png, format="PNG")
    print(f"Saved static banner: {out_png}")


if __name__ == "__main__":
    random.seed(0)
    generate_animated_banner()
