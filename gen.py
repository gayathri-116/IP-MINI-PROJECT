import re, random, os
W, H, HZ = 900, 600, 420
def sh(h, f):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(x*f))) for x in (r, g, b))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def P(pts): return ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts)
SKY = [(('#ff9a8b', '#ffe2b0'), .95), (('#3a9be0', '#c4e8ff'), 1), (('#2d1b5e', '#ff7a50'), .72), (('#040a22', '#1a2a5c'), .42)]
SUN = [(640, 340), (730, 110), (190, 370), (730, 100)]

def ridge(r, y, amp, col, f, n=8, snow=False):
    pts = [(-10, HZ+90)]; caps = ''
    for i in range(n+1):
        x = i*W/n; py = y - r.uniform(.3, 1)*amp if i % 2 else y - r.uniform(0, .25)*amp
        pts.append((x, py))
        if snow and i % 2 and py < y - amp*.55:
            caps += f'<polygon points="{P([(x,py),(x-38,py+46),(x-14,py+36),(x,py+52),(x+16,py+36),(x+38,py+46)])}" fill="{sh("#ffffff",f)}"/>'
    pts.append((W+10, HZ+90))
    return f'<polygon points="{P(pts)}" fill="{sh(col,f)}"/>' + caps
def pines(r, f, y0, n=26):
    s = ''
    for _ in range(n):
        x = r.randint(0, W); h = r.randint(40, 90)
        s += f'<polygon points="{P([(x,y0-h),(x-h*.22,y0),(x+h*.22,y0)])}" fill="{sh("#1d4a30",f)}"/>'
    return s
def blobs(r, f, y0, y1, col, n):
    return ''.join(f'<circle cx="{r.randint(0,W)}" cy="{r.randint(y0,y1)}" r="{r.randint(30,60)}" fill="{sh(col,f*r.uniform(.8,1.1))}"/>' for _ in range(n))
def water(f, y=HZ, col='#2f7fa8'):
    lines = ''.join(f'<rect x="{(i*137)%800}" y="{y+25+i*17}" width="{90+i*9}" height="3" rx="1.5" fill="#fff" opacity=".28"/>' for i in range(9))
    return f'<rect y="{y}" width="{W}" height="{H-y}" fill="{sh(col,f)}"/>' + lines

def b_mount(r, f, v, snow=True):
    return ridge(r, 330, 190, '#7a8fae', f, 7, snow) + ridge(r, 390, 140, '#506b88', f, 9, snow) + \
        f'<rect y="{HZ+10}" width="{W}" height="{H}" fill="{sh("#2f5a3a",f)}"/>' + pines(r, f, 470) + pines(r, f, 540, 14)
def b_lake(r, f, v):
    return ridge(r, 320, 190, '#7a8fae', f, 7, True) + ridge(r, 390, 130, '#3f5c4f', f, 9) + water(f)
def b_water(r, f, v):
    return ridge(r, 400, 50, '#3f6b4a', f, 12) + water(f, 405)
def b_desert(r, f, v):
    d = lambda y, c: f'<path d="M0,{y} Q220,{y-70} 450,{y} T900,{y-10} V600 H0Z" fill="{sh(c,f)}"/>'
    return d(430, '#d9a45a') + d(490, '#c58a42') + d(560, '#a96f33')
def b_salt(r, f, v):
    cr = ''.join(f'<path d="M{i*90},{450+i*13} l40,12 l30,-8" stroke="{sh("#cfcfc4",f)}" fill="none"/>' for i in range(10))
    return f'<rect y="{HZ+10}" width="{W}" height="{H}" fill="{sh("#f1ece0",f)}"/>' + cr
def b_hills(r, f, v, snow=False):
    s = ridge(r, 350, 150, '#8aa0bd', f, 7, True) if snow else ''
    for y, c in ((410, '#4f9a4f'), (470, '#3f8742'), (540, '#2f6f37')):
        s += f'<path d="M0,{y} Q200,{y-60} 450,{y-10} T900,{y-30} V600 H0Z" fill="{sh(c,f)}"/>'
    s += ''.join(f'<path d="M0,{500+i*14} Q250,{470+i*14} 500,{500+i*12} T900,{480+i*10}" stroke="{sh("#2a5f31",f)}" fill="none" stroke-width="2"/>' for i in range(5))
    return s
def b_beach(r, f, v):
    return f'<rect y="340" width="{W}" height="140" fill="{sh("#1fa6c9",f)}"/><rect y="340" width="{W}" height="8" fill="{sh("#7fd6ea",f)}"/>' + \
        f'<path d="M0,600 V480 Q450,430 900,490 V600Z" fill="{sh("#f0d9a0",f)}"/><path d="M0,478 Q450,425 900,486" stroke="#fff" stroke-width="5" fill="none" opacity=".7"/>'
def b_city(r, f, v):
    s = ''
    for x in range(0, W, 45):
        h = r.randint(60, 190); s += f'<rect x="{x}" y="{HZ+30-h}" width="40" height="{h}" fill="{sh("#6c7fa0",f)}"/>'
    return s + f'<rect y="{HZ+30}" width="{W}" height="{H}" fill="{sh("#38465e",f)}"/>'
def b_falls(r, f, v):
    s = f'<rect width="{W}" height="{H}" fill="{sh("#2f5a3a",f)}" opacity="0"/>'
    s += f'<rect x="0" y="230" width="360" height="300" fill="{sh("#4b4036",f)}"/><rect x="540" y="230" width="360" height="300" fill="{sh("#4b4036",f)}"/>'
    s += f'<rect x="360" y="260" width="180" height="230" fill="{sh("#eaf6ff",f)}"/>' + ''.join(f'<rect x="{372+i*26}" y="260" width="6" height="230" fill="#9fd0ea" opacity=".6"/>' for i in range(6))
    s += blobs(r, f, 215, 250, '#2f7a3a', 12) + f'<ellipse cx="450" cy="500" rx="260" ry="40" fill="{sh("#3b9bb5",f)}"/><rect y="520" width="{W}" height="80" fill="{sh("#2f5a3a",f)}"/>'
    return s
def b_jungle(r, f, v):
    return blobs(r, f, 300, 420, '#2f7a3a', 24) + f'<rect y="360" width="{W}" height="120" fill="#fff" opacity=".18"/>' + \
        f'<rect y="{HZ+20}" width="{W}" height="{H}" fill="{sh("#35542f",f)}"/>' + blobs(r, f, 430, 520, '#1f4a2a', 20)
def b_plain(r, f, v):
    return ridge(r, 410, 30, '#6d9658', f, 12) + f'<rect y="{HZ+15}" width="{W}" height="{H}" fill="{sh("#79a05c",f)}"/>'
BASES = {'mount': b_mount, 'mountbare': lambda r, f, v: b_mount(r, f, v, False), 'lake': b_lake, 'water': b_water, 'desert': b_desert, 'salt': b_salt,
         'hills': b_hills, 'hillsnow': lambda r, f, v: b_hills(r, f, v, True), 'beach': b_beach, 'city': b_city, 'falls': b_falls, 'jungle': b_jungle, 'plain': b_plain}

def dome(cx, f, v, r, col='#f5efe6', mins=True):
    y = 455; c = sh(col, f); d = sh(col, f*.8); glow = '#ffd36b' if v >= 2 else sh('#3a3a3a', f)
    s = f'<rect x="{cx-170}" y="{y-24}" width="340" height="24" fill="{d}"/><rect x="{cx-100}" y="{y-130}" width="200" height="106" fill="{c}"/>'
    s += f'<path d="M{cx-95},{y-130} Q{cx-118},{y-230} {cx},{y-270} Q{cx+118},{y-230} {cx+95},{y-130}Z" fill="{c}"/><rect x="{cx-2}" y="{y-300}" width="4" height="34" fill="{d}"/>'
    s += f'<path d="M{cx-26},{y-24} V{y-80} Q{cx},{y-110} {cx+26},{y-80} V{y-24}Z" fill="{glow}"/>'
    if mins:
        for dx in (-175, 175):
            s += f'<rect x="{cx+dx-9}" y="{y-210}" width="18" height="190" fill="{c}"/><path d="M{cx+dx-14},{y-210} Q{cx+dx},{y-250} {cx+dx+14},{y-210}Z" fill="{d}"/>'
    return s
def gopuram(cx, f, v, r, col='#c98b5a'):
    s = ''
    for i in range(7):
        w = 300 - i*38; y = 455 - i*38
        s += f'<polygon points="{P([(cx-w/2,y),(cx+w/2,y),(cx+w/2-14,y-38),(cx-w/2+14,y-38)])}" fill="{sh(col, f*(1.1 if i%2 else .9))}"/>'
        s += ''.join(f'<rect x="{cx-w/2+10+k*(w-30)/6}" y="{y-26}" width="8" height="14" fill="{sh("#5a3320",f)}"/>' for k in range(7) if w > 120)
    s += f'<path d="M{cx-14},455 V410 Q{cx},392 {cx+14},410 V455Z" fill="{"#ffd36b" if v>=2 else sh("#2a1a10",f)}"/><ellipse cx="{cx}" cy="{455-7*38-6}" rx="22" ry="10" fill="{sh("#e8c15a",f)}"/>'
    return s
def fort(cx, f, v, r, col='#d9a066'):
    c = sh(col, f); d = sh(col, f*.8); s = f'<rect x="{cx-330}" y="395" width="660" height="60" fill="{c}"/>'
    s += ''.join(f'<rect x="{cx-330+i*30}" y="383" width="18" height="14" fill="{c}"/>' for i in range(22))
    for dx in (-300, 0, 300):
        s += f'<rect x="{cx+dx-40}" y="300" width="80" height="155" fill="{d}"/><path d="M{cx+dx-46},300 Q{cx+dx},235 {cx+dx+46},300Z" fill="{c}"/>'
        s += f'<path d="M{cx+dx-10},455 V420 Q{cx+dx},405 {cx+dx+10},420 V455Z" fill="{"#ffd36b" if v>=2 else sh("#3a2a1a",f)}"/>'
    return s
def eiffel(cx, f, v, r):
    col = '#e0b24a' if v == 3 else sh('#5a4b44', f)
    s = f'<path d="M{cx-100},470 L{cx-20},250 L{cx+20},250 L{cx+100},470 L{cx+66},470 L{cx},350 L{cx-66},470Z" fill="{col}"/><polygon points="{P([(cx-20,250),(cx,120),(cx+20,250)])}" fill="{col}"/>'
    s += f'<rect x="{cx-70}" y="345" width="140" height="10" fill="{col}"/><rect x="{cx-26}" y="248" width="52" height="8" fill="{col}"/>'
    s += ''.join(f'<line x1="{cx-60+i*30}" y1="470" x2="{cx-12+i*8}" y2="360" stroke="{col}" opacity=".7"/>' for i in range(5))
    return s
def pyramids(cx, f, v, r):
    s = ''
    for dx, w, h in ((-190, 230, 150), (30, 330, 230), (250, 190, 120)):
        x = cx+dx; s += f'<polygon points="{P([(x-w/2,455),(x,455-h),(x,455)])}" fill="{sh("#e6c27a",f)}"/><polygon points="{P([(x,455-h),(x+w/2,455),(x,455)])}" fill="{sh("#c79a52",f)}"/>'
    return s
def balloons(cx, f, v, r):
    s = ''
    for i, (x, y, c) in enumerate(((150, 150, '#e63946'), (330, 100, '#f4a261'), (560, 170, '#2a9d8f'), (770, 120, '#e9c46a'), (450, 230, '#9b5de5'))):
        s += f'<ellipse cx="{x}" cy="{y}" rx="38" ry="46" fill="{sh(c,f)}"/><line x1="{x-18}" y1="{y+40}" x2="{x-8}" y2="{y+68}" stroke="#333"/><line x1="{x+18}" y1="{y+40}" x2="{x+8}" y2="{y+68}" stroke="#333"/><rect x="{x-9}" y="{y+68}" width="18" height="12" fill="{sh("#6b4a2a",f)}"/>'
    return s
def overwater(cx, f, v, r):
    s = f'<rect x="60" y="470" width="780" height="8" fill="{sh("#8a6a45",f)}"/>'
    for i in range(5):
        x = 110 + i*160; s += f'<rect x="{x}" y="478" width="4" height="30" fill="{sh("#6b4a2a",f)}"/><rect x="{x+60}" y="478" width="4" height="30" fill="{sh("#6b4a2a",f)}"/>'
        s += f'<rect x="{x-8}" y="440" width="80" height="30" fill="{sh("#e9dcc0",f)}"/><polygon points="{P([(x-18,442),(x+32,408),(x+82,442)])}" fill="{sh("#b58a4a",f)}"/><rect x="{x+22}" y="450" width="20" height="20" fill="{"#ffd36b" if v>=2 else sh("#555555",f)}"/>'
    return s
def sails(cx, f, v, r):
    s = f'<rect x="{cx-260}" y="452" width="520" height="14" fill="{sh("#cfc8bb",f)}"/>'
    for dx, k in ((-240, 1), (-60, 1.2), (130, .9)):
        x = cx+dx; s += f'<path d="M{x},452 Q{x+10},{452-120*k} {x+130*k},{452-170*k} Q{x+140*k},{452-70*k} {x+130*k},452Z" fill="{sh("#f6f2ea",f)}"/>'
    return s
def stupa(cx, f, v, r):
    s = f'<rect x="{cx-150}" y="440" width="300" height="16" fill="{sh("#d8d2c4",f)}"/><rect x="{cx-120}" y="424" width="240" height="16" fill="{sh("#e6e0d2",f)}"/>'
    s += f'<path d="M{cx-100},424 A100,100 0 0 1 {cx+100},424Z" fill="{sh("#faf6ee",f)}"/><rect x="{cx-30}" y="300" width="60" height="30" fill="{sh("#e8b34a",f)}"/>'
    s += f'<polygon points="{P([(cx-26,300),(cx,200),(cx+26,300)])}" fill="{sh("#e8b34a",f)}"/><circle cx="{cx-12}" cy="314" r="4"/><circle cx="{cx+12}" cy="314" r="4"/>'
    for i, c in enumerate(('#2a6fdb', '#f4f4f4', '#d62828', '#2a9d3f', '#f2c12e')):
        s += f'<path d="M{cx},205 L{cx-170+i*34},{330+i*10}" stroke="{c}" stroke-width="5" opacity=".9"/><path d="M{cx},205 L{cx+170-i*34},{330+i*10}" stroke="{c}" stroke-width="5" opacity=".9"/>'
    return s
def monastery(cx, f, v, r):
    s = f'<polygon points="{P([(cx-190,470),(cx-120,330),(cx-60,300),(cx+80,290),(cx+170,350),(cx+210,470)])}" fill="{sh("#7a6a58",f)}"/>'
    for i, (x, y, w, h) in enumerate(((-90, 330, 150, 60), (-60, 280, 100, 52), (-30, 236, 56, 46))):
        s += f'<rect x="{cx+x}" y="{y}" width="{w}" height="{h}" fill="{sh("#f6f0e6",f)}"/><polygon points="{P([(cx+x-8,y),(cx+x+w/2,y-24),(cx+x+w+8,y)])}" fill="{sh("#d9a02e",f)}"/>'
        s += f'<rect x="{cx+x+w/2-6}" y="{y+16}" width="12" height="16" fill="{"#ffd36b" if v>=2 else sh("#6a3a2a",f)}"/>'
    return s
def bigben(cx, f, v, r):
    c = sh('#c9b27a', f); s = f'<rect x="{cx-200}" y="390" width="230" height="65" fill="{c}"/>' + ''.join(f'<rect x="{cx-190+i*30}" y="400" width="12" height="30" fill="{sh("#8a7a50",f)}"/>' for i in range(7))
    s += f'<rect x="{cx+30}" y="200" width="70" height="255" fill="{c}"/><polygon points="{P([(cx+26,200),(cx+65,110),(cx+104,200)])}" fill="{sh("#6a7a6a",f)}"/>'
    s += f'<circle cx="{cx+65}" cy="240" r="24" fill="{"#fff3b0" if v>=2 else "#f6f6f2"}" stroke="#333" stroke-width="3"/><line x1="{cx+65}" y1="240" x2="{cx+65}" y2="226" stroke="#333" stroke-width="2"/><line x1="{cx+65}" y1="240" x2="{cx+76}" y2="244" stroke="#333" stroke-width="2"/>'
    return s
def burj(cx, f, v, r):
    s = f'<polygon points="{P([(cx-34,470),(cx-20,350),(cx-12,260),(cx-4,160),(cx,70),(cx+4,160),(cx+12,260),(cx+20,350),(cx+34,470)])}" fill="{sh("#aab8c8",f)}"/>'
    for dx, h in ((-160, 150), (-110, 200), (90, 180), (140, 130), (190, 160)):
        s += f'<rect x="{cx+dx-18}" y="{470-h}" width="36" height="{h}" fill="{sh("#8c9cb4",f)}"/>'
    return s
def petronas(cx, f, v, r):
    s = ''
    for dx in (-60, 60):
        x = cx+dx; s += f'<polygon points="{P([(x-34,470),(x-26,330),(x-20,230),(x-8,170),(x,120),(x+8,170),(x+20,230),(x+26,330),(x+34,470)])}" fill="{sh("#b9c6d6",f)}"/>'
    return s + f'<rect x="{cx-60}" y="300" width="120" height="12" fill="{sh("#8c9cb4",f)}"/>'
def marina(cx, f, v, r):
    s = ''.join(f'<rect x="{cx-120+i*85}" y="300" width="50" height="170" fill="{sh("#c5d0dc",f)}"/>' for i in range(3))
    s += f'<path d="M{cx-150},300 Q{cx},265 {cx+150},300 Q{cx},290 {cx-150},300Z" fill="{sh("#90a0b4",f)}"/><path d="M{cx+190},470 Q{cx+250},400 {cx+310},470Z" fill="{sh("#e8d8f0",f)}"/>'
    return s
def nyc(cx, f, v, r):
    s = ''
    for i in range(14):
        x = 60+i*58; h = r.randint(120, 260); s += f'<rect x="{x}" y="{470-h}" width="46" height="{h}" fill="{sh("#566580",f)}"/>' + (''.join(f'<rect x="{x+8+(k%3)*12}" y="{470-h+12+(k//3)*20}" width="6" height="8" fill="#ffd36b"/>' for k in range(18)) if v >= 2 else '')
    return s + f'<polygon points="{P([(cx-40,470),(cx-40,260),(cx-24,260),(cx-24,200),(cx-10,200),(cx-10,150),(cx,90),(cx+10,150),(cx+10,200),(cx+24,200),(cx+24,260),(cx+40,260),(cx+40,470)])}" fill="{sh("#7080a0",f)}"/>'
def gate(cx, f, v, r):
    c = sh('#c8a96a', f)
    s = f'<rect x="{cx-130}" y="270" width="260" height="190" fill="{c}"/><path d="M{cx-45},460 V350 Q{cx},290 {cx+45},350 V460Z" fill="{"#ffd36b" if v>=2 else sh("#3a2f20",f)}"/>'
    for dx in (-130, -105, 105, 130):
        s += f'<rect x="{cx+dx-10}" y="230" width="20" height="45" fill="{c}"/><circle cx="{cx+dx}" cy="228" r="12" fill="{c}"/>'
    return s + f'<path d="M{cx-60},270 Q{cx},190 {cx+60},270Z" fill="{c}"/>'
def charminar(cx, f, v, r):
    c = sh('#e8dcc4', f); s = f'<rect x="{cx-120}" y="300" width="240" height="155" fill="{c}"/>'
    for dx in (-120, 120):
        s += f'<rect x="{cx+dx-14}" y="200" width="28" height="255" fill="{c}"/><path d="M{cx+dx-20},200 Q{cx+dx},160 {cx+dx+20},200Z" fill="{sh("#b8a888",f)}"/>'
    s += ''.join(f'<path d="M{cx-90+i*60},455 V380 Q{cx-70+i*60},345 {cx-50+i*60},380 V455Z" fill="{"#ffd36b" if v>=2 else sh("#4a3f30",f)}"/>' for i in range(3))
    return s
def torii(cx, f, v, r):
    c = sh('#d62828', f)
    return f'<rect x="{cx-90}" y="360" width="16" height="110" fill="{c}"/><rect x="{cx+74}" y="360" width="16" height="110" fill="{c}"/><rect x="{cx-120}" y="340" width="240" height="14" fill="{c}"/><rect x="{cx-100}" y="372" width="200" height="8" fill="{c}"/>'
def fuji(cx, f, v, r):
    return f'<polygon points="{P([(120,HZ),(450,170),(780,HZ)])}" fill="{sh("#5a6f9a",f)}"/><polygon points="{P([(450,170),(396,240),(425,228),(450,250),(480,228),(506,240)])}" fill="{sh("#ffffff",f)}"/>'
def karst(cx, f, v, r):
    s = ''
    for x, h, w in ((90, 210, 90), (240, 150, 70), (400, 260, 100), (580, 170, 80), (730, 230, 95), (840, 120, 60)):
        s += f'<path d="M{x-w},{HZ+30} Q{x-w*.9},{HZ-h} {x},{HZ-h-20} Q{x+w*.9},{HZ-h} {x+w},{HZ+30}Z" fill="{sh("#6f8a7a",f)}"/>'
    return s + f'<rect y="{HZ+10}" width="{W}" height="40" fill="#fff" opacity=".2"/>'
def boat(cx, f, v, r, x=None, y=520, roof=True):
    x = cx-60 if x is None else x
    s = f'<path d="M{x},{y} Q{x+60},{y+30} {x+160},{y} L{x+140},{y+22} Q{x+80},{y+36} {x+20},{y+22}Z" fill="{sh("#b5452f",f)}"/>'
    return s + (f'<rect x="{x+40}" y="{y-34}" width="80" height="34" fill="{sh("#f0dcb0",f)}"/><path d="M{x+30},{y-34} Q{x+80},{y-62} {x+130},{y-34}Z" fill="{sh("#c8553d",f)}"/>' if roof else '')
def houseboat(cx, f, v, r):
    return boat(cx, f, v, r, cx-150, 510) + f'<rect x="{cx-30}" y="470" width="150" height="6" fill="{sh("#6b4a2a",f)}"/>'
def palm(x, f, h=210, lean=30):
    s = f'<path d="M{x},470 Q{x+lean},{470-h*.6} {x+lean*1.4},{470-h}" stroke="{sh("#6b4a2a",f)}" stroke-width="10" fill="none"/>'
    tx, ty = x+lean*1.4, 470-h
    for a in (-70, -35, 0, 35, 70, 110, -110):
        import math; ex = tx+math.cos(math.radians(a-90+ (0)))*95; ey = ty+math.sin(math.radians(a-90))*40+25
        s += f'<path d="M{tx},{ty} Q{(tx+ex)/2},{ty-45} {ex},{ey}" stroke="{sh("#2f8a3a",f)}" stroke-width="8" fill="none" stroke-linecap="round"/>'
    return s
def palms(cx, f, v, r): return palm(70, f, 220, 30) + palm(820, f, 190, -30) + palm(150, f, 150, 20)
def church(cx, f, v, r):
    c = sh('#f6f1e6', f)
    return f'<rect x="{cx-110}" y="360" width="220" height="95" fill="{c}"/><rect x="{cx-30}" y="300" width="60" height="60" fill="{c}"/><polygon points="{P([(cx-36,300),(cx,250),(cx+36,300)])}" fill="{sh("#c8553d",f)}"/><rect x="{cx-2}" y="226" width="4" height="26" fill="#444"/><rect x="{cx-10}" y="236" width="20" height="4" fill="#444"/><path d="M{cx-18},455 V400 Q{cx},380 {cx+18},400 V455Z" fill="{"#ffd36b" if v>=2 else sh("#4a3a2a",f)}"/>'
def ghat(cx, f, v, r):
    s = ''.join(f'<rect x="40" y="{455-i*14}" width="{820-i*18}" height="14" fill="{sh("#d9c39a" if i%2 else "#cdb27c",f)}"/>' for i in range(5))
    for x in (160, 330, 520, 690):
        s += f'<rect x="{x}" y="320" width="50" height="70" fill="{sh("#e0c99a",f)}"/><polygon points="{P([(x-6,320),(x+25,250),(x+56,320)])}" fill="{sh("#b5652f",f)}"/>'
    return s
def bridge(cx, f, v, r):
    s = ''.join(f'<rect x="{x}" y="320" width="14" height="150" fill="{sh("#5a5a60",f)}"/>' for x in (cx-210, cx+196))
    return s + f'<path d="M{cx-203},330 Q{cx},470 {cx+203},330" stroke="{sh("#44444a",f)}" stroke-width="4" fill="none"/><rect x="40" y="440" width="820" height="8" fill="{sh("#6a6a70",f)}"/>'
def cabin(cx, f, v, r):
    s = ''
    for dx, sc in ((-150, 1), (110, 1.3), (300, .8)):
        x = cx+dx; w = 80*sc; s += f'<rect x="{x}" y="{455-50*sc}" width="{w}" height="{50*sc}" fill="{sh("#d9b98a",f)}"/><polygon points="{P([(x-8,455-50*sc),(x+w/2,455-90*sc),(x+w+8,455-50*sc)])}" fill="{sh("#a8472e",f)}"/><rect x="{x+w/2-8}" y="{455-34*sc}" width="16" height="{20*sc}" fill="{"#ffd36b" if v>=2 else sh("#4a3a2a",f)}"/>'
    return s
def tents(cx, f, v, r):
    return ''.join(f'<polygon points="{P([(x,470),(x+45,410),(x+90,470)])}" fill="{sh("#f6f2e8",f)}"/><rect x="{x+38}" y="440" width="14" height="30" fill="{"#ffd36b" if v>=2 else sh("#666666",f)}"/>' for x in range(cx-260, cx+240, 130))
def rock(cx, f, v, r):
    return f'<polygon points="{P([(cx-140,470),(cx-100,300),(cx-70,250),(cx+70,250),(cx+110,310),(cx+150,470)])}" fill="{sh("#8a6f55",f)}"/><path d="M{cx-72},250 Q{cx},215 {cx+72},250Z" fill="{sh("#2f7a3a",f)}"/>'
def pagoda(cx, f, v, r):
    s = ''
    for i in range(4):
        w = 250 - i*50; y = 455 - i*72
        s += f'<rect x="{cx-w/2+14}" y="{y-60}" width="{w-28}" height="60" fill="{sh("#f1e1b8",f)}"/><path d="M{cx-w/2-24},{y-56} Q{cx},{y-90} {cx+w/2+24},{y-56} L{cx+w/2},{y-44} H{cx-w/2}Z" fill="{sh("#c8302a" if i%2==0 else "#e0a030",f)}"/>'
    return s + f'<rect x="{cx-2}" y="{455-4*72-40}" width="4" height="50" fill="#e0a030"/>'
LM = {'dome': dome, 'palace': lambda cx, f, v, r: dome(cx, f, v, r, '#f0c890', False), 'goldendome': lambda cx, f, v, r: dome(cx, f, v, r, '#e8b64a', True),
      'gopuram': gopuram, 'fort': fort, 'eiffel': eiffel, 'pyramids': pyramids, 'balloons': balloons, 'overwater': overwater, 'sails': sails, 'stupa': stupa,
      'monastery': monastery, 'bigben': bigben, 'burj': burj, 'petronas': petronas, 'marina': marina, 'nyc': nyc, 'gate': gate, 'charminar': charminar,
      'torii': torii, 'fuji': fuji, 'karst': karst, 'boat': boat, 'houseboat': houseboat, 'palms': palms, 'church': church, 'ghat': ghat, 'bridge': bridge,
      'cabin': cabin, 'tents': tents, 'rock': rock, 'pagoda': pagoda}

MAP = {
 'Kashmir Paradise': ('lake', ['boat']), 'Leh Ladakh Road Trip': ('mountbare', ['monastery']), 'Manali & Shimla Escape': ('mount', ['cabin']),
 'Golden Temple & Wagah': ('water', ['goldendome']), 'Rishikesh & Haridwar Yatra': ('water', ['bridge']), 'Jim Corbett Tiger Safari': ('jungle', []),
 'Golden Triangle': ('plain', ['dome']), 'Varanasi & Ayodhya Darshan': ('water', ['ghat']), 'Royal Rajasthan': ('plain', ['fort']),
 'Desert Forts of Jaisalmer': ('desert', ['fort']), 'Chandigarh & Kasauli Weekend': ('hills', ['cabin']), 'Goa Beach Break': ('beach', ['church', 'palms']),
 'Mumbai & Ajanta Ellora': ('water', ['gate']), 'Rann of Kutch & Gir Lions': ('salt', ['tents']), 'Khajuraho & Kanha Tigers': ('jungle', ['gopuram']),
 'Bastar & Chitrakote Falls': ('falls', []), 'Kolkata & Darjeeling': ('hillsnow', []), 'Sundarbans Mangrove Cruise': ('water', ['boat', 'palms']),
 'Puri, Konark & Chilika': ('beach', ['gopuram']), 'Buddhist Circuit': ('plain', ['stupa']), 'Jharkhand Waterfalls': ('falls', []),
 'Kaziranga & Meghalaya': ('jungle', []), 'Sikkim Himalaya': ('mount', ['monastery']), 'Tawang & Arunachal': ('mount', ['monastery']),
 'Nagaland Hornbill Trail': ('hills', ['cabin']), 'Manipur & Loktak Lake': ('lake', ['overwater']), 'Mizoram & Tripura Discovery': ('hills', ['palace']),
 'Backwaters & Spice Hills': ('water', ['houseboat', 'palms']), 'Temple Trail of Tamil Nadu': ('plain', ['gopuram']), 'Ooty & Kodaikanal Hills': ('hills', []),
 'Pondicherry Heritage Stay': ('beach', ['church']), 'Hampi & Mysore Palaces': ('plain', ['palace']), 'Coorg Coffee Country': ('hills', []),
 'Hyderabad Nizam Trail': ('plain', ['charminar']), 'Tirupati & Araku Valley': ('hills', ['gopuram']), 'Island Days in the Andamans': ('beach', ['palms']),
 'Lakshadweep Lagoons': ('beach', ['overwater']),
 'Dubai Desert & Skyline': ('city', ['burj']), 'Singapore & Sentosa': ('city', ['marina']), 'Bangkok & Phuket': ('beach', ['pagoda']),
 'Bali Island Retreat': ('hills', ['gopuram']), 'Maldives Overwater Escape': ('water', ['overwater']), 'Paris & Swiss Alps': ('city', ['eiffel']),
 'London & Scotland': ('city', ['bigben']), 'Tokyo & Mount Fuji': ('water', ['fuji', 'torii']), 'Kuala Lumpur & Langkawi': ('city', ['petronas']),
 'Sri Lanka Ramayana & Beaches': ('hills', ['rock']), 'Nepal Kathmandu & Pokhara': ('mount', ['stupa']), 'Bhutan Happiness Trail': ('mount', ['monastery']),
 'Turkey Istanbul & Cappadocia': ('plain', ['balloons', 'dome']), 'Vietnam Ha Long & Hanoi': ('water', ['karst', 'boat']), 'New York & Niagara': ('city', ['nyc']),
 'Sydney & Great Barrier Reef': ('water', ['sails']), 'Mauritius Island Holiday': ('beach', ['palms']), 'Egypt Pyramids & Nile': ('desert', ['pyramids'])}

def render(title, v):
    base, marks = MAP[title]; r = random.Random(slug(title)); (c1, c2), f = SKY[v]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#s)"/>']
    sx, sy = SUN[v]
    if v == 3:
        o += [f'<circle cx="{r.randint(0,W)}" cy="{r.randint(10,230)}" r="{r.choice([1,1.5,2])}" fill="#fff" opacity=".85"/>' for _ in range(70)]
        o.append(f'<circle cx="{sx}" cy="{sy}" r="34" fill="#f4f1de"/><circle cx="{sx+14}" cy="{sy-8}" r="30" fill="{c1}"/>')
    else:
        o.append(f'<circle cx="{sx}" cy="{sy}" r="90" fill="#fff6c8" opacity=".35"/><circle cx="{sx}" cy="{sy}" r="40" fill="#fff3b0"/>')
    o.append(BASES[base](r, f, v))
    cx = [450, 340, 560, 450][v]
    for m in marks: o.append(LM[m](cx, f, v, r))
    o.append('</svg>')
    return ''.join(o)

sql = open('/home/claude/wanderly/database.sql').read()
titles = re.findall(r"^\('([^']+)'", sql, re.M)
assert set(titles) == set(MAP), (set(titles) ^ set(MAP))
for t in titles:
    d = f'/home/claude/wanderly/assets/img/{slug(t)}'; os.makedirs(d, exist_ok=True)
    for v in range(4): open(f'{d}/{v+1}.svg', 'w').write(render(t, v))
print(len(titles), 'packages ->', len(titles)*4, 'images')
