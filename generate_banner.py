"""
PURPLE PIXEL UNIVERSE — Complete Artwork Generator
Creates: header.gif, footer.gif, anime-avatar.png, project thumbnails
"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
PROJECTS = os.path.join(ASSETS, "projects")
os.makedirs(PROJECTS, exist_ok=True)

# ── PALETTE ───────────────────────────────────────────────────────────────────
BG0         = (8,   7,  17)   # deepest background
BG1         = (11,  9,  25)
BG2         = (17, 12,  38)
BG3         = (26, 18,  58)
P_DARK      = (40, 20,  90)
P_MID       = (80, 40, 160)
P_BRIGHT    = (140, 70, 230)
P_PRIMARY   = (168, 85, 247)
P_NEON      = (192,132, 252)
P_LAVEN     = (233,213, 255)
P_PINK      = (240,171, 252)
MOON_COLOR  = (220,195, 255)
STAR_W      = (255,255,255)
TEXT_WHITE  = (248,250,252)
TEXT_DIM    = (161,161,170)
GOLD        = (255,215, 60)
CYAN        = ( 56,189,248)
GREEN_NEO   = ( 74,222,128)

# ── FONTS ─────────────────────────────────────────────────────────────────────
FIMPACT  = "C:/Windows/Fonts/impact.ttf"
FGOTHICB = "C:/Windows/Fonts/GOTHICB.TTF"
FGOTHIC  = "C:/Windows/Fonts/GOTHIC.TTF"
FCONSOLA = "C:/Windows/Fonts/consola.ttf"
FSEGUI   = "C:/Windows/Fonts/segoeui.ttf"
FSEGOUB  = "C:/Windows/Fonts/segoeuib.ttf"

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def lerp(a, b, t):
    return int(a + (b - a) * t)

def lerp3(ca, cb, t):
    return (lerp(ca[0],cb[0],t), lerp(ca[1],cb[1],t), lerp(ca[2],cb[2],t))

def sky_gradient(draw, W, H, sky_h, top=(8,5,20), mid=(20,10,55), bot=(35,18,90)):
    for y in range(sky_h):
        t = y / sky_h
        if t < 0.5:
            c = lerp3(top, mid, t*2)
        else:
            c = lerp3(mid, bot, (t-0.5)*2)
        draw.line([(0,y),(W,y)], fill=c)

def draw_moon(draw, cx, cy, R, pulse=1.0):
    # outer glow rings
    for gr in range(int(R*2.5), 0, -4):
        a = int(28 * (1 - gr/(R*2.5)) * pulse)
        gc = (max(0,80-gr), max(0,30-gr//2), min(255,120+gr//2))
        draw.ellipse([cx-gr,cy-gr,cx+gr,cy+gr], fill=gc)
    # moon disc
    for dy in range(-R, R+1):
        for dx in range(-R, R+1):
            d = math.sqrt(dx*dx+dy*dy)
            if d <= R:
                t = 1 - d/R
                lum = int(170 + 85*t)
                col = (max(0,lum-30), max(0,lum-100), min(255,lum+15))
                draw.point((cx+dx, cy+dy), fill=col)
    # subtle craters
    for cxr,cyr,cr in [(cx-R//3,cy-R//4,R//6),(cx+R//4,cy+R//3,R//8)]:
        draw.ellipse([cxr-cr,cyr-cr,cxr+cr,cyr+cr], fill=(140,100,200))

def draw_stars(draw, W, H_sky, seed, n=120, phase=0.0):
    rng = random.Random(seed)
    for _ in range(n):
        sx = rng.randint(5, W-5)
        sy = rng.randint(5, H_sky-5)
        ph = rng.random()
        sz = rng.choice([1,1,1,2])
        t = 0.5 + 0.5*math.sin(2*math.pi*(phase + ph))
        bri = int(90 + 165*t)
        col = (bri, bri-10, min(255,bri+30))
        if sz==1:
            draw.point((sx,sy), fill=col)
        else:
            draw.rectangle([sx,sy,sx+1,sy+1], fill=col)

def draw_city(draw, W, ground_y, seed=7):
    rng = random.Random(seed)
    x = 0
    while x < W:
        bw = rng.randint(28, 70)
        bh = rng.randint(55, 180)
        # building body
        shade = rng.choice([(14,8,32),(18,10,42),(22,13,52),(28,15,65)])
        draw.rectangle([x, ground_y-bh, x+bw, ground_y], fill=shade)
        # windows
        for wy in range(ground_y-bh+8, ground_y-6, 11):
            for wx in range(x+5, x+bw-5, 10):
                lit = rng.random()
                if lit > 0.45:
                    wc = rng.choice([(220,195,100),(180,140,255),(100,200,255),(255,160,80)])
                elif lit > 0.2:
                    wc = (40,25,80)
                else:
                    wc = (20,12,38)
                draw.rectangle([wx,wy,wx+5,wy+6], fill=wc)
        # rooftop details
        if bw > 40:
            draw.rectangle([x+bw//2-2,ground_y-bh-8,x+bw//2+2,ground_y-bh], fill=P_BRIGHT)
        x += bw + rng.randint(2,8)

def draw_ground_grid(draw, W, H, ground_y):
    # Neon perspective grid
    horizon = ground_y
    vanish_x = W // 2
    # vertical lines
    for xi in range(-W, W*2, 48):
        draw.line([(xi, horizon),(vanish_x + (xi - vanish_x)*3, H)], fill=(30,8,80), width=1)
    # horizontal lines
    for frac in [0.1,0.25,0.45,0.65,0.82,1.0]:
        yi = int(horizon + (H-horizon)*frac)
        draw.line([(0,yi),(W,yi)], fill=(35,10,90), width=1)

def draw_glow_text(draw, x, y, text, fnt, main_col, glow_col, glow_r=10):
    for r in [glow_r, glow_r//2, glow_r//4]:
        for dx in range(-r, r+1, max(1,r//3)):
            for dy in range(-r, r+1, max(1,r//3)):
                if dx==0 and dy==0: continue
                if abs(dx)+abs(dy) <= r:
                    draw.text((x+dx,y+dy), text, font=fnt, fill=(*glow_col, 40))
    draw.text((x,y), text, font=fnt, fill=main_col)

def draw_pixel_char(draw, cx, cy, scale=1):
    """Draw a simple pixel-art anime developer character (front-view, seated)."""
    s = scale
    # Skin tone
    skin = (200, 155, 120)
    skin2 = (180, 130, 95)
    dark  = (20, 10, 35)
    hair  = (30, 20, 55)
    shirt = (60, 30, 120)
    shirt2= (80, 45, 160)
    eye_w = (220, 210, 255)
    eye_p = (140, 80, 255)
    glow_col = (160, 90, 255)
    
    def r(x,y,w,h,col): 
        draw.rectangle([cx+x*s, cy+y*s, cx+(x+w)*s-1, cy+(y+h)*s-1], fill=col)
    def p(x,y,col):
        draw.rectangle([cx+x*s,cy+y*s,cx+(x+1)*s-1,cy+(y+1)*s-1], fill=col)

    # === HAIR (spiky anime) ===
    # Main hair block
    r(-6,-16,12,8, hair)
    # Spikes
    for sx, sy2, sw, sh in [(-8,-20,3,5),(-5,-22,4,7),(0,-23,4,8),(5,-21,4,6),(8,-18,3,4)]:
        r(sx,sy2,sw,abs(sh), hair)
    # Side hair
    r(-8,-12,3,10, hair)
    r(5,-12,3,10, hair)
    
    # === FACE ===
    r(-5,-10,10,10, skin)
    # Cheeks
    r(-5,-6,2,3, skin2)
    r(3,-6,2,3, skin2)
    # Eyes
    r(-4,-9,3,3, dark)
    r(1,-9,3,3, dark)
    r(-3,-8,1,1, eye_w)
    r(2,-8,1,1, eye_w)
    r(-3,-9,2,2, eye_p)
    r(2,-9,2,2, eye_p)
    # Highlight in eyes
    r(-3,-9,1,1, (255,240,255))
    r(2,-9,1,1,  (255,240,255))
    # Nose
    r(-1,-6,1,1, skin2)
    # Mouth (slight smile)
    r(-2,-4,1,1, skin2)
    r(-1,-3,4,1, skin2)
    r(2,-4,1,1, skin2)
    
    # Neck
    r(-2,0,4,3, skin)
    
    # === BODY / SHIRT ===
    r(-8,3,16,12, shirt)
    r(-8,3,3,12, shirt2)   # left shading
    r(5,3,3,12, shirt2)    # right shading
    # Collar
    r(-2,2,2,4, (40,20,80))
    r(0,2,2,4, (40,20,80))
    
    # Shoulders
    r(-10,3,2,8, shirt2)
    r(8,3,2,8, shirt2)
    
    # Arms (resting on desk)
    r(-10,8,4,8, skin)   # left arm
    r(6,8,4,8, skin)     # right arm
    
    # Hands on keyboard
    r(-10,14,5,4, skin)
    r(5,14,5,4, skin)
    
    # Headphones hint
    r(-8,-15,2,6, (90,50,180))
    r(6,-15,2,6, (90,50,180))
    r(-7,-16,14,2, (90,50,180))

def draw_desk(draw, cx, cy, W_desk, s=1):
    """Draw a futuristic pixel-art desk with monitors."""
    dark_desk = (25, 15, 55)
    desk_top  = (35, 20, 75)
    mon_frame = (30, 20, 65)
    mon_scrn  = (10, 5, 25)
    glow_grn  = (80, 255, 150)
    glow_pur  = (160, 80, 255)
    glow_cya  = (50, 200, 255)
    
    def r(x,y,w,h,col):
        draw.rectangle([x,y,x+w-1,y+h-1], fill=col)
    
    # Desk surface
    r(cx - W_desk//2, cy, W_desk, 8*s, desk_top)
    r(cx - W_desk//2, cy+8*s, W_desk, 4*s, dark_desk)
    
    # Left monitor
    ml_x = cx - W_desk//2 + 15*s
    ml_y = cy - 55*s
    r(ml_x, ml_y, 70*s, 50*s, mon_frame)
    r(ml_x+3*s, ml_y+3*s, 64*s, 44*s, mon_scrn)
    # Screen content (code lines)
    for i, (ly, lc) in enumerate([(6,glow_grn),(12,(100,180,255)),(18,glow_grn),(24,(200,120,255)),(30,glow_grn),(36,(100,180,255))]):
        lw = random.Random(i*7).randint(20,55)
        r(ml_x+5*s, ml_y+ly*s, lw*s, 2*s, (*lc[:3], 180))
    # Monitor glow
    for gr in range(10,0,-2):
        draw.rectangle([ml_x-gr, ml_y-gr, ml_x+70*s+gr, ml_y+50*s+gr], outline=glow_cya, width=1)
    # Monitor stand (removed zero-height rect)
    # stand already grounded on desk surface
    
    # Right monitor (main, larger)
    mr_x = cx + 10*s
    mr_y = cy - 70*s
    r(mr_x, mr_y, 90*s, 65*s, mon_frame)
    r(mr_x+3*s, mr_y+3*s, 84*s, 59*s, mon_scrn)
    # Code editor on screen
    for i, (ly, lc, lw) in enumerate([
        (5,glow_pur,30),(9,(150,200,255),45),(13,glow_grn,38),(17,(100,170,255),25),
        (21,glow_pur,42),(25,glow_grn,33),(29,(180,130,255),50),(33,glow_cya,28),
        (37,glow_pur,38),(41,(100,200,255),44),(45,glow_grn,30),(50,glow_cya,55),
    ]):
        r(mr_x+5*s, mr_y+ly*s, lw*s, 2*s, lc)
    # Blinking cursor block
    r(mr_x+5*s+30*s, mr_y+50*s, 4*s, 8*s, (220,180,255))
    # Monitor glow
    for gr in range(14,0,-2):
        a_frac = 1 - gr/14
        gc = (int(80*a_frac), int(30*a_frac), int(160*a_frac))
        draw.rectangle([mr_x-gr, mr_y-gr, mr_x+90*s+gr, mr_y+65*s+gr], outline=gc, width=1)
    
    # Keyboard
    kb_x = cx - 40*s
    kb_y = cy + 2*s
    r(kb_x, kb_y, 80*s, 5*s, (45,28,95))
    # Key rows
    for ki in range(8):
        r(kb_x+ki*9*s+2*s, kb_y+1*s, 7*s, 3*s, (60,38,120))

    # Small accent items on desk
    r(cx+W_desk//2-30*s, cy-15*s, 12*s, 15*s, (30,18,65))  # mug
    r(cx+W_desk//2-28*s, cy-13*s, 8*s, 11*s, (20,100,180))  # mug inside
    # Steam from mug
    for si in range(3):
        r(cx+W_desk//2-26*s+si*3*s, cy-18*s-si*2*s, 1*s, 2*s, (180,180,220))


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER GIF — 1200×350
# ═══════════════════════════════════════════════════════════════════════════════

def build_header_frame(frame_index, total_frames):
    W, H = 1200, 350
    SKY_H = 240
    GROUND_Y = 240
    img = Image.new("RGBA", (W, H), (*BG0, 255))
    draw = ImageDraw.Draw(img)
    
    phase = frame_index / total_frames

    # Sky gradient
    for y in range(SKY_H):
        t = y / SKY_H
        c = lerp3(BG0, BG2, t**0.7)
        draw.line([(0,y),(W,y)], fill=(*c,255))

    # Ground fill
    for y in range(GROUND_Y, H):
        t = (y - GROUND_Y) / (H - GROUND_Y)
        c = lerp3(BG1, BG0, t)
        draw.line([(0,y),(W,y)], fill=(*c,255))

    # Perspective grid on ground
    draw_ground_grid(draw, W, H, GROUND_Y)

    # Stars (twinkling)
    draw_stars(draw, W, SKY_H - 20, seed=1234, n=140, phase=phase)

    # Moon (pulsing glow)
    pulse = 0.75 + 0.25*math.sin(2*math.pi*phase)
    draw_moon(draw, 980, 65, 45, pulse)

    # Purple clouds (slow drift)
    cloud_offset = int(phase * 80) % W
    for cxi, cyi, cri in [(300,45,30),(500,30,20),(700,55,25),(900,38,18),(200,60,22),(1050,42,16)]:
        cx_shifted = (cxi - cloud_offset) % W
        for puff_dx in [-20,-5,10]:
            cr = cri - abs(puff_dx)//5
            for gy in range(-cr, cr+1):
                for gx in range(-cr, cr+1):
                    d = math.sqrt(gx*gx+gy*gy)
                    if d <= cr:
                        t = 1-d/cr
                        a = int(50*t*(0.6+0.4*pulse))
                        col = (int(60*t),int(20*t),int(130*t))
                        draw.point(((cx_shifted+puff_dx+gx)%W, cyi+gy), fill=col)

    # Floating particles
    rng = random.Random(42)
    for _ in range(55):
        px = rng.randint(0, W)
        py = rng.randint(10, SKY_H-10)
        pphase = rng.random()
        psize = rng.randint(1,3)
        t = 0.4 + 0.6*math.sin(2*math.pi*(phase*1.3+pphase))
        pc = rng.choice([(P_PRIMARY,t),(P_PINK,t),(P_LAVEN,t*0.5)])
        col,alpha = pc
        bri = int(alpha*200)
        if bri > 20:
            drift_x = int(rng.choice([-1,1]) * 15 * math.sin(2*math.pi*(phase+pphase)))
            drift_y = int(8 * math.sin(2*math.pi*(phase*0.7+pphase)))
            ppx = (px + drift_x) % W
            ppy = max(0, min(SKY_H-1, py + drift_y))
            if psize == 1:
                draw.point((ppx, ppy), fill=(*col[:3], bri))
            else:
                draw.ellipse([ppx-psize//2, ppy-psize//2, ppx+psize//2, ppy+psize//2],
                             fill=(*col[:3], bri))

    # City silhouette
    draw_city(draw, W, GROUND_Y, seed=99)

    # ── DESK SCENE (centered right half) ──────────────────────────────────────
    char_cx = 820
    char_cy = GROUND_Y - 20
    s = 2  # scale factor

    draw_desk(draw, char_cx, char_cy, 220, s)
    draw_pixel_char(draw, char_cx, char_cy - 2*s, s)

    # Scanline on character (subtle retro)
    if frame_index % 3 == 0:
        for scan_y in range(char_cy - 85*s, char_cy + 20*s, 4):
            if 0 <= scan_y < H:
                draw.line([(char_cx - 120, scan_y),(char_cx + 120, scan_y)], fill=(0,0,0,30))

    # Blinking cursor on big monitor (alternating frames)
    mr_x = char_cx + 10*s
    mr_y = char_cy - 70*s
    if (frame_index // 4) % 2 == 0:
        draw.rectangle([mr_x+5*s+30*s, mr_y+50*s, mr_x+5*s+34*s, mr_y+58*s], fill=(220,180,255,220))

    # ── LEFT SIDE TEXT ────────────────────────────────────────────────────────
    f_name = font(FIMPACT, 86)
    f_sub  = font(FGOTHICB, 22)
    f_tag  = font(FCONSOLA, 15)
    f_tiny = font(FCONSOLA, 13)

    # hello_world() label
    code_phase = phase
    code_col = (
        int(190 + 65*math.sin(2*math.pi*code_phase)),
        int(100 + 50*math.sin(2*math.pi*code_phase + 1)),
        int(220 + 35*math.sin(2*math.pi*code_phase + 2))
    )
    draw.text((52, 42), "{ hello_world(); }", font=font(FCONSOLA, 16), fill=code_col)

    # Main name with glow
    name_text = "SATHURJAN"
    nb = f_name.getbbox(name_text)
    name_w = nb[2]-nb[0]
    name_x = 52
    # Glow layers
    for gr in [18, 12, 7, 3]:
        for ddx in range(-gr, gr+1, max(1,gr//3)):
            for ddy in range(-gr, gr+1, max(1,gr//3)):
                if abs(ddx)+abs(ddy) <= gr:
                    draw.text((name_x+ddx, 72+ddy), name_text, font=f_name,
                              fill=(*P_BRIGHT, max(0,55-gr*2)))
    draw.text((name_x, 72), name_text, font=f_name, fill=P_LAVEN)

    # Subtitle
    draw.text((54, 170), "SOFTWARE ENGINEERING UNDERGRADUATE", font=f_sub, fill=P_NEON)
    draw.text((54, 198), "University of Moratuwa  •  Sri Lanka  🇱🇰", font=f_tag, fill=TEXT_DIM)

    # Animated typewriter on tagline
    tagline = "BUILD  •  CREATE  •  INNOVATE"
    chars_shown = int(len(tagline) * min(1.0, (phase * 1.8) % 1.0 + 0.3))
    partial_tag = tagline[:chars_shown]
    cursor_blink = (frame_index // 3) % 2 == 0
    tag_draw = partial_tag + ("▮" if cursor_blink else "▯")
    draw.text((54, 226), tag_draw, font=f_tag, fill=P_PINK)

    # Skill badges row
    badges = ["Software Eng", "Full Stack", "AI & ML", "Backend", "Open Source"]
    bx, by = 54, 265
    for i, badge in enumerate(badges):
        bfont = font(FCONSOLA, 12)
        try:
            bb = bfont.getbbox(badge)
            bw = bb[2]-bb[0]+18
        except:
            bw = len(badge)*7+18
        bh = 22
        # Glow
        b_phase = 0.3 + 0.7*math.sin(2*math.pi*(phase + i*0.18))
        b_glow = (int(50*b_phase), int(15*b_phase), int(100*b_phase))
        for gr in [4,2]:
            draw.rounded_rectangle([bx-gr,by-gr,bx+bw+gr,by+bh+gr], radius=5, outline=(*P_MID,100), width=1)
        draw.rounded_rectangle([bx,by,bx+bw,by+bh], radius=4,
                               fill=(20,8,48), outline=(*P_PRIMARY,220), width=1)
        draw.text((bx+9, by+4), badge, font=bfont, fill=P_LAVEN)
        bx += bw + 8

    # Bottom border glow line
    glow_alpha = int(120 + 80*math.sin(2*math.pi*phase))
    draw.line([(0, H-3),(W, H-3)], fill=(*P_PRIMARY, glow_alpha), width=2)
    draw.line([(0, H-1),(W, H-1)], fill=(*P_MID, 60), width=1)

    return img.convert("RGB")


def generate_header(total_frames=36):
    print("Generating HEADER GIF...")
    frames = []
    for fi in range(total_frames):
        f = build_header_frame(fi, total_frames)
        frames.append(f)
        if fi % 6 == 0: print(f"  frame {fi+1}/{total_frames}")

    out = os.path.join(ASSETS, "header.gif")
    # Quantize each frame for GIF
    q_frames = [f.quantize(colors=180, dither=Image.Dither.FLOYDSTEINBERG) for f in frames]
    q_frames[0].save(
        out, save_all=True, append_images=q_frames[1:],
        optimize=True, duration=65, loop=0
    )
    print(f"  → {out}  ({os.path.getsize(out)//1024} KB)")
    # Static preview
    frames[0].save(os.path.join(ASSETS, "header_preview.png"), format="PNG")


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER GIF — 1200×160
# ═══════════════════════════════════════════════════════════════════════════════

def build_footer_frame(fi, total):
    W, H = 1200, 160
    phase = fi / total
    img = Image.new("RGB", (W, H), BG0)
    draw = ImageDraw.Draw(img)

    # Sky section (top 110px)
    for y in range(110):
        t = y / 110
        c = lerp3(BG0, BG2, t)
        draw.line([(0,y),(W,y)], fill=c)

    # Ground section
    for y in range(110, H):
        t = (y-110)/(H-110)
        c = lerp3(BG2, BG0, t)
        draw.line([(0,y),(W,y)], fill=c)

    # Stars
    draw_stars(draw, W, 100, 5555, n=70, phase=phase)

    # Moon (smaller, right)
    pulse = 0.8 + 0.2*math.sin(2*math.pi*phase)
    draw_moon(draw, 1050, 40, 28, pulse)

    # City
    draw_city(draw, W, 110, seed=42)

    # Closing text
    f_msg = font(FSEGOUB, 20)
    f_msg2= font(FCONSOLA, 13)
    msg = "Keep Building.  Keep Learning.  Keep Growing."
    try:
        mb = f_msg.getbbox(msg)
        mw = mb[2]-mb[0]
    except:
        mw = len(msg)*12
    mx = (W - mw) // 2
    # Glow
    glow_a = 0.6 + 0.4*math.sin(2*math.pi*phase)
    for gr in [8,4,2]:
        draw.text((mx-gr, 20-gr//2), msg, font=f_msg, fill=(*P_MID, int(60*glow_a)))
    draw.text((mx, 20), msg, font=f_msg, fill=P_LAVEN)

    sub = "— Sathurjan  |  github.com/Sathurjanv23"
    try:
        sb = f_msg2.getbbox(sub)
        sw = sb[2]-sb[0]
    except:
        sw = len(sub)*8
    sx = (W - sw) // 2
    draw.text((sx, 50), sub, font=f_msg2, fill=TEXT_DIM)

    # Bottom neon line
    glow_a2 = int(100 + 80*math.sin(2*math.pi*phase))
    draw.line([(0,H-3),(W,H-3)], fill=(*P_PRIMARY, glow_a2), width=2)

    return img


def generate_footer(total_frames=24):
    print("Generating FOOTER GIF...")
    frames = [build_footer_frame(fi, total_frames) for fi in range(total_frames)]
    q_frames = [f.quantize(colors=120, dither=Image.Dither.FLOYDSTEINBERG) for f in frames]
    out = os.path.join(ASSETS, "footer.gif")
    q_frames[0].save(out, save_all=True, append_images=q_frames[1:],
                     optimize=True, duration=80, loop=0)
    print(f"  → {out}  ({os.path.getsize(out)//1024} KB)")


# ═══════════════════════════════════════════════════════════════════════════════
# ANIME AVATAR — 400×400
# ═══════════════════════════════════════════════════════════════════════════════

def generate_anime_avatar():
    print("Generating ANIME AVATAR...")
    W = H = 400
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(img)

    # Circular background
    for r in range(190, 0, -2):
        t = 1 - r/190
        c = lerp3(BG1, P_DARK, t)
        a = 255
        draw.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], fill=(*c,a))

    # Ring border
    for rr in [192,196,198,200]:
        draw.ellipse([W//2-rr, H//2-rr, W//2+rr, H//2+rr], outline=(*P_PRIMARY, 220), width=2)

    # Character (larger)
    draw_pixel_char(draw, W//2, H//2+40, scale=5)

    # Overlay glow
    overlay = Image.new("RGBA", (W,H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    odraw.ellipse([W//2-190, H//2-190, W//2+190, H//2+190], fill=(*P_PRIMARY,15))
    img = Image.alpha_composite(img, overlay)

    out = os.path.join(ASSETS, "anime-avatar.png")
    img.save(out, format="PNG")
    print(f"  → {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT THUMBNAILS — 480×260
# ═══════════════════════════════════════════════════════════════════════════════

def project_thumb_base(W=480, H=260, bg=BG1):
    img = Image.new("RGB", (W,H), bg)
    draw = ImageDraw.Draw(img)
    # Gradient bg
    for y in range(H):
        t = y/H
        c = lerp3(BG0, BG2, t)
        draw.line([(0,y),(W,y)], fill=c)
    # Dot grid
    for x in range(16, W-16, 20):
        for y in range(16, H-16, 20):
            draw.point((x,y), fill=(40,20,80))
    return img, draw


def draw_thumb_label(draw, W, H, title, stack, icon="🏗️"):
    f_title = font(FGOTHICB, 22)
    f_stack = font(FCONSOLA, 12)
    f_icon  = font(FSEGUI,   30)

    # Title background
    draw.rectangle([0, H-70, W, H], fill=(10,5,25))
    draw.line([(0,H-70),(W,H-70)], fill=P_MID, width=1)

    # Icon circle
    draw.ellipse([18,H-62,56,H-24], fill=P_DARK, outline=P_PRIMARY, width=1)
    draw.text((22, H-58), icon, font=f_icon, fill=P_LAVEN)

    # Title
    draw.text((65, H-62), title, font=f_title, fill=P_LAVEN)
    # Stack
    draw.text((66, H-36), stack, font=f_stack, fill=TEXT_DIM)

    # Glow border on card
    for gr in [4,2]:
        draw.rounded_rectangle([gr,gr,W-gr,H-gr], radius=10, outline=(*P_PRIMARY, 80//gr), width=1)
    draw.rounded_rectangle([0,0,W-1,H-1], radius=10, outline=(*P_PRIMARY,160), width=2)


def gen_project_01_reqtrace():
    """ReqTrace AI — neural net / requirement nodes aesthetic"""
    W, H = 480, 260
    img, draw = project_thumb_base(W,H)

    # Node network (AI brain style)
    rng = random.Random(1)
    nodes = [(rng.randint(60,W-60), rng.randint(40,H-90)) for _ in range(18)]
    # Connections
    for i, (nx,ny) in enumerate(nodes):
        for j, (mx,my) in enumerate(nodes):
            if i<j and math.sqrt((nx-mx)**2+(ny-my)**2) < 110:
                col = (40,15,90)
                draw.line([(nx,ny),(mx,my)], fill=col, width=1)
    # Node dots with glow
    cols = [P_PRIMARY, P_PINK, P_NEON, CYAN]
    for i,(nx,ny) in enumerate(nodes):
        col = cols[i%len(cols)]
        for gr in [10,6,3]:
            draw.ellipse([nx-gr,ny-gr,nx+gr,ny+gr], fill=(*col[:3],40//gr*10))
        draw.ellipse([nx-5,ny-5,nx+5,ny+5], fill=col)

    # Central AI eye
    cx,cy = W//2, (H-70)//2+5
    for gr in range(45,0,-3):
        t=1-gr/45
        col=lerp3(BG0,P_MID,t)
        draw.ellipse([cx-gr,cy-gr,cx+gr,cy+gr], fill=col)
    # Iris
    for gr in range(20,0,-2):
        t=1-gr/20
        col=lerp3(P_MID,P_PRIMARY,t)
        draw.ellipse([cx-gr,cy-gr,cx+gr,cy+gr], fill=col)
    draw.ellipse([cx-6,cy-6,cx+6,cy+6], fill=P_LAVEN)
    draw.ellipse([cx-2,cy-2,cx+2,cy+2], fill=(255,255,255))

    # PROJECT label
    draw.text((18,18), "PROJECT  /  01", font=font(FCONSOLA,12), fill=TEXT_DIM)

    draw_thumb_label(draw, W, H, "ReqTrace AI", "Java  •  Spring Boot  •  MongoDB  •  React  •  AI", "🤖")
    out = os.path.join(PROJECTS, "project-01.png")
    img.save(out)
    print(f"  → {out}")


def gen_project_02_iws():
    """IWS.LK — geospatial map / workforce matching"""
    W, H = 480, 260
    img, draw = project_thumb_base(W,H)

    # Map hexagon grid
    rng = random.Random(2)
    HEX_R = 22
    for row in range(8):
        for col in range(14):
            hx = col * HEX_R * 1.75 + (HEX_R if row%2 else 0)
            hy = row * HEX_R * 1.52
            # hex outline
            pts = []
            for ang in range(0,360,60):
                a = math.radians(ang)
                pts.append((hx+HEX_R*0.9*math.cos(a), hy+HEX_R*0.9*math.sin(a)))
            # fill based on activity
            prob = rng.random()
            if prob > 0.75:
                fcol = (*P_MID, 180)
                draw.polygon(pts, fill=fcol, outline=(*P_PRIMARY,100))
            elif prob > 0.5:
                draw.polygon(pts, fill=(*BG2, 180), outline=(30,15,70))
            else:
                draw.polygon(pts, fill=(*BG1, 180), outline=(20,10,50))

    # Location pins
    pin_locs = [(180,80),(260,110),(340,70),(200,145),(310,140)]
    for px,py in pin_locs:
        for gr in [12,7,3]:
            draw.ellipse([px-gr,py-gr,px+gr,py+gr], fill=(*P_PINK[:3],30+gr*8))
        draw.ellipse([px-5,py-5,px+5,py+5], fill=P_PINK)
        # pin stem
        draw.line([(px,py+5),(px,py+14)], fill=P_PINK, width=2)
    # connection lines
    for i,(px,py) in enumerate(pin_locs):
        for qx,qy in pin_locs[i+1:i+2]:
            draw.line([(px,py),(qx,qy)], fill=(*P_PRIMARY,80), width=1)

    draw.text((18,18), "PROJECT  /  02", font=font(FCONSOLA,12), fill=TEXT_DIM)
    draw_thumb_label(draw, W, H, "IWS.LK", "FastAPI  •  Python  •  React  •  MongoDB  •  ML", "🌐")
    out = os.path.join(PROJECTS, "project-02.png")
    img.save(out)
    print(f"  → {out}")


def gen_project_03_crms():
    """CRMS — Kanban board / workflow dashboard"""
    W, H = 480, 260
    img, draw = project_thumb_base(W,H)

    # Kanban columns
    columns = [("TODO","#5B21B6",(90,35,180)), ("IN PROGRESS","#9333EA",(147,51,234)), ("REVIEW","#EC4899",(236,72,153)), ("DONE","#10B981",(16,185,129))]
    col_w = 90
    for ci,(label,hx,col_rgb) in enumerate(columns):
        cx = 45 + ci*(col_w+18)
        # Column header
        draw.rectangle([cx, 25, cx+col_w, 50], fill=(*col_rgb,180))
        draw.text((cx+6, 32), label, font=font(FCONSOLA,10), fill=(240,230,255))
        # Cards
        rng2 = random.Random(ci*17)
        cards_n = rng2.randint(2,4)
        for card_i in range(cards_n):
            cy_card = 58 + card_i * 38
            if cy_card + 32 < H - 75:
                draw.rectangle([cx+2, cy_card, cx+col_w-2, cy_card+30], fill=(20,10,45))
                draw.rectangle([cx+2, cy_card, cx+col_w-2, cy_card+4], fill=col_rgb)
                draw.rectangle([cx+6, cy_card+8, cx+6+rng2.randint(30,65), cy_card+11], fill=(60,30,120))
                draw.rectangle([cx+6, cy_card+16, cx+6+rng2.randint(20,55), cy_card+19], fill=(40,20,80))

    # Corner role badge
    for role,ry,rcol in [("Client",8,P_PINK),("Company",28,P_PRIMARY),("Admin",48,CYAN)]:
        draw.rounded_rectangle([W-80,ry,W-5,ry+16], radius=4, fill=(20,8,45))
        draw.text((W-75, ry+2), role, font=font(FCONSOLA,10), fill=rcol)

    draw.text((18,18), "PROJECT  /  03", font=font(FCONSOLA,12), fill=TEXT_DIM)
    draw_thumb_label(draw, W, H, "CRMS", "Spring Boot  •  Next.js  •  MongoDB  •  JWT", "🔄")
    out = os.path.join(PROJECTS, "project-03.png")
    img.save(out)
    print(f"  → {out}")


def gen_project_04_ipl():
    """IPL Analytics — data viz / charts"""
    W, H = 480, 260
    img, draw = project_thumb_base(W,H)

    # Bar chart
    chart_x, chart_y = 40, 20
    chart_w, chart_h = 240, 155
    # Axes
    draw.line([(chart_x, chart_y),(chart_x, chart_y+chart_h)], fill=P_MID, width=2)
    draw.line([(chart_x, chart_y+chart_h),(chart_x+chart_w, chart_y+chart_h)], fill=P_MID, width=2)
    # Bars
    bars = [0.6,0.85,0.45,0.95,0.7,0.55,0.8,0.65,0.9,0.5]
    colors = [P_PRIMARY,P_PINK,P_NEON,CYAN,GREEN_NEO,P_PRIMARY,P_PINK,CYAN,GREEN_NEO,P_NEON]
    bw = chart_w // len(bars) - 4
    for bi,(bv,bc) in enumerate(zip(bars,colors)):
        bh2 = int(chart_h * bv)
        bx = chart_x + bi*(bw+4) + 4
        by_top = chart_y + chart_h - bh2
        # Bar glow
        for gr in [4,2]:
            draw.rectangle([bx-gr, by_top-gr, bx+bw+gr, chart_y+chart_h+gr], fill=(*bc[:3],25))
        draw.rectangle([bx, by_top, bx+bw, chart_y+chart_h], fill=bc)
        # Top highlight
        draw.rectangle([bx, by_top, bx+bw, by_top+2], fill=(255,255,255))

    # Line chart overlay (trend line)
    pts = []
    for bi,bv in enumerate(bars):
        lx = chart_x + bi*(bw+4) + 4 + bw//2
        ly = chart_y + chart_h - int(chart_h*bv)
        pts.append((lx,ly))
    for i in range(len(pts)-1):
        draw.line([pts[i],pts[i+1]], fill=P_PINK, width=2)
    for px,py in pts:
        draw.ellipse([px-3,py-3,px+3,py+3], fill=P_PINK)

    # Stats cards on right
    stats = [("768","Matches"),("12.5K","Deliveries"),("94%","Accuracy")]
    for si,(val,lbl) in enumerate(stats):
        sx = chart_x+chart_w+25
        sy = 20+si*52
        draw.rectangle([sx,sy,sx+110,sy+42], fill=(15,8,38))
        draw.rectangle([sx,sy,sx+4,sy+42], fill=P_PRIMARY)
        draw.text((sx+10,sy+5), val, font=font(FGOTHICB,18), fill=P_LAVEN)
        draw.text((sx+10,sy+26), lbl, font=font(FCONSOLA,11), fill=TEXT_DIM)

    draw.text((18,18), "PROJECT  /  04", font=font(FCONSOLA,12), fill=TEXT_DIM)
    draw_thumb_label(draw, W, H, "IPL Analytics", "Python  •  Pandas  •  Scikit-learn  •  Plotly", "📊")
    out = os.path.join(PROJECTS, "project-04.png")
    img.save(out)
    print(f"  → {out}")


if __name__ == "__main__":
    random.seed(0)
    print("=" * 60)
    print(" PURPLE PIXEL UNIVERSE — ARTWORK GENERATOR")
    print("=" * 60)

    generate_header(total_frames=36)
    generate_footer(total_frames=24)
    generate_anime_avatar()

    print("Generating PROJECT THUMBNAILS...")
    gen_project_01_reqtrace()
    gen_project_02_iws()
    gen_project_03_crms()
    gen_project_04_ipl()

    print()
    print("All artwork generated successfully!")
    all_files = []
    for root, dirs, files in os.walk(ASSETS):
        for f in files:
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            all_files.append((path.replace(ASSETS, "assets"), size))
    for name, size in all_files:
        print(f"  {name:50s}  {size//1024:>5} KB")
