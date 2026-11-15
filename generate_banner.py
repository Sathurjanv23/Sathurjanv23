import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_banner():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    avatar_path = os.path.join(base_dir, "assets", "avatar.png")
    output_path = os.path.join(base_dir, "assets", "banner.png")
    
    W, H = 1200, 560
    
    # 1. Base dark background (deep obsidian with warm undertone)
    banner = Image.new("RGBA", (W, H), (13, 14, 18, 255))
    draw = ImageDraw.Draw(banner)
    
    # 2. Subtle dot grid texture
    grid_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_img)
    for x in range(32, W - 32, 22):
        for y in range(32, H - 32, 22):
            grid_draw.point((x, y), fill=(255, 255, 255, 14))
    banner = Image.alpha_composite(banner, grid_img)
    
    # 3. Ambient warm copper / amber radial glow on the right
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    gx, gy = 960, 280
    
    for r in range(450, 0, -4):
        t = 1.0 - (r / 450.0)
        alpha = int(115 * (t ** 2.4))
        r_col = 255
        g_col = int(85 + 55 * t)
        b_col = int(15 + 25 * t)
        g_draw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(r_col, g_col, b_col, alpha))
        
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    banner = Image.alpha_composite(banner, glow)
    
    # 4. Process Sathurjan's Avatar into Clean ASCII Matrix Portrait
    avatar = Image.open(avatar_path).convert("RGB")
    W_av, H_av = avatar.size
    
    # Accurate segmentation polygon for Sathurjan
    poly_pts = [
        (182, 130), (190, 105), (210, 90), (240, 80), (268, 82), (292, 95), (312, 115), (318, 145), (308, 175),
        (298, 200), (282, 235), (305, 245), 
        (325, 250), (355, 272), (370, 310), (365, 365), (355, 460),
        (85, 460),
        (75, 395), (70, 345), (80, 275), (115, 245), (145, 240),
        (170, 230), (165, 175), (172, 145)
    ]
    p_mask = Image.new("L", (W_av, H_av), 0)
    ImageDraw.Draw(p_mask).polygon(poly_pts, fill=255)
    p_mask = p_mask.filter(ImageFilter.GaussianBlur(3))
    p_arr = np.array(p_mask) / 255.0
    
    gray = avatar.convert("L")
    g_arr = np.array(gray).astype(np.float32)
    
    intensity = np.zeros_like(g_arr)
    # Hair & dark sunglasses: high density
    hair_mask = (g_arr < 80)
    intensity[hair_mask] = 255 - g_arr[hair_mask] * 1.5
    
    # Skin & facial features: mid density
    skin_mask = (g_arr >= 80) & (g_arr < 190)
    intensity[skin_mask] = 160 + (140 - np.abs(g_arr[skin_mask] - 130)) * 0.5
    
    # Shirt patterns & highlights
    shirt_mask = (g_arr >= 190)
    intensity[shirt_mask] = 110
    
    final_intensity = (intensity * p_arr).astype(np.uint8)
    
    # Vertical soft fade-out at bottom
    for y in range(370, 460):
        fade = 1.0 - ((y - 370) / 90.0) ** 1.6
        final_intensity[y, :] = (final_intensity[y, :] * fade).astype(np.uint8)
        
    # Crop to subject bounding box: x: 70..375, y: 75..460
    cropped = Image.fromarray(final_intensity).crop((68, 75, 375, 460))
    
    # Render ASCII matrix
    COLS = 68
    ROWS = 54
    small_subj = cropped.resize((COLS, ROWS), Image.Resampling.LANCZOS)
    subj_arr = np.array(small_subj)
    
    chars = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
    
    try:
        ascii_font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 9)
    except:
        ascii_font = ImageFont.load_default()
        
    ascii_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ascii_draw = ImageDraw.Draw(ascii_layer)
    
    # Position on right side of card
    start_x = 790
    start_y = 120
    dx = 5.6
    dy = 7.4
    
    for row in range(ROWS):
        for col in range(COLS):
            val = subj_arr[row, col]
            if val > 12:
                idx = int((val / 256.0) * len(chars))
                idx = min(idx, len(chars) - 1)
                ch = chars[idx]
                
                # Center is crisp white, edges softly tinted amber
                brightness = int(185 + 70 * (val / 255.0))
                r = brightness
                g = int(brightness * 0.95)
                b = int(brightness * 0.88)
                a = int(min(255, val * 1.55 + 30))
                
                px = start_x + col * dx
                py = start_y + row * dy
                ascii_draw.text((px, py), ch, font=ascii_font, fill=(r, g, b, a))
                
    banner = Image.alpha_composite(banner, ascii_layer)
    
    # 5. Draw sleek outer rounded border
    border_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(border_img)
    b_draw.rounded_rectangle([14, 14, W - 14, H - 14], radius=26, outline=(42, 45, 54, 230), width=2)
    banner = Image.alpha_composite(banner, border_img)
    
    # 6. Render Typography
    draw = ImageDraw.Draw(banner)
    
    font_mono_small = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
    font_pill = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
    font_name_sans = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 66)
    font_name_serif = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 62)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
    font_meta = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
    
    # Top-Left: SATHURJANV.DEV
    draw.text((68, 54), "SATHURJANV.DEV", font=font_mono_small, fill=(136, 142, 153, 255))
    
    # Top-Right: Open to internships pill
    pill_w = 210
    pill_h = 36
    pill_x1 = W - pill_w - 68
    pill_y1 = 48
    pill_x2 = pill_x1 + pill_w
    pill_y2 = pill_y1 + pill_h
    
    draw.rounded_rectangle([pill_x1, pill_y1, pill_x2, pill_y2], radius=18, fill=(22, 23, 29, 250), outline=(48, 51, 62, 255), width=1)
    
    # Glowing orange dot
    dot_cx = pill_x1 + 18
    dot_cy = (pill_y1 + pill_y2) // 2
    # Outer glow
    draw.ellipse([dot_cx - 6, dot_cy - 6, dot_cx + 6, dot_cy + 6], fill=(249, 115, 22, 60))
    # Core dot
    draw.ellipse([dot_cx - 4, dot_cy - 4, dot_cx + 4, dot_cy + 4], fill=(249, 115, 22, 255))
    draw.text((pill_x1 + 32, pill_y1 + 7), "Open to internships", font=font_pill, fill=(228, 228, 231, 255))
    
    # Main Headline
    # Line 1: Sathurjan
    draw.text((68, 136), "Sathurjan", font=font_name_sans, fill=(255, 255, 255, 255))
    # Line 2: Vijithakumarasena
    draw.text((68, 212), "Vijithakumarasena", font=font_name_serif, fill=(218, 220, 226, 255))
    
    # Subtitle
    draw.text((68, 318), "Full-stack developer, mostly on the backend.", font=font_sub, fill=(156, 163, 175, 255))
    draw.text((68, 350), "I build web platforms and see them through to production.", font=font_sub, fill=(156, 163, 175, 255))
    
    # Bottom metadata divider
    draw.line([(68, 442), (740, 442)], fill=(42, 45, 54, 220), width=1)
    
    # Bottom metadata line
    draw.text((68, 464), "BSC IT, UNIVERSITY OF MORATUWA  —  FULL-STACK & BACKEND  —  SRI LANKA", font=font_meta, fill=(120, 126, 138, 255))
    
    # Save optimized PNG
    banner.save(output_path, format="PNG", optimize=True)
    print(f"Generated refined banner at {output_path}")

if __name__ == "__main__":
    generate_banner()
