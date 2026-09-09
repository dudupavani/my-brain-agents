from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
REPO = ROOT.parents[2]
TEMPLATES = REPO / '.agents/skills/instagram-carousel/assets/templates'
OUT = ROOT / 'deliverables'
ASSETS = OUT / 'assets'
OUT.mkdir(exist_ok=True)

W, H = 1080, 1350
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
WHITE = '#F8F8F5'
DARK = '#3f3f49'
BLUE = '#2158f4'


def f(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def cover(src, size):
    src = src.convert('RGB')
    scale = max(size[0] / src.width, size[1] / src.height)
    resized = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
    x = (resized.width - size[0]) // 2
    y = (resized.height - size[1]) // 2
    return resized.crop((x, y, x + size[0], y + size[1]))


def rounded_media(img, src_path, box, radius=70):
    media = cover(Image.open(src_path), (box[2]-box[0], box[3]-box[1]))
    mask = Image.new('L', media.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, media.width, media.height), radius=radius, fill=255)
    img.paste(media, box[:2], mask)


def wrap(draw, text, font_obj, width):
    words, lines, line = text.split(), [], ''
    for word in words:
        candidate = word if not line else line + ' ' + word
        if draw.textbbox((0, 0), candidate, font=font_obj)[2] <= width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text(draw, text, x, y, width, font_obj, fill=WHITE, line_gap=8):
    for line in wrap(draw, text, font_obj, width):
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_gap


def base(name):
    return Image.open(TEMPLATES / name).convert('RGB')


def wipe(draw, box, fill):
    draw.rounded_rectangle(box, radius=0, fill=fill)

# Slide 1 — reference-01: image top, hook bottom
img = base('reference-01.jpg'); d = ImageDraw.Draw(img)
rounded_media(img, ASSETS/'openai-sketch.png', (72, 80, 1010, 905), 76)
# replace hook placeholder while retaining template's lower region and arrow
d.rounded_rectangle((45, 840, 910, 1250), radius=0, fill=DARK)
draw_text(d, 'Agora você pode desenhar no ChatGPT para guiar uma imagem.', 68, 900, 780, f(57), WHITE, 4)
img.save(OUT/'slide-01.png', 'PNG', optimize=True)

# Slide 2 — reference-02: upper headline, lower support text
img = base('reference-02.jpg'); d = ImageDraw.Draw(img)
d.rounded_rectangle((65, 120, 1010, 655), radius=0, fill=BLUE)
draw_text(d, 'O ChatGPT agora aceita rascunhos como referência visual.', 105, 190, 790, f(53, True), WHITE, 6)
d.rounded_rectangle((65, 635, 925, 1160), radius=0, fill=DARK)
draw_text(d, 'A OpenAI anunciou o ChatGPT Images 2.5 com novos controles de criação e edição.', 105, 710, 780, f(40), WHITE, 10)
img.save(OUT/'slide-02.png', 'PNG', optimize=True)

# Slide 3 — reference-03: text top, image bottom
img = base('reference-03.jpg'); d = ImageDraw.Draw(img)
d.rounded_rectangle((75, 75, 980, 525), radius=0, fill=DARK)
draw_text(d, 'Com o Sketch, você faz um desenho simples e usa esse rascunho como referência para a imagem final.', 95, 90, 845, f(51, True), WHITE, 7)
rounded_media(img, ASSETS/'openai-sketch.png', (74, 575, 1010, 1265), 76)
img.save(OUT/'slide-03.png', 'PNG', optimize=True)

# Slide 4 — reference-02: same exact template, new copy in its two text placeholders
img = base('reference-02.jpg'); d = ImageDraw.Draw(img)
d.rounded_rectangle((65, 120, 1010, 655), radius=0, fill=BLUE)
draw_text(d, 'Templates para começar. Comentários para pedir ajustes.', 105, 190, 790, f(53, True), WHITE, 7)
d.rounded_rectangle((65, 635, 925, 1160), radius=0, fill=DARK)
draw_text(d, 'Edições mais precisas sem refazer tudo.', 105, 740, 785, f(53), WHITE, 8)
img.save(OUT/'slide-04.png', 'PNG', optimize=True)

# Slide 5 — reference-03: text top, official editing media bottom
img = base('reference-03.jpg'); d = ImageDraw.Draw(img)
d.rounded_rectangle((75, 75, 980, 535), radius=0, fill=DARK)
draw_text(d, 'O salto não é só gerar uma imagem melhor. É conduzir uma intenção visual até um resultado mais próximo do que você imaginou.', 95, 90, 845, f(48, True), WHITE, 7)
rounded_media(img, ASSETS/'openai-editing.png', (74, 575, 1010, 1265), 76)
img.save(OUT/'slide-05.png', 'PNG', optimize=True)
