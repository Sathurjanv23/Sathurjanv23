"""
Professional Cyberpunk Purple Pixel Banner Renderer
Generates elite animated header.gif with pristine typography and flawless aesthetic.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
os.makedirs(ASSETS, exist_ok=True)

# ── COLOR PALETTE ─────────────────────────────────────────────────────────────
BG_DEEP     = (6,   4,  14)     # #06040E
BG_MID      = (14,  9,  28)     # #0E091C
BG_VIOLET   = (24, 14,  48)     # #180E30
P_PRIMARY   = (168, 85, 247)    # #A855F7
P_NEON      = (192, 132, 252)   # #C084FC
P_ELECTRIC  = (216, 180, 254)   # #D8B4FE
P_LAVENDER  = (243, 232, 255)   # #F3E8FF
P_DARK      = (45,  22,  90)     # #2D165A
P_BORDER    = (124, 58, 237)    # #7C3AED
CYAN        = (56, 189, 248)    # #38BDF8
PINK_NEON   = (244, 114, 182)   # #F472B6
GREEN_CODE  = (74, 222, 128)    # #4ADE80
TEXT_WHITE  = (248, 250, 252)   # #F8FAFC
TEXT_MUTED  = (161, 161, 170)   # #A1A1AA
TEXT_LILAC  = (216, 180, 254)   # #D8B4FE

# ── FONTS ─────────────────────────────────────────────────────────────────────
F_IMPACT  = "C:/Windows/Fonts/impact.ttf"
F_GOTHICB = "C:/Windows/Fonts/GOTHICB.TTF"
F_GOTHIC  = "C:/Windows/Fonts/GOTHIC.TTF"
F_CONSOLA = "C:/Windows/Fonts/consola.ttf"
F_SEGUIB  = "C:/Windows/Fonts/segoeuib.ttf"
F_SEGUI   = "C:/Windows/Fonts/segoeui.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_cyber_frame(draw, W, H, phase=0.0):
    """Draw ornate cyberpunk frame with corner brackets and telemetry tags."""
    m = 12  # margin
    glow_alpha = int(140 + 70 * math.sin(2 * math.pi * phase))
    frame_col = (*P_BORDER[:3], glow_alpha)
    bracket_col = (*P_NEON[:3], 240)

    # Outer border
    draw.rounded_rectangle([m, m, W - m, H - m], radius=6, outline=frame_col, width=1)
    
    # Corner brackets (L-shapes)
    blen = 22
    bthick = 2
    # Top-Left
    draw.line([(m, m + blen), (m, m), (m + blen, m)], fill=bracket_col, width=bthick)
    # Top-Right
    draw.line([(W - m - blen, m), (W - m, m), (W - m, m + blen)], fill=bracket_col, width=bthick)
    # Bottom-Left
    draw.line([(m, H - m - blen), (m, H - m), (m + blen, H - m)], fill=bracket_col, width=bthick)
    # Bottom-Right
    draw.line([(W - m - blen, H - m), (W - m, H - m), (W - m, H - m - blen)], fill=bracket_col, width=bthick)

    # Corner telemetry micro-text
    f_micro = get_font(F_CONSOLA, 10)
    draw.text((m + 28, m + 4), "// SYS.ID: MORA-SE", font=f_micro, fill=(*P_ELECTRIC[:3], 180))
    draw.text((W - m - 145, m + 4), "ARCH // ACTIVE [OK]", font=f_micro, fill=(*CYAN[:3], 190))
    draw.text((m + 28, H - m - 14), "LATITUDE: 6.7969° N • LONGITUDE: 79.9018° E", font=f_micro, fill=(*TEXT_MUTED[:3], 140))
    draw.text((W - m - 120, H - m - 14), "REV 2.8 // BUILD", font=f_micro, fill=(*P_NEON[:3], 170))

def draw_stars(draw, W, H, seed=101, n=90, phase=0.0):
    """Draw subtle twinkling stars on the canvas."""
    rng = random.Random(seed)
    for i in range(n):
        sx = rng.randint(20, W - 20)
        sy = rng.randint(18, H - 40)
        # Avoid stars right over the main title
        if 40 < sx < 550 and 50 < sy < 220:
            continue
        ph = rng.random()
        t = 0.5 + 0.5 * math.sin(2 * math.pi * (phase + ph))
        bri = int(80 + 175 * t)
        col = (bri, max(0, bri - 15), min(255, bri + 30), int(200 * t))
        
        # Cross flare for a few bright stars
        if i % 14 == 0 and t > 0.7:
            draw.line([(sx - 2, sy), (sx + 2, sy)], fill=col, width=1)
            draw.line([(sx, sy - 2), (sx, sy + 2)], fill=col, width=1)
        else:
            draw.point((sx, sy), fill=col)

def draw_moon(img, cx, cy, radius, phase=0.0):
    """Draw vibrant purple anime moon with soft multi-layered glow."""
    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_layer)

    pulse = 0.85 + 0.15 * math.sin(2 * math.pi * phase)
    # Outer diffuse aura
    for gr in range(int(radius * 2.8), radius, -4):
        alpha = int(22 * (1.0 - (gr - radius) / (radius * 1.8)) * pulse)
        gdraw.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=(*P_PRIMARY[:3], alpha))

    # Inner bright corona
    for gr in range(int(radius * 1.3), radius, -2):
        alpha = int(45 * (1.0 - (gr - radius) / (radius * 0.3)) * pulse)
        gdraw.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=(*P_ELECTRIC[:3], alpha))

    # Moon core disc
    mdisc = Image.new("RGBA", (radius * 2 + 10, radius * 2 + 10), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(mdisc)
    mcx, mcy = radius + 5, radius + 5
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            d = math.sqrt(dx * dx + dy * dy)
            if d <= radius:
                t = 1.0 - d / radius
                lum = int(210 + 45 * t)
                col = (min(255, lum), max(0, lum - 35), min(255, lum + 20), 255)
                mdraw.point((mcx + dx, mcy + dy), fill=col)
    
    # Stylized anime craters
    for crx, cry, crr in [(mcx - radius // 3, mcy - radius // 4, radius // 5),
                          (mcx + radius // 3, mcy + radius // 3, radius // 7),
                          (mcx - radius // 5, mcy + radius // 3, radius // 8)]:
        mdraw.ellipse([crx - crr, cry - crr, crx + crr, cry + crr], fill=(160, 110, 220, 180))

    glow_layer.paste(mdisc, (cx - mcx, cy - mcy), mdisc)
    img.alpha_composite(glow_layer)

def draw_anime_clouds(img, W, H, phase=0.0):
    """Draw elegant horizontal Japanese anime cloud bands."""
    cloud_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cloud_layer)

    bands = [
        # (base_y, height, speed_factor, alpha)
        (55,  18,  0.4, 60),
        (85,  22, -0.3, 75),
        (120, 26,  0.5, 90),
        (150, 20, -0.4, 70),
    ]

    for cy, ch, spd, a in bands:
        offset = int(phase * spd * 120) % W
        # Draw long flowing cloud strip on the right/upper half
        cx1 = (650 + offset) % (W + 200) - 100
        cw = 380
        # Rounded pill shape for anime cloud
        cdraw.rounded_rectangle([cx1, cy, cx1 + cw, cy + ch], radius=ch // 2,
                                fill=(*P_DARK[:3], a))
        # Inner lighter core
        cdraw.rounded_rectangle([cx1 + 25, cy + 3, cx1 + cw - 25, cy + ch - 3],
                                radius=(ch - 6) // 2, fill=(*P_PRIMARY[:3], int(a * 0.4)))

    img.alpha_composite(cloud_layer)

def draw_city_skyline(draw, W, H, ground_y=280):
    """
    Draw a clean, moody cyberpunk city skyline CONFINED TO THE RIGHT (x > 580).
    Leaves the left half completely pristine and dark for high-contrast typography!
    """
    # Background skyline buildings on right
    buildings = [
        # (x, w, h, col_idx)
        (580,  45, 110, 0),
        (630,  35, 150, 1),
        (670,  55, 130, 0),
        (730,  40, 180, 2),
        (775,  30, 95,  0),
        (810,  50, 140, 1),
        (865,  38, 165, 2),
        (910,  48, 120, 0),
        (965,  42, 190, 2),
        (1015, 36, 110, 0),
        (1055, 52, 145, 1),
        (1115, 45, 100, 0),
        (1165, 35, 135, 1),
    ]

    colors = [
        (18, 10, 36),  # deep shadow purple
        (26, 14, 52),  # mid purple silhouette
        (35, 18, 70),  # foreground purple silhouette
    ]

    rng = random.Random(42)
    for bx, bw, bh, cidx in buildings:
        by = ground_y - bh
        bcol = colors[cidx]
        draw.rectangle([bx, by, bx + bw, ground_y], fill=(*bcol, 255))
        # Roof antennas
        if bh > 140:
            draw.line([(bx + bw // 2, by - 18), (bx + bw // 2, by)], fill=(*P_PRIMARY[:3], 180), width=1)
            draw.point((bx + bw // 2, by - 19), fill=(*PINK_NEON[:3], 255))

        # Windows (subtle, delicate neon dots)
        for wy in range(by + 10, ground_y - 12, 14):
            for wx in range(bx + 6, bx + bw - 6, 8):
                if rng.random() > 0.55:
                    wcol = rng.choice([
                        (*P_ELECTRIC[:3], 180),
                        (*CYAN[:3], 190),
                        (*PINK_NEON[:3], 170),
                        (255, 235, 150, 190),
                    ])
                    draw.rectangle([wx, wy, wx + 3, wy + 5], fill=wcol)

def draw_developer_workspace(draw, W, H, phase=0.0):
    """Draw futuristic developer workstation on the right (x=900 to 1120)."""
    dx = 910
    dy = 205

    # 1. Main Curved Ultra-wide Monitor
    mw, mh = 145, 82
    draw.rounded_rectangle([dx, dy, dx + mw, dy + mh], radius=5, fill=(10, 6, 22), outline=(*P_PRIMARY[:3], 200), width=1)
    
    # Code editor syntax lines on main screen
    code_colors = [CYAN, P_NEON, GREEN_CODE, PINK_NEON, P_LAVENDER, CYAN, P_PRIMARY]
    rng = random.Random(88)
    for i in range(7):
        ly = dy + 10 + i * 9
        lx = dx + 12
        # Indents
        indent = (i % 3) * 12
        line_w = rng.randint(45, 95)
        col = code_colors[i % len(code_colors)]
        draw.line([(lx + indent, ly), (lx + indent + line_w, ly)], fill=(*col[:3], 220), width=2)
    
    # Blinking cursor on terminal
    if int(phase * 12) % 2 == 0:
        draw.rectangle([dx + 12, dy + 70, dx + 18, dy + 76], fill=(*P_ELECTRIC[:3], 255))

    # 2. Secondary Vertical Monitor on Left
    sw, sh = 52, 92
    sx = dx - 60
    sy = dy - 6
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=4, fill=(10, 6, 22), outline=(*P_BORDER[:3], 170), width=1)
    
    # Vertical architecture node graph / telemetry
    for i in range(5):
        ny = sy + 14 + i * 15
        draw.rectangle([sx + 8, ny, sx + sw - 8, ny + 8], fill=(*P_DARK[:3], 200))
        draw.line([(sx + 14, ny + 4), (sx + sw - 14, ny + 4)], fill=(*CYAN[:3], 180), width=1)

    # 3. Desk Surface with Neon Underglow
    desk_y = dy + mh + 12
    draw.rectangle([dx - 80, desk_y, dx + mw + 40, desk_y + 12], fill=(16, 10, 32))
    # Ambient desk glow strip
    draw.line([(dx - 80, desk_y), (dx + mw + 40, desk_y)], fill=(*P_NEON[:3], 240), width=2)
    for gr in [2, 4]:
        draw.line([(dx - 80, desk_y + gr), (dx + mw + 40, desk_y + gr)], fill=(*P_PRIMARY[:3], 120 // gr), width=1)

    # 4. Developer Character (Silhouette / Anime Back View)
    cx = dx + mw // 2 - 12
    cy = desk_y - 20
    # Head & Headphones
    draw.ellipse([cx, cy - 26, cx + 24, cy - 2], fill=(22, 14, 44))
    # Hair spikes
    draw.polygon([(cx + 2, cy - 20), (cx + 6, cy - 34), (cx + 12, cy - 24)], fill=(15, 8, 30))
    draw.polygon([(cx + 10, cy - 24), (cx + 18, cy - 35), (cx + 22, cy - 20)], fill=(15, 8, 30))
    # Headphones band & earcups
    draw.arc([cx - 2, cy - 28, cx + 26, cy - 4], start=180, end=0, fill=(*P_NEON[:3], 240), width=2)
    draw.ellipse([cx - 4, cy - 18, cx, cy - 6], fill=(*CYAN[:3], 240))
    draw.ellipse([cx + 24, cy - 18, cx + 28, cy - 6], fill=(*CYAN[:3], 240))
    # Torso (Hoodie / Jacket)
    draw.rounded_rectangle([cx - 14, cy - 2, cx + 38, cy + 24], radius=6, fill=(30, 16, 60))
    draw.line([(cx + 12, cy), (cx + 12, cy + 24)], fill=(*P_PRIMARY[:3], 200), width=1)

def render_frame(fi, total_frames):
    W, H = 1200, 350
    phase = fi / total_frames

    # Base Canvas with Deep Gradient
    img = Image.new("RGBA", (W, H), (*BG_DEEP, 255))
    draw = ImageDraw.Draw(img)

    # 1. Sky Gradient (Vertical)
    for y in range(H):
        t = y / H
        r = int(BG_DEEP[0] + (BG_VIOLET[0] - BG_DEEP[0]) * (t**0.75))
        g = int(BG_DEEP[1] + (BG_VIOLET[1] - BG_DEEP[1]) * (t**0.75))
        b = int(BG_DEEP[2] + (BG_VIOLET[2] - BG_DEEP[2]) * (t**0.75))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # 2. Left Side Pristine Dark Backdrop (Vignette)
    # Ensures 100% contrast behind typography
    for x in range(650):
        t = x / 650
        alpha = int(220 * (1.0 - t**1.4))
        draw.line([(x, 0), (x, H)], fill=(*BG_DEEP[:3], alpha))

    # 3. Ground Perspective Grid at Bottom (y: 280 -> 350)
    for gy in range(280, H, 14):
        draw.line([(0, gy), (W, gy)], fill=(*P_BORDER[:3], 35), width=1)
    for gx in range(0, W, 40):
        draw.line([(gx, 280), (int(gx * 1.15) - 80, H)], fill=(*P_BORDER[:3], 25), width=1)

    # 4. Celestial Elements: Stars & Moon
    draw_stars(draw, W, H, seed=777, n=110, phase=phase)
    draw_moon(img, cx=1060, cy=72, radius=44, phase=phase)

    # Re-acquire draw after composite
    draw = ImageDraw.Draw(img)

    # 5. Stylized Anime Clouds
    draw_anime_clouds(img, W, H, phase=phase)
    draw = ImageDraw.Draw(img)

    # 6. City Skyline (Right side only)
    draw_city_skyline(draw, W, H, ground_y=280)

    # 7. Developer Workstation
    draw_developer_workspace(draw, W, H, phase=phase)

    # 8. Cyberpunk Frame & Telemetry
    draw_cyber_frame(draw, W, H, phase=phase)

    # ── TYPOGRAPHY: PRISTINE, HIGH-CONTRAST & CRISP ────────────────────────────
    # Fonts
    f_sys     = get_font(F_CONSOLA, 13)
    f_name1   = get_font(F_IMPACT, 70)
    f_name2   = get_font(F_GOTHICB, 24)
    f_role    = get_font(F_GOTHICB, 18)
    f_campus  = get_font(F_CONSOLA, 14)
    f_tagline = get_font(F_CONSOLA, 13)
    f_badge   = get_font(F_CONSOLA, 11)

    # Line 1: IDE Terminal Code Prompt
    code_phase = phase
    col_code = (
        int(190 + 55 * math.sin(2 * math.pi * code_phase)),
        int(130 + 40 * math.sin(2 * math.pi * code_phase + 1)),
        int(240 + 15 * math.sin(2 * math.pi * code_phase + 2))
    )
    draw.text((54, 34), "> system.initialize(domain=\"software_engineering\");", font=f_sys, fill=col_code)

    # Line 2: First Name SATHURJAN with Smooth Neon Drop-Shadow
    tx, ty = 54, 58
    # Subtle diffuse glow behind text (not blocky!)
    for off_x, off_y, a in [(-2, 0, 90), (2, 0, 90), (0, -2, 90), (0, 2, 90), (0, 0, 160)]:
        draw.text((tx + off_x, ty + off_y), "SATHURJAN", font=f_name1, fill=(*P_PRIMARY[:3], a))
    # Crisp foreground text
    draw.text((tx, ty), "SATHURJAN", font=f_name1, fill=P_LAVENDER)

    # Line 3: Surname VIJITHAKUMARASENA
    ty_last = ty + 74
    draw.text((tx + 2, ty_last), "VIJITHAKUMARASENA", font=f_name2, fill=P_NEON)

    # Line 4: Role & Specialization Subtitle
    ty_role = ty_last + 34
    draw.text((tx + 2, ty_role), "SOFTWARE ENGINEERING UNDERGRADUATE", font=f_role, fill=P_ELECTRIC)

    # Line 5: University of Moratuwa | Sri Lanka
    ty_campus = ty_role + 26
    draw.text((tx + 2, ty_campus), "University of Moratuwa  •  Sri Lanka  🇱🇰", font=f_campus, fill=TEXT_LILAC)

    # Line 6: Typewriter Tagline with Blinking Cursor
    ty_tag = ty_campus + 26
    tag_full = "BUILD  •  ARCHITECT  •  INNOVATE"
    chars = int(len(tag_full) * min(1.0, (phase * 1.6) % 1.0 + 0.35))
    tag_sub = tag_full[:chars]
    cursor = "▮" if int(phase * 12) % 2 == 0 else "▯"
    draw.text((tx + 2, ty_tag), f"{tag_sub} {cursor}", font=f_tagline, fill=PINK_NEON)

    # Line 7: Premium Dark Pill Badges
    badges = ["Software Engineering", "Full-Stack Dev", "Backend Architecture", "AI & ML"]
    bx = tx + 2
    by = ty_tag + 28
    for i, btext in enumerate(badges):
        bw = len(btext) * 7 + 18
        bh = 22
        # Pill background
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=4,
                               fill=(18, 10, 36, 230), outline=(*P_PRIMARY[:3], 200), width=1)
        draw.text((bx + 9, by + 4), btext, font=f_badge, fill=P_LAVENDER)
        bx += bw + 8

    return img.convert("RGB")

def generate_header_gif(total_frames=36):
    print(f"Generating Professional Header GIF ({total_frames} frames)...")
    frames = []
    for fi in range(total_frames):
        f = render_frame(fi, total_frames)
        frames.append(f)
        if fi % 6 == 0:
            print(f"  frame {fi + 1}/{total_frames}")

    out_gif = os.path.join(ASSETS, "header.gif")
    out_png = os.path.join(ASSETS, "header_preview.png")

    # Save static preview of frame 0
    frames[0].save(out_png, format="PNG")
    print(f"Saved preview: {out_png}")

    # Quantize and save GIF
    q_frames = [f.quantize(colors=192, dither=Image.Dither.FLOYDSTEINBERG) for f in frames]
    q_frames[0].save(
        out_gif,
        save_all=True,
        append_images=q_frames[1:],
        optimize=True,
        duration=65,
        loop=0
    )
    print(f"Saved GIF: {out_gif} ({os.path.getsize(out_gif) // 1024} KB)")

def render_footer_frame(fi, total_frames):
    W, H = 1200, 160
    phase = fi / total_frames

    img = Image.new("RGBA", (W, H), (*BG_DEEP, 255))
    draw = ImageDraw.Draw(img)

    # 1. Sky Gradient
    for y in range(H):
        t = y / H
        r = int(BG_DEEP[0] + (BG_VIOLET[0] - BG_DEEP[0]) * (t**0.8))
        g = int(BG_DEEP[1] + (BG_VIOLET[1] - BG_DEEP[1]) * (t**0.8))
        b = int(BG_DEEP[2] + (BG_VIOLET[2] - BG_DEEP[2]) * (t**0.8))
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # 2. Stars
    draw_stars(draw, W, H - 40, seed=999, n=60, phase=phase)

    # 3. Small Moon on Right
    draw_moon(img, cx=1080, cy=42, radius=24, phase=phase)
    draw = ImageDraw.Draw(img)

    # 4. Skyline silhouette along bottom
    skyline_pts = [
        (0, 120), (50, 95), (90, 120), (140, 85), (200, 120),
        (260, 100), (310, 120), (370, 90), (430, 120), (500, 95),
        (560, 120), (620, 85), (680, 120), (740, 100), (800, 120),
        (860, 90), (920, 120), (980, 85), (1040, 120), (1100, 95),
        (1160, 120), (1200, 120)
    ]
    # Draw silhouette
    draw.polygon([(0, H)] + skyline_pts + [(W, H)], fill=(16, 9, 32))
    draw.line(skyline_pts, fill=(*P_BORDER[:3], 180), width=1)

    # 5. Cyber frame & corner brackets
    m = 8
    glow_alpha = int(130 + 60 * math.sin(2 * math.pi * phase))
    draw.rounded_rectangle([m, m, W - m, H - m], radius=4, outline=(*P_BORDER[:3], glow_alpha), width=1)
    # Brackets
    blen = 14
    draw.line([(m, m + blen), (m, m), (m + blen, m)], fill=(*P_NEON[:3], 220), width=2)
    draw.line([(W - m - blen, m), (W - m, m), (W - m, m + blen)], fill=(*P_NEON[:3], 220), width=2)
    draw.line([(m, H - m - blen), (m, H - m), (m + blen, H - m)], fill=(*P_NEON[:3], 220), width=2)
    draw.line([(W - m - blen, H - m), (W - m, H - m), (W - m, H - m - blen)], fill=(*P_NEON[:3], 220), width=2)

    # 6. Centered Closing Message with diffuse glow
    f_msg1 = get_font(F_GOTHICB, 18)
    f_msg2 = get_font(F_CONSOLA, 12)

    msg1 = "Keep Building.  Keep Learning.  Keep Growing."
    try:
        bbox1 = f_msg1.getbbox(msg1)
        w1 = bbox1[2] - bbox1[0]
    except:
        w1 = len(msg1) * 11
    x1 = (W - w1) // 2
    y1 = 52

    # Glow
    for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        draw.text((x1 + ddx, y1 + ddy), msg1, font=f_msg1, fill=(*P_PRIMARY[:3], 120))
    draw.text((x1, y1), msg1, font=f_msg1, fill=P_LAVENDER)

    msg2 = "SATHURJAN VIJITHAKUMARASENA  //  SOFTWARE ENGINEERING UNDERGRADUATE  •  UNIVERSITY OF MORATUWA"
    try:
        bbox2 = f_msg2.getbbox(msg2)
        w2 = bbox2[2] - bbox2[0]
    except:
        w2 = len(msg2) * 7
    x2 = (W - w2) // 2
    y2 = y1 + 32
    draw.text((x2, y2), msg2, font=f_msg2, fill=(*P_ELECTRIC[:3], 200))

    return img.convert("RGB")

def generate_footer_gif(total_frames=24):
    print(f"Generating Professional Footer GIF ({total_frames} frames)...")
    frames = []
    for fi in range(total_frames):
        f = render_footer_frame(fi, total_frames)
        frames.append(f)

    out_gif = os.path.join(ASSETS, "footer.gif")
    q_frames = [f.quantize(colors=160, dither=Image.Dither.FLOYDSTEINBERG) for f in frames]
    q_frames[0].save(
        out_gif,
        save_all=True,
        append_images=q_frames[1:],
        optimize=True,
        duration=70,
        loop=0
    )
    print(f"Saved Footer GIF: {out_gif} ({os.path.getsize(out_gif) // 1024} KB)")

if __name__ == "__main__":
    generate_header_gif(total_frames=36)
    generate_footer_gif(total_frames=24)
