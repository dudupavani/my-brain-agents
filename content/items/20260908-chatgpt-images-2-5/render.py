from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
ROOT = Path(__file__).parent
OUT = ROOT / "deliverables"
OUT.mkdir(exist_ok=True)

BG = "#252633"
BLUE = "#1C5DFF"
BLUE_LIGHT = "#8CA9FF"
WHITE = "#F8F8F5"
MUTED = "#BEC6E8"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def wrap(draw, text, fnt, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = word if not line else f"{line} {word}"
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, text, x, y, width, fnt, fill, gap=12):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def base():
    return Image.new("RGB", (W, H), BG)


def save(img, n):
    img.save(OUT / f"slide-{n:02d}.png", "PNG", optimize=True)

# 1
img = base(); d = ImageDraw.Draw(img)
d.rounded_rectangle((70, 78, 1010, 1272), radius=56, outline="#41445D", width=3)
d.text((110, 125), "CHATGPT IMAGES 2.5", font=font(26, True), fill=BLUE_LIGHT)
y = text_block(d, "Agora você pode desenhar dentro do", 110, 245, 850, font(72, True), WHITE, 8)
d.text((110, y + 4), "ChatGPT", font=font(98, True), fill=BLUE_LIGHT)
d.text((110, y + 116), "para guiar uma imagem.", font=font(72, True), fill=WHITE)
# abstract sketch-to-image path
for x, y0, r in [(170, 940, 20), (360, 865, 28), (590, 945, 22), (815, 830, 38)]:
    d.ellipse((x-r, y0-r, x+r, y0+r), outline=BLUE_LIGHT, width=5)
d.line((190, 930, 335, 875, 565, 935, 780, 840), fill=BLUE, width=10, joint="curve")
d.text((110, 1185), "01", font=font(24, True), fill=MUTED)
save(img, 1)

# 2
img = base(); d = ImageDraw.Draw(img)
d.rounded_rectangle((0, 0, W, 590), radius=0, fill=BLUE)
d.rounded_rectangle((0, 520, W, H), radius=70, fill=BG)
d.text((105, 135), "O que mudou", font=font(30, True), fill="#D8E2FF")
d.text((105, 245), "Mais", font=font(104, True), fill=WHITE)
d.text((105, 360), "controle.", font=font(104, True), fill=WHITE)
d.text((105, 700), "A OpenAI lançou o", font=font(48, True), fill=WHITE)
d.text((105, 770), "ChatGPT Images 2.5.", font=font(48, True), fill=BLUE_LIGHT)
text_block(d, "A promessa é simples: mais controle para criar, editar e refinar imagens.", 105, 910, 820, font(39), WHITE, 15)
d.text((105, 1185), "02", font=font(24, True), fill=MUTED)
save(img, 2)

# 3
img = base(); d = ImageDraw.Draw(img)
d.text((105, 118), "O ponto prático", font=font(30, True), fill=BLUE_LIGHT)
d.text((105, 225), "Rascunho", font=font(78, True), fill=WHITE)
d.text((105, 330), "→ imagem", font=font(78, True), fill=BLUE_LIGHT)
d.rounded_rectangle((105, 515, 410, 765), radius=36, outline=BLUE_LIGHT, width=5)
d.line((155, 700, 230, 595, 320, 680, 370, 570), fill=BLUE_LIGHT, width=8, joint="curve")
d.polygon((415, 630, 485, 590, 485, 670), fill=BLUE)
d.rounded_rectangle((525, 515, 975, 765), radius=36, fill=BLUE)
d.ellipse((655, 565, 845, 715), outline=WHITE, width=7)
d.arc((685, 595, 815, 705), 200, 340, fill=WHITE, width=7)
text_block(d, "Com o Sketch, você faz um rascunho e usa esse desenho como referência para a imagem final.", 105, 885, 850, font(42), WHITE, 15)
d.text((105, 1185), "03", font=font(24, True), fill=MUTED)
save(img, 3)

# 4
img = base(); d = ImageDraw.Draw(img)
d.text((105, 115), "O que entra no processo", font=font(30, True), fill=BLUE_LIGHT)
items = [("Templates", "para começar."), ("Comentários", "para pedir ajustes."), ("Edições mais precisas", "sem refazer tudo.")]
y = 230
for i, (a, b) in enumerate(items):
    color = BLUE if i != 1 else "#3B72FF"
    d.rounded_rectangle((85, y, 995, y+205), radius=38, fill=color)
    d.text((125, y+42), a, font=font(53, True), fill=WHITE)
    d.text((125, y+113), b, font=font(38), fill="#E6ECFF")
    y += 240
d.text((105, 1185), "04", font=font(24, True), fill=MUTED)
save(img, 4)

# 5
img = base(); d = ImageDraw.Draw(img)
d.text((105, 120), "A mudança relevante", font=font(30, True), fill=BLUE_LIGHT)
text_block(d, "O salto não é só gerar uma imagem melhor.", 105, 245, 850, font(66, True), WHITE, 8)
d.rounded_rectangle((75, 700, 1005, 1125), radius=56, fill=BLUE)
text_block(d, "É conseguir transformar uma intenção visual em um processo mais controlável.", 120, 765, 800, font(57, True), WHITE, 12)
d.text((105, 1185), "05", font=font(24, True), fill=MUTED)
save(img, 5)
