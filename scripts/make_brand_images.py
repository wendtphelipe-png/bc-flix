"""Gera favicon/ícones e imagens de prévia (Open Graph) do site.

Uso (rodar localmente, as imagens geradas vão para o git):
    python scripts/make_brand_images.py --font caminho/PlusJakartaSans[wght].ttf

Precisa de Pillow. A fonte é a Plus Jakarta Sans (a mesma do site):
https://github.com/google/fonts/tree/main/ofl/plusjakartasans
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(BASE, 'assets', 'logo_final.png')
OUT_ICONS = os.path.join(BASE, 'assets', 'icons')
OUT_OG = os.path.join(BASE, 'assets', 'og')

NAVY = (10, 25, 47)
SLATE = (51, 65, 85)
RED = (165, 28, 36)
BG = (248, 250, 252)

# Imagens de prévia: arquivo -> (rótulo, título, subtítulo)
PREVIAS = {
    'og-home.jpg': ('INSTITUTO DE CIRURGIA BARIÁTRICA E METABÓLICA','Educação em Cirurgia\nBariátrica e Metabólica',
                    'Cirurgias ao vivo • BC Flix • Corpo docente internacional'),
    'og-live.jpg': ('TRANSMISSÃO AO VIVO', 'Live Surgery',
                    'Cirurgias bariátricas e metabólicas ao vivo,\ncom discussão técnica em tempo real'),
    'og-bcflix.jpg': ('STREAMING CIRÚRGICO', 'BC Flix',
                      'Acervo de cirurgias bariátricas e metabólicas\nreais, narradas passo a passo'),
    'og-professores.jpg': ('CORPO DOCENTE', 'Cirurgiões de referência',
                           'Especialistas em cirurgia bariátrica e\nmetabólica do Brasil e do mundo'),
    'og-webinar.jpg': ('BC WEBINARS', 'Webinars Bariatric Channel',
                       'Atualização científica em cirurgia\nbariátrica e metabólica'),
}


def fonte(path, size, peso):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def icone_bolhas(logo):
    """Recorta o símbolo de bolhas (parte esquerda da logo) e deixa quadrado."""
    simbolo = logo.crop((0, 0, 360, logo.height))
    bbox = simbolo.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    simbolo = simbolo.crop(bbox)
    lado = max(simbolo.size)
    quad = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    quad.alpha_composite(simbolo, ((lado - simbolo.width) // 2, (lado - simbolo.height) // 2))
    return quad


def gerar_icones(logo):
    os.makedirs(OUT_ICONS, exist_ok=True)
    simbolo = icone_bolhas(logo)
    # Favicon transparente (aba do navegador)
    simbolo.resize((256, 256), Image.LANCZOS).save(
        os.path.join(BASE, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    simbolo.resize((32, 32), Image.LANCZOS).save(os.path.join(OUT_ICONS, 'favicon-32.png'))
    # Ícones com fundo branco (atalho no celular)
    for nome, tam in [('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512)]:
        fundo = Image.new('RGBA', (tam, tam), (255, 255, 255, 255))
        s = simbolo.resize((int(tam * 0.72),) * 2, Image.LANCZOS)
        fundo.alpha_composite(s, ((tam - s.width) // 2, (tam - s.height) // 2))
        fundo.convert('RGB').save(os.path.join(OUT_ICONS, nome), optimize=True)
    print(' -> favicon.ico e assets/icons/ gerados')


def gerar_previas(logo, font_path):
    os.makedirs(OUT_OG, exist_ok=True)
    simbolo = icone_bolhas(logo)
    W, H = 1200, 630
    f_rot = fonte(font_path, 26, 800)
    f_tit = fonte(font_path, 72, 800)
    f_sub = fonte(font_path, 34, 500)
    f_url = fonte(font_path, 26, 700)
    logo_p = logo.resize((int(logo.width * 70 / logo.height), 70), Image.LANCZOS)
    marca = simbolo.resize((560, 560), Image.LANCZOS)
    a = marca.getchannel('A').point(lambda v: int(v * 0.07))
    marca.putalpha(a)
    for nome, (rotulo, titulo, sub) in PREVIAS.items():
        img = Image.new('RGBA', (W, H), BG + (255,))
        img.alpha_composite(marca, (W - 470, H - 500))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 14, H), fill=RED)
        img.alpha_composite(logo_p, (70, 55))
        y = 200
        d.text((72, y), rotulo, font=f_rot, fill=RED)
        y += 50
        d.multiline_text((70, y), titulo, font=f_tit, fill=NAVY, spacing=8)
        y += d.multiline_textbbox((70, y), titulo, font=f_tit, spacing=8)[3] - y + 28
        d.multiline_text((72, y), sub, font=f_sub, fill=SLATE, spacing=10)
        d.text((72, H - 70), 'bariatricchannel.com', font=f_url, fill=RED)
        img.convert('RGB').save(os.path.join(OUT_OG, nome), quality=88, optimize=True, progressive=True)
        print(f' -> assets/og/{nome}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--font', required=True, help='Plus Jakarta Sans (variável ou ExtraBold)')
    args = ap.parse_args()
    logo = Image.open(LOGO).convert('RGBA')
    gerar_icones(logo)
    gerar_previas(logo, args.font)
