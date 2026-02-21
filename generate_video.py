"""텅장실험실 — 노트북 TOP5 영상 (실험실 테마 UI)"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1080, 1920  # 쇼츠 세로 9:16
FPS = 24
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "notebook_top5.mp4")

# ─── 텅장실험실 브랜드 컬러 ───
BRAND = {
    "bg_top": (8, 12, 28),
    "bg_bottom": (2, 4, 14),
    "neon_green": (0, 255, 170),       # 실험실 메인 네온
    "neon_blue": (0, 180, 255),
    "neon_pink": (255, 50, 150),
    "card_bg": (18, 22, 42),
    "card_border": (40, 50, 80),
    "text_white": (240, 245, 255),
    "text_dim": (120, 130, 160),
    "text_muted": (70, 80, 110),
    "danger": (255, 70, 70),
    "success": (0, 230, 150),
    "warning": (255, 200, 50),
}

PRODUCT_COLORS = {
    1: (255, 208, 0),
    2: (0, 180, 255),
    3: (0, 255, 170),
    4: (180, 120, 255),
    5: (255, 140, 50),
}

PRODUCTS = [
    {
        "num": 1, "tag": "EXPERIMENT #1", "subtitle": "가성비 끝판왕",
        "name": "레노버 Slim3 OLED", "image": None, "color": (255, 208, 0),
        "price": "~65만원", "rocket": True,
        "specs": [("CPU", "Ryzen 5 8640HS"), ("RAM", "8GB DDR5"), ("SSD", "256GB"),
                  ("Display", '14" OLED FHD+'), ("Weight", "1.33kg"), ("Battery", "15h")],
        "scores": {"성능": 70, "화면": 95, "휴대성": 80, "배터리": 65, "가성비": 98},
        "pros": ["60만원대 유일 OLED", "1.33kg 가볍다", "DCI-P3 100%"],
        "cons": ["RAM 8GB 기본", "FreeDOS"],
        "verdict": "예산 빠듯한 문과생, 인강러",
    },
    {
        "num": 2, "tag": "EXPERIMENT #2", "subtitle": "넓은 화면 만능형",
        "name": "ASUS 비보북 S16", "image": "asus_vivobook.png", "color": (0, 180, 255),
        "price": "~96만원", "rocket": True,
        "specs": [("CPU", "Ryzen AI 7 350"), ("RAM", "16GB DDR5"), ("SSD", "512GB"),
                  ("Display", '16" IPS FHD+'), ("Weight", "1.70kg"), ("Battery", "23h")],
        "scores": {"성능": 85, "화면": 70, "휴대성": 55, "배터리": 88, "가성비": 85},
        "pros": ["16인치 넓은 화면", "16GB+512GB 기본", "배터리 23시간"],
        "cons": ["1.70kg 무거움", "IPS 패널"],
        "verdict": "이과/공학생, 코딩러",
    },
    {
        "num": 3, "tag": "EXPERIMENT #3", "subtitle": "깃털 무게",
        "name": "ASUS 젠북 A14", "image": "asus_zenbook.jpg", "color": (0, 255, 170),
        "price": "~107만원", "rocket": True,
        "specs": [("CPU", "Snapdragon X Plus"), ("RAM", "16GB LPDDR5X"), ("SSD", "512GB"),
                  ("Display", '14" OLED HDR'), ("Weight", "0.98kg"), ("Battery", "26h")],
        "scores": {"성능": 75, "화면": 92, "휴대성": 99, "배터리": 95, "가성비": 78},
        "pros": ["0.98kg 초경량", "OLED 600nit", "배터리 26시간"],
        "cons": ["ARM 호환성", "확장 불가"],
        "verdict": "매일 등교, 카페 작업러",
    },
    {
        "num": 4, "tag": "EXPERIMENT #4", "subtitle": "화면 미쳤다",
        "name": "갤럭시북5 프로 14", "image": "samsung_galaxybook.jpg", "color": (180, 120, 255),
        "price": "~176만원", "rocket": True,
        "specs": [("CPU", "Core Ultra 5 S2"), ("RAM", "16GB"), ("SSD", "256GB"),
                  ("Display", '14" AMOLED 2.8K'), ("Weight", "1.23kg"), ("Battery", "21h")],
        "scores": {"성능": 88, "화면": 99, "휴대성": 82, "배터리": 80, "가성비": 55},
        "pros": ["2880x1800 AMOLED", "120Hz", "삼성 AS"],
        "cons": ["256GB 부족", "가격 높음"],
        "verdict": "디자인/영상 전공, 갤럭시 유저",
    },
    {
        "num": 5, "tag": "EXPERIMENT #5", "subtitle": "배터리 괴물",
        "name": "LG 그램 2026 15", "image": "lg_gram.jpg", "color": (255, 140, 50),
        "price": "~180만원", "rocket": True,
        "specs": [("CPU", "Ryzen AI 5 435"), ("RAM", "16GB"), ("SSD", "512GB"),
                  ("Display", '15.6" FHD IPS'), ("Weight", "1.29kg"), ("Battery", "32h")],
        "scores": {"성능": 80, "화면": 60, "휴대성": 85, "배터리": 99, "가성비": 58},
        "pros": ["15.6인치 1.29kg", "배터리 32시간", "SSD 확장"],
        "cons": ["FHD 아쉬움", "OLED 아님"],
        "verdict": "코딩/개발, 하루종일 밖에서",
    },
]

random.seed(42)
PARTICLES = [(random.randint(0, WIDTH), random.randint(0, HEIGHT),
              random.uniform(0.5, 2.5), random.random(), random.choice(["g", "b", "w"])) for _ in range(100)]


def FindFont():
    for p in ["C:/Windows/Fonts/malgunbd.ttf", "C:/Windows/Fonts/malgun.ttf"]:
        if os.path.exists(p):
            return p
    return None


def LoadProductImage(filename, targetSize=(420, 340)):
    if not filename:
        return None
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        return None
    try:
        img = Image.open(path).convert("RGBA")
        img.thumbnail(targetSize, Image.LANCZOS)
        return img
    except Exception:
        return None


def Gradient(topC, botC):
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        r = y / HEIGHT
        draw.line([(0, y), (WIDTH, y)], fill=tuple(int(topC[i] + (botC[i] - topC[i]) * r) for i in range(3)))
    return img


def DrawParticles(draw, t, color=None):
    for px, py, size, phase, pType in PARTICLES:
        twinkle = (math.sin(t * 1.5 + phase * 6.28) + 1) / 2
        if pType == "g":
            c = (0, int(80 + 60 * twinkle), int(50 + 40 * twinkle))
        elif pType == "b":
            c = (0, int(50 + 40 * twinkle), int(80 + 60 * twinkle))
        else:
            c = (int(40 + 30 * twinkle),) * 3
        if color:
            c = tuple(int(color[i] * 0.15 * twinkle) for i in range(3))
        draw.ellipse([(px - size, py - size), (px + size, py + size)], fill=c)


def DrawScanlines(draw, alpha=8):
    for y in range(0, HEIGHT, 4):
        draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0), width=1)


def DrawHexGrid(draw, color, spacing=160):
    c = tuple(max(0, v // 12) for v in color)
    for x in range(-50, WIDTH + 50, spacing):
        for y in range(-50, HEIGHT + 50, spacing):
            offset = spacing // 2 if (y // spacing) % 2 else 0
            cx, cy = x + offset, y
            r = 30
            points = [(cx + r * math.cos(math.radians(60 * i - 30)),
                        cy + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]
            draw.polygon(points, outline=c)


def DrawCard(draw, x, y, w, h, radius=16):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=radius, fill=BRAND["card_bg"])
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=radius, outline=BRAND["card_border"], width=1)


def DrawNeonLine(draw, y, color, width=2):
    glow = tuple(max(0, v // 3) for v in color)
    draw.line([(0, y - 1), (WIDTH, y - 1)], fill=glow, width=1)
    draw.line([(0, y), (WIDTH, y)], fill=color, width=width)
    draw.line([(0, y + width), (WIDTH, y + width)], fill=glow, width=1)


def DrawProgressBar(draw, x, y, w, h, percent, color, fonts):
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=h // 2, fill=(25, 30, 50))
    fillW = int(w * percent / 100)
    if fillW > 0:
        draw.rounded_rectangle([(x, y), (x + fillW, y + h)], radius=h // 2, fill=color)
    glow = tuple(min(255, int(v * 1.3)) for v in color)
    if fillW > 2:
        draw.rounded_rectangle([(x + 1, y + 1), (x + fillW - 1, y + h // 2)], radius=h // 4,
                                fill=glow)


def DrawBrandWatermark(draw, fonts):
    bbox = draw.textbbox((0, 0), "텅장실험실", font=fonts["watermark"])
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x, HEIGHT - 60), "텅장실험실", font=fonts["watermark"], fill=BRAND["text_muted"])
    draw.rectangle([(x - 12, HEIGHT - 58), (x - 4, HEIGHT - 34)], fill=BRAND["neon_green"])


def MakeBg(t, color=None):
    c = color or BRAND["neon_green"]
    img = Gradient(BRAND["bg_top"], BRAND["bg_bottom"])
    draw = ImageDraw.Draw(img)
    DrawHexGrid(draw, c)
    DrawParticles(draw, t, c)
    DrawScanlines(draw)
    return img, draw


# ─────────────────────────────────────
# 인트로 프레임
# ─────────────────────────────────────
def RenderIntro(t, fonts):
    img, draw = MakeBg(t)
    green = BRAND["neon_green"]
    cx = WIDTH // 2

    if t < 6:
        DrawNeonLine(draw, 600, green)
        DrawNeonLine(draw, 1200, green)

        # 비커 아이콘
        bx, by = cx, 780
        draw.rounded_rectangle([(bx - 35, by - 70), (bx + 35, by + 15)], radius=8, outline=green, width=2)
        draw.ellipse([(bx - 12, by - 45), (bx + 12, by - 18)], fill=green)
        draw.rectangle([(bx - 25, by - 88), (bx + 25, by - 70)], fill=green)

        f = fonts["hero"]
        text = "텅장실험실"
        bbox = draw.textbbox((0, 0), text, font=f)
        tw = bbox[2] - bbox[0]
        x = (WIDTH - tw) // 2
        for offset in [3, 2, 1]:
            gc = tuple(max(0, v - 80 * offset) for v in green)
            draw.text((x, 850 + offset), text, font=f, fill=gc)
        draw.text((x, 850), text, font=f, fill=green)

        sub = "NOTEBOOK LAB REPORT"
        bbox2 = draw.textbbox((0, 0), sub, font=fonts["tag"])
        sw = bbox2[2] - bbox2[0]
        draw.text(((WIDTH - sw) // 2, 970), sub, font=fonts["tag"], fill=BRAND["text_dim"])

    elif t < 12:
        DrawCard(draw, 40, 500, WIDTH - 80, 550, 20)
        draw.text((80, 530), "[SUBJECT]", font=fonts["tag"], fill=green)
        draw.text((80, 590), "2026", font=fonts["title"], fill=BRAND["warning"])
        draw.text((80, 660), "대학생 노트북", font=fonts["title"], fill=BRAND["text_white"])
        draw.text((80, 740), "TOP 5", font=fonts["hero"], fill=green)
        draw.text((80, 870), "60만원 → 180만원", font=fonts["medium"], fill=BRAND["warning"])
        draw.text((80, 930), "가성비부터 프리미엄까지", font=fonts["body"], fill=BRAND["text_dim"])
        draw.text((80, 970), "전공별 분석 실험 보고서", font=fonts["body"], fill=BRAND["text_dim"])

    else:
        f = fonts["large"]
        text = "실험 시작"
        bbox = draw.textbbox((0, 0), text, font=f)
        tw = bbox[2] - bbox[0]
        x = (WIDTH - tw) // 2
        draw.text((x, HEIGHT // 2 - 40), text, font=f, fill=green)
        if int(t * 3) % 2:
            draw.rectangle([(x + tw + 10, HEIGHT // 2 - 35), (x + tw + 22, HEIGHT // 2 + 35)], fill=green)

    DrawBrandWatermark(draw, fonts)
    return np.array(img)


# ─────────────────────────────────────
# 제품 1페이지 프레임
# ─────────────────────────────────────
def RenderProduct(product, productImg, fonts, t):
    color = product["color"]
    img, draw = MakeBg(t, color)
    pad = 40

    # ── 상단 바 ──
    DrawNeonLine(draw, 80, color)
    draw.rectangle([(0, 0), (WIDTH, 79)], fill=BRAND["card_bg"])
    draw.text((pad, 22), product["tag"], font=fonts["tag"], fill=color)
    draw.rounded_rectangle([(WIDTH - 200, 20), (WIDTH - pad, 56)], radius=18, fill=color)
    draw.text((WIDTH - 185, 23), "TESTING", font=fonts["badge"], fill=(10, 10, 20))

    # ── 제품명 + 가격 ──
    y = 100
    draw.text((pad, y), product["subtitle"], font=fonts["medium"], fill=BRAND["text_dim"])
    y += 50
    draw.text((pad, y), product["name"], font=fonts["productName"], fill=BRAND["text_white"])
    y += 65

    draw.rounded_rectangle([(pad, y), (pad + 180, y + 40)], radius=12, fill=BRAND["danger"])
    draw.text((pad + 15, y + 5), product["price"], font=fonts["price"], fill=(255, 255, 255))
    if product["rocket"]:
        draw.rounded_rectangle([(pad + 200, y), (pad + 360, y + 40)], radius=12, outline=BRAND["neon_green"], width=1)
        draw.text((pad + 215, y + 5), "로켓배송", font=fonts["price"], fill=BRAND["neon_green"])
    y += 60

    # ── 이미지 ──
    DrawCard(draw, pad, y, WIDTH - pad * 2, 350)
    if productImg:
        resized = productImg.copy()
        resized.thumbnail((WIDTH - pad * 2 - 40, 320), Image.LANCZOS)
        imgX = pad + (WIDTH - pad * 2 - resized.width) // 2
        imgY = y + (350 - resized.height) // 2
        if resized.mode == "RGBA":
            img.paste(resized, (imgX, imgY), resized)
        else:
            img.paste(resized, (imgX, imgY))
    else:
        bbox = draw.textbbox((0, 0), product["name"], font=fonts["medium"])
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y + 150), product["name"], font=fonts["medium"], fill=color)
    y += 370

    # ── 스펙 ──
    DrawCard(draw, pad, y, WIDTH - pad * 2, 280)
    draw.text((pad + 15, y + 10), "[SPECS]", font=fonts["small"], fill=color)
    specY = y + 40
    for label, value in product["specs"]:
        draw.text((pad + 20, specY), label, font=fonts["specLabel"], fill=BRAND["text_dim"])
        draw.text((pad + 200, specY), value, font=fonts["specValue"], fill=BRAND["text_white"])
        draw.line([(pad + 15, specY + 33), (WIDTH - pad - 15, specY + 33)], fill=BRAND["card_border"], width=1)
        specY += 38
    y += 295

    # ── LAB SCORE ──
    DrawCard(draw, pad, y, WIDTH - pad * 2, 330)
    draw.text((pad + 15, y + 10), "[LAB SCORE]", font=fonts["small"], fill=color)
    barY = y + 45
    for label, score in product["scores"].items():
        draw.text((pad + 20, barY), label, font=fonts["scoreLabel"], fill=BRAND["text_dim"])
        DrawProgressBar(draw, pad + 130, barY + 5, WIDTH - pad * 2 - 230, 22, score, color, fonts)
        draw.text((WIDTH - pad - 60, barY), f"{score}", font=fonts["scoreLabel"], fill=BRAND["text_white"])
        barY += 48
    avgScore = sum(product["scores"].values()) // len(product["scores"])
    draw.text((pad + 20, barY + 8), "TOTAL", font=fonts["scoreLabel"], fill=color)
    draw.text((WIDTH - pad - 130, barY), f"{avgScore}/100", font=fonts["totalScore"], fill=color)
    y += 345

    # ── 장단점 + 판정 ──
    DrawCard(draw, pad, y, (WIDTH - pad * 2) // 2 - 10, 200)
    draw.text((pad + 15, y + 8), "[PROS]", font=fonts["small"], fill=BRAND["success"])
    proY = y + 38
    for pro in product["pros"]:
        draw.ellipse([(pad + 15, proY + 8), (pad + 25, proY + 18)], fill=BRAND["success"])
        draw.text((pad + 35, proY), pro, font=fonts["small"], fill=(200, 255, 230))
        proY += 36

    conX = WIDTH // 2 + 10
    DrawCard(draw, conX, y, (WIDTH - pad * 2) // 2 - 10, 200)
    draw.text((conX + 15, y + 8), "[CONS]", font=fonts["small"], fill=BRAND["danger"])
    conY = y + 38
    for con in product["cons"]:
        draw.text((conX + 15, conY), "× " + con, font=fonts["small"], fill=(255, 200, 200))
        conY += 36

    # 판정
    draw.text((pad + 15, y + 145), "추천:", font=fonts["specLabel"], fill=BRAND["text_dim"])
    draw.text((pad + 100, y + 145), product["verdict"], font=fonts["verdict"], fill=color)

    DrawBrandWatermark(draw, fonts)
    return np.array(img)


# ─────────────────────────────────────
# 비교표
# ─────────────────────────────────────
def RenderComparison(fonts, t):
    img, draw = MakeBg(t)
    green = BRAND["neon_green"]
    pad = 40

    # Header
    DrawNeonLine(draw, 80, green)
    draw.rectangle([(0, 0), (WIDTH, 79)], fill=BRAND["card_bg"])
    draw.text((pad, 20), "[COMPARISON]", font=fonts["tag"], fill=green)
    draw.text((pad + 250, 26), "실험 결과 비교", font=fonts["specLabel"], fill=BRAND["text_dim"])

    compData = [
        ("#1 Slim3 OLED", "~65만", "1.33kg", "OLED", "15h", 82, PRODUCT_COLORS[1]),
        ("#2 비보북 S16", "~96만", "1.70kg", "IPS", "23h", 77, PRODUCT_COLORS[2]),
        ("#3 젠북 A14", "~107만", "0.98kg", "OLED", "26h", 88, PRODUCT_COLORS[3]),
        ("#4 갤북5 프로", "~176만", "1.23kg", "AMOLED", "21h", 81, PRODUCT_COLORS[4]),
        ("#5 그램 2026", "~180만", "1.29kg", "IPS", "32h", 76, PRODUCT_COLORS[5]),
    ]

    highlights = {"#3 젠북 A14": "무게", "#5 그램 2026": "배터리", "#4 갤북5 프로": "화면"}

    y = 100
    cardH = 200
    for name, price, weight, display, battery, score, color in compData:
        DrawCard(draw, pad, y, WIDTH - pad * 2, cardH)
        draw.rectangle([(pad, y), (pad + 5, y + cardH)], fill=color)

        # Product name
        draw.text((pad + 20, y + 12), name, font=fonts["medium"], fill=color)

        # Price badge
        bbox = draw.textbbox((0, 0), price, font=fonts["price"])
        pw = bbox[2] - bbox[0]
        draw.rounded_rectangle([(WIDTH - pad - pw - 40, y + 12), (WIDTH - pad - 15, y + 48)],
                                radius=14, fill=BRAND["danger"])
        draw.text((WIDTH - pad - pw - 28, y + 16), price, font=fonts["price"], fill=(255, 255, 255))

        # Specs row — 3 columns
        specY = y + 60
        colW = (WIDTH - pad * 2 - 40) // 3
        specs = [("무게", weight), ("화면", display), ("배터리", battery)]
        for i, (label, val) in enumerate(specs):
            sx = pad + 20 + i * colW
            draw.text((sx, specY), label, font=fonts["small"], fill=BRAND["text_dim"])
            vc = BRAND["text_white"]
            if name in highlights and highlights[name] == label:
                vc = green
            draw.text((sx, specY + 28), val, font=fonts["specValue"], fill=vc)

        # Score bar
        barY = y + 140
        draw.text((pad + 20, barY), "SCORE", font=fonts["small"], fill=BRAND["text_dim"])
        DrawProgressBar(draw, pad + 120, barY + 4, WIDTH - pad * 2 - 220, 20, score, color, fonts)
        draw.text((WIDTH - pad - 55, barY), f"{score}", font=fonts["scoreLabel"], fill=color)

        y += cardH + 15

    # Recommendation section — 2 columns
    recY = y + 10
    DrawCard(draw, pad, recY, WIDTH - pad * 2, 320)
    draw.text((pad + 15, recY + 10), "[RECOMMENDATION]", font=fonts["small"], fill=green)

    recs = [
        ("문과/경영", "젠북 A14", PRODUCT_COLORS[3]),
        ("이과/공학", "비보북 S16", PRODUCT_COLORS[2]),
        ("디자인/영상", "갤북5 프로", PRODUCT_COLORS[4]),
        ("코딩/개발", "그램 2026", PRODUCT_COLORS[5]),
        ("예산 제한", "Slim3 OLED", PRODUCT_COLORS[1]),
    ]
    colW = (WIDTH - pad * 2 - 50) // 2
    for i, (major, pick, c) in enumerate(recs):
        col = i % 2
        row = i // 2
        rx = pad + 15 + col * (colW + 20)
        ry = recY + 50 + row * 85
        draw.rounded_rectangle([(rx, ry), (rx + colW, ry + 70)], radius=10, outline=c, width=1)
        draw.text((rx + 12, ry + 8), major, font=fonts["small"], fill=BRAND["text_dim"])
        draw.text((rx + 12, ry + 35), pick, font=fonts["specValue"], fill=c)

    DrawBrandWatermark(draw, fonts)
    return np.array(img)


# ─────────────────────────────────────
# 아웃트로
# ─────────────────────────────────────
def RenderOutro(phase, fonts, t):
    img, draw = MakeBg(t)
    green = BRAND["neon_green"]
    pad = 40

    DrawNeonLine(draw, 80, green)
    draw.rectangle([(0, 0), (WIDTH, 79)], fill=BRAND["card_bg"])
    draw.text((pad, 20), "[CONCLUSION]", font=fonts["tag"], fill=green)
    draw.text((pad + 230, 26), "실험 결론", font=fonts["specLabel"], fill=BRAND["text_dim"])

    recs = [
        ("돈 없으면", "레노버 Slim3 OLED", PRODUCT_COLORS[1]),
        ("코딩/큰화면", "ASUS 비보북 S16", PRODUCT_COLORS[2]),
        ("가벼운 게 최고", "ASUS 젠북 A14", PRODUCT_COLORS[3]),
        ("화면이 생명", "갤럭시북5 프로", PRODUCT_COLORS[4]),
        ("배터리 괴물", "LG 그램 2026", PRODUCT_COLORS[5]),
    ]

    y = 120
    for i, (label, value, c) in enumerate(recs):
        DrawCard(draw, pad, y, WIDTH - pad * 2, 100)
        draw.rectangle([(pad, y), (pad + 5, y + 100)], fill=c)
        draw.text((pad + 25, y + 15), label, font=fonts["medium"], fill=BRAND["text_dim"])
        bbox = draw.textbbox((0, 0), value, font=fonts["medium"])
        vw = bbox[2] - bbox[0]
        draw.text((WIDTH - pad - 20 - vw, y + 15), value, font=fonts["medium"], fill=c)
        draw.text((pad + 25, y + 60), "추천", font=fonts["small"], fill=c)
        y += 125

    if phase > 0.3:
        msgY = y + 30
        DrawCard(draw, pad, msgY, WIDTH - pad * 2, 210)
        draw.text((pad + 20, msgY + 20), "설명란에 구매 링크", font=fonts["body"], fill=BRAND["text_white"])
        draw.text((pad + 20, msgY + 58), "다 넣어뒀으니 관심 있는 거 눌러봐",
                  font=fonts["body"], fill=BRAND["text_white"])
        draw.text((pad + 20, msgY + 110), "구독하면 다음에는", font=fonts["body"], fill=green)
        draw.text((pad + 20, msgY + 148), "태블릿 추천도 올릴게", font=fonts["body"], fill=green)
        draw.text((pad + 20, msgY + 195), "※ 쿠팡 파트너스 활동의 일환으로 수수료를 제공받습니다",
                  font=fonts["small"], fill=BRAND["text_muted"])

    DrawBrandWatermark(draw, fonts)
    return np.array(img)


# ─────────────────────────────────────
# 타이틀 카드
# ─────────────────────────────────────
def RenderTitleCard(product, fonts, t):
    color = product["color"]
    img, draw = MakeBg(t, color)
    baseY = 550  # 세로 중앙 배치

    # 큰 번호 + 글로우
    numText = f"#{product['num']}"
    f = fonts["hero"]
    bbox = draw.textbbox((0, 0), numText, font=f)
    nw = bbox[2] - bbox[0]
    nx = (WIDTH - nw) // 2
    for off in [4, 2]:
        gc = tuple(max(0, v - 60 * off) for v in color)
        draw.text((nx, baseY + off), numText, font=f, fill=gc)
    draw.text((nx, baseY), numText, font=f, fill=color)

    # 태그
    tagBbox = draw.textbbox((0, 0), product["tag"], font=fonts["tag"])
    tagW = tagBbox[2] - tagBbox[0]
    draw.text(((WIDTH - tagW) // 2, baseY + 130), product["tag"], font=fonts["tag"], fill=BRAND["text_dim"])

    # 부제
    subF = fonts["title"]
    subBbox = draw.textbbox((0, 0), product["subtitle"], font=subF)
    sw = subBbox[2] - subBbox[0]
    draw.text(((WIDTH - sw) // 2, baseY + 190), product["subtitle"], font=subF, fill=BRAND["text_white"])

    # 제품명
    nameF = fonts["medium"]
    nameBbox = draw.textbbox((0, 0), product["name"], font=nameF)
    namew = nameBbox[2] - nameBbox[0]
    draw.text(((WIDTH - namew) // 2, baseY + 270), product["name"], font=nameF, fill=color)

    # 네온 라인
    DrawNeonLine(draw, baseY + 350, color, 1)

    DrawBrandWatermark(draw, fonts)
    return np.array(img)


def main():
    from moviepy import VideoClip

    fontPath = FindFont()
    if not fontPath:
        print("폰트 없음!")
        return
    print(f"폰트: {fontPath}")

    fonts = {
        "hero": ImageFont.truetype(fontPath, 100),
        "title": ImageFont.truetype(fontPath, 56),
        "large": ImageFont.truetype(fontPath, 68),
        "productName": ImageFont.truetype(fontPath, 48),
        "tag": ImageFont.truetype(fontPath, 32),
        "tagSub": ImageFont.truetype(fontPath, 28),
        "badge": ImageFont.truetype(fontPath, 24),
        "medium": ImageFont.truetype(fontPath, 38),
        "price": ImageFont.truetype(fontPath, 28),
        "specLabel": ImageFont.truetype(fontPath, 26),
        "specValue": ImageFont.truetype(fontPath, 28),
        "scoreLabel": ImageFont.truetype(fontPath, 26),
        "totalScore": ImageFont.truetype(fontPath, 40),
        "body": ImageFont.truetype(fontPath, 28),
        "verdict": ImageFont.truetype(fontPath, 34),
        "small": ImageFont.truetype(fontPath, 22),
        "watermark": ImageFont.truetype(fontPath, 24),
        "tableH": ImageFont.truetype(fontPath, 26),
        "tableL": ImageFont.truetype(fontPath, 24),
        "tableV": ImageFont.truetype(fontPath, 24),
    }

    print("이미지 로드...")
    productImages = {}
    for p in PRODUCTS:
        productImages[p["num"]] = LoadProductImage(p["image"])
        print(f"  {p['name']}: {'OK' if productImages[p['num']] else '플레이스홀더'}")

    INTRO_DUR = 16
    TITLE_DUR = 4
    PRODUCT_DUR = 18
    COMPARE_DUR = 18
    OUTRO_DUR = 16
    TOTAL = INTRO_DUR + len(PRODUCTS) * (TITLE_DUR + PRODUCT_DUR) + COMPARE_DUR + OUTRO_DUR
    print(f"총 길이: {TOTAL}초 ({TOTAL / 60:.1f}분)")

    def MakeFrame(t):
        if t < INTRO_DUR:
            return RenderIntro(t, fonts)

        t2 = t - INTRO_DUR
        productBlock = TITLE_DUR + PRODUCT_DUR
        productEnd = len(PRODUCTS) * productBlock

        if t2 < productEnd:
            idx = int(t2 // productBlock)
            localT = t2 - idx * productBlock
            if localT < TITLE_DUR:
                return RenderTitleCard(PRODUCTS[idx], fonts, t)
            else:
                return RenderProduct(PRODUCTS[idx], productImages[PRODUCTS[idx]["num"]], fonts, t)

        t3 = t2 - productEnd
        if t3 < COMPARE_DUR:
            return RenderComparison(fonts, t)

        t4 = t3 - COMPARE_DUR
        return RenderOutro(t4 / OUTRO_DUR, fonts, t)

    print("인코딩 시작...")
    video = VideoClip(MakeFrame, duration=TOTAL).with_fps(FPS)
    video.write_videofile(OUTPUT_PATH, fps=FPS, codec="libx264", audio=False,
                          preset="ultrafast", threads=4, logger="bar")

    size = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
    print(f"\n완료: {OUTPUT_PATH}")
    print(f"{TOTAL}초 ({TOTAL / 60:.1f}분) / {size:.1f}MB")


if __name__ == "__main__":
    main()
