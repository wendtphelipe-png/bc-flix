import json
from jinja2 import Environment, FileSystemLoader
import os
import shutil

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'database.json')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
DEPLOY_DIR = BASE_DIR

# Cria os diretórios de saída se não existirem
os.makedirs(os.path.join(DEPLOY_DIR, 'eventos'), exist_ok=True)
os.makedirs(os.path.join(DEPLOY_DIR, 'professores'), exist_ok=True)
os.makedirs(os.path.join(DEPLOY_DIR, 'assets'), exist_ok=True)

# Copia assets e vídeos se existirem
assets_to_copy = {
    'Logo_branco.mp4': 'Logo_branco.mp4',
    'BC institucional-1.mp4': 'bc_video.mp4',
    'Animação_de_Logo_com_VEO.mp4': 'animacao_logo.mp4',
    'Check-in.png': 'Check-in.png',
    'onça low.jpg': 'onça low.jpg',
    'IMG_2037.JPG.jpeg': 'paulo_reis_v2.jpg',
    'unnamed.png': 'apoio_institucional_v2.png',
    'logobcflix-removebg-preview.png': 'logobcflix-removebg-preview.png'
}

for src_name, dest_name in assets_to_copy.items():
    src_path = os.path.join(BASE_DIR, src_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, os.path.join(DEPLOY_DIR, 'assets', dest_name))
        print(f" -> Asset {dest_name} copiado para assets.")

# Copia Fotos do Design sem nome para assets/participantes
design_dir = os.path.join(BASE_DIR, 'Design sem nome')
participantes_dir = os.path.join(DEPLOY_DIR, 'assets', 'participantes')
os.makedirs(participantes_dir, exist_ok=True)
if os.path.exists(design_dir):
    for filename in os.listdir(design_dir):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            src_path = os.path.join(design_dir, filename)
            shutil.copy(src_path, os.path.join(participantes_dir, filename))
    print(f" -> Imagens da Galeria copiadas para assets/participantes.")

# Carrega os dados principais
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Mapeamento de Países: (Código ISO para bandeira, Nome por Extenso)
COUNTRY_INFO = {
    'AR': ('ar', 'Argentina'), 'ARG': ('ar', 'Argentina'),
    'ARE': ('ae', 'Emirados Árabes Unidos'), 'UAE': ('ae', 'Emirados Árabes Unidos'),
    'B': ('br', 'Brasil'), 'BR': ('br', 'Brasil'), 'BRA': ('br', 'Brasil'), 'Brasil': ('br', 'Brasil'),
    'BEL': ('be', 'Bélgica'),
    'BOL': ('bo', 'Bolívia'),
    'CAN': ('ca', 'Canadá'),
    'CHL': ('cl', 'Chile'),
    'COL': ('co', 'Colômbia'),
    'DEU': ('de', 'Alemanha'),
    'ECU': ('ec', 'Equador'),
    'EGY': ('eg', 'Egito'),
    'ENG': ('gb-eng', 'Inglaterra'),
    'ESP': ('es', 'Espanha'),
    'FRA': ('fr', 'França'),
    'GBR': ('gb', 'Reino Unido'),
    'GTM': ('gt', 'Guatemala'),
    'IND': ('in', 'Índia'),
    'IRL': ('ie', 'Irlanda'),
    'IRN': ('ir', 'Irã'),
    'ISR': ('il', 'Israel'),
    'ITA': ('it', 'Itália'),
    'KWT': ('kw', 'Kuwait'),
    'MEX': ('mx', 'México'),
    'PAN': ('pa', 'Panamá'),
    'PE': ('pe', 'Peru'), 'PER': ('pe', 'Peru'),
    'POR': ('pt', 'Portugal'), 'PRT': ('pt', 'Portugal'), 'PT': ('pt', 'Portugal'),
    'TUR': ('tr', 'Turquia'),
    'USA': ('us', 'Estados Unidos'),
    'VEN': ('ve', 'Venezuela')
}

# Carrega a nova base de palestrantes
PALESTRANTES_FILE = os.path.join(BASE_DIR, 'data', 'palestrantes_raw.json')
with open(PALESTRANTES_FILE, 'r', encoding='utf-8') as f:
    palestrantes_data = json.load(f)

# Enriquece dados com a URL da bandeira e nome completo
for p in palestrantes_data:
    pais_raw = p.get('País', '').upper()
    info = COUNTRY_INFO.get(pais_raw)
    
    if info:
        iso_code, full_name = info
        p['FlagURL'] = f"https://flagcdn.com/w40/{iso_code}.png"
        p['PaisNome'] = full_name
    else:
        p['FlagURL'] = None
        p['PaisNome'] = p.get('País') or 'INTERNACIONAL'
    
    # Fotos: as do antigo servidor de eventos (bariatricchannel.com/event/ e .com.br) não existem mais.
    # Fonte atual: assets/palestrantes/id/<ID>.jpg, extraídas da planilha
    # "Bariatric Channel - Palestrantes (foto, nome, currículo).xlsx" pelo mesmo ID.
    foto_id = os.path.join(BASE_DIR, 'assets', 'palestrantes', 'id', f"{p.get('ID')}.jpg")
    url = (p.get('Foto URL') or '').strip()
    if p.get('ID') and os.path.exists(foto_id):
        p['Foto URL'] = f"/assets/palestrantes/id/{p.get('ID')}.jpg"
    elif '/event/images/' in url:
        p['Foto URL'] = ''  # link morto: cai no avatar com as iniciais
    elif url and not url.startswith(('http', '/')):
        p['Foto URL'] = '/' + url.lstrip('./')  # caminho local relativo -> absoluto

# Mapeia cronograma por professor
speaker_schedules = {}
for evento in data.get('eventos', []):
    for item in evento.get('cronograma', []):
        pal_str = item.get('palestrante', '')
        if not pal_str: continue
        for p in palestrantes_data:
            nome = p.get('Nome', '')
            if nome and nome.lower() in pal_str.lower():
                if nome not in speaker_schedules:
                    speaker_schedules[nome] = []
                speaker_schedules[nome].append({
                    "evento": evento.get('titulo'),
                    "hora": item.get('hora'),
                    "titulo": item.get('titulo')
                })

# Configura o Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# -------
# 1. Gerar Index (Página Inicial)
# -------
print("Gerando home.html...")
# Cópia direta do index para deploy (ele já tem o design estático, no futuro podemos inserir os dados do db)
# Como o template index.html está estático, por enquanto apenas copiamos
# Atualizado: Agora renderizando dinamicamente com dados do database.json
index_template = env.get_template('home.html')
# Pegando o evento BCLS para exibir em destaque na home page
evento_destaque = data.get('eventos', [{}])[0]

# Próxima live da agenda (data/agenda.json). Some sozinha no dia seguinte à data.
from datetime import datetime, timedelta, timezone
hoje = (datetime.now(timezone.utc) - timedelta(hours=3)).date().isoformat()  # horário de Brasília
agenda_path = os.path.join(BASE_DIR, 'data', 'agenda.json')
agenda = {}
if os.path.exists(agenda_path):
    with open(agenda_path, 'r', encoding='utf-8') as f:
        agenda = json.load(f)
proximas_lives = sorted(
    [l for l in agenda.get('lives', []) if l.get('ativo') and l.get('data', '') >= hoje],
    key=lambda l: l['data']
)
live = proximas_lives[0] if proximas_lives else None
print(f" -> Live em destaque: {live['id'] if live else 'nenhuma (home abre na Amazon Week)'}")

output_index = index_template.render(
    evento_destaque=evento_destaque,
    live=live
)

with open(os.path.join(DEPLOY_DIR, 'home.html'), 'w', encoding='utf-8') as f:
    f.write(output_index)
with open(os.path.join(DEPLOY_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(output_index)

# -------
# 1.5 Gerar Masterclass Landing Page
# -------
print("Gerando masterclass.html...")
masterclass_template = env.get_template('masterclass.html')
output_masterclass = masterclass_template.render()
with open(os.path.join(DEPLOY_DIR, 'masterclass.html'), 'w', encoding='utf-8') as f:
    f.write(output_masterclass)

print("Gerando bc_amazon_week.html...")
bc_amazon_template = env.get_template('bc_amazon_week.html')
output_bc_amazon = bc_amazon_template.render(
    palestrantes=palestrantes_data
)
with open(os.path.join(DEPLOY_DIR, 'bc_amazon_week.html'), 'w', encoding='utf-8') as f:
    f.write(output_bc_amazon)

print("Gerando checkin_bc.html...")
# Check if template exists before attempting to render
if os.path.exists(os.path.join(TEMPLATES_DIR, 'checkin_bc.html')):
    checkin_template = env.get_template('checkin_bc.html')
    output_checkin = checkin_template.render()
    with open(os.path.join(DEPLOY_DIR, 'checkin_bc.html'), 'w', encoding='utf-8') as f:
        f.write(output_checkin)

print("Gerando config_evento.html...")
if os.path.exists(os.path.join(TEMPLATES_DIR, 'config_evento.html')):
    config_template = env.get_template('config_evento.html')
    output_config = config_template.render()
    with open(os.path.join(DEPLOY_DIR, 'config_evento.html'), 'w', encoding='utf-8') as f:
        f.write(output_config)

print("Gerando bcflix.html...")
if os.path.exists(os.path.join(TEMPLATES_DIR, 'bcflix.html')):
    bcflix_template = env.get_template('bcflix.html')
    output_bcflix = bcflix_template.render()
    with open(os.path.join(DEPLOY_DIR, 'bcflix.html'), 'w', encoding='utf-8') as f:
        f.write(output_bcflix)



# -------
# 2. Gerar Páginas de Eventos
# -------
print("Gerando páginas de eventos...")
evento_template = env.get_template('eventos/evento_detalhe.html')

# (Opcional) Gerar página de lista de eventos
# Para a demonstração, copiaremos uma index básica se existir, ou não fazer nada

for evento in data.get('eventos', []):
    output_html = evento_template.render(
        evento_titulo=evento.get('titulo'),
        evento_data=evento.get('data'),
        evento_local=evento.get('local'),
        evento_horario=evento.get('horario'),
        evento_publico=evento.get('publico'),
        evento_imagem=evento.get('imagem'),
        evento_descricao=evento.get('descricao'),
        evento_cronograma=evento.get('cronograma'),
        evento_cirurgioes=evento.get('cirurgioes'),
        evento_palestrantes=evento.get('palestrantes'),
        evento_convidados=evento.get('convidados'),
        evento_localizacao=evento.get('localizacao')
    )
    # Ex: deploy/BariatricChannel/eventos/masterclass-sutura-robotica.html
    output_path = os.path.join(DEPLOY_DIR, 'eventos', f"{evento['id']}.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_html)
    print(f" -> {evento['id']}.html gerado.")


# -------
# 3. Gerar Página de Professores
# -------
print("Gerando página do corpo docente...")
professores_template = env.get_template('professores/corpo_docente.html')
prof_output_html = professores_template.render(
    professores=palestrantes_data
)
prof_output_path = os.path.join(DEPLOY_DIR, 'professores', 'corpo_docente.html')
with open(prof_output_path, 'w', encoding='utf-8') as f:
    f.write(prof_output_html)
print(" -> professores/corpo_docente.html gerado.")

# -------
# 3.5 SEO: descrição, prévia de compartilhamento, favicon e sitemap (data/seo.json)
# -------
import html as _html
import re as _re

print("Aplicando SEO...")
SEO_INI, SEO_FIM = '<!-- SEO:inicio', '<!-- SEO:fim -->'
with open(os.path.join(BASE_DIR, 'data', 'seo.json'), 'r', encoding='utf-8') as f:
    seo = json.load(f)
SITE = seo['site'].rstrip('/')
FAVICON = (
    '<link rel="icon" href="/favicon.ico" sizes="any">\n'
    '    <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">\n'
    '    <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">\n'
    '    <meta name="theme-color" content="#A51C24">'
)


def _aplicar_bloco(rel, bloco):
    caminho = os.path.join(DEPLOY_DIR, rel)
    if not os.path.exists(caminho):
        print(f" !! {rel} não existe, pulando SEO")
        return
    with open(caminho, 'r', encoding='utf-8', newline='') as f:
        txt = f.read()
    nl = '\r\n' if '\r\n' in txt else '\n'
    bloco = f'{SEO_INI} (gerado por build_site.py a partir de data/seo.json) -->\n    {bloco}\n    {SEO_FIM}'.replace('\n', nl)
    # tira bloco anterior (idempotente) e insere logo depois do </title>
    txt = _re.sub(r'[ \t]*' + _re.escape(SEO_INI) + r'.*?' + _re.escape(SEO_FIM) + r'\r?\n?', '', txt, flags=_re.S)
    txt = txt.replace('</title>', '</title>' + nl + '    ' + bloco, 1)
    with open(caminho, 'w', encoding='utf-8', newline='') as f:
        f.write(txt)


sitemap_urls = []
for rel, info in seo['paginas'].items():
    caminho = os.path.join(DEPLOY_DIR, rel)
    if not os.path.exists(caminho):
        print(f" !! {rel} não existe, pulando SEO")
        continue
    with open(caminho, 'r', encoding='utf-8') as f:
        m = _re.search(r'<title>(.*?)</title>', f.read(), _re.S)
    titulo = _html.unescape(m.group(1).strip()) if m else 'Bariatric Channel'
    url = SITE + info.get('url', '/' + rel)
    img = f"{SITE}/assets/og/{info.get('imagem', 'og-home.jpg')}"
    e = lambda s: _html.escape(s, quote=True)
    tags = [
        f'<meta name="description" content="{e(info["descricao"])}">',
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Bariatric Channel">',
        '<meta property="og:locale" content="pt_BR">',
        f'<meta property="og:title" content="{e(titulo)}">',
        f'<meta property="og:description" content="{e(info["descricao"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        FAVICON,
    ]
    _aplicar_bloco(rel, '\n    '.join(tags))
    if info.get('sitemap', True):
        sitemap_urls.append((url, info.get('prioridade', '0.5')))
for rel in seo.get('so_favicon', []):
    _aplicar_bloco(rel, FAVICON)

with open(os.path.join(DEPLOY_DIR, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url, prio in sitemap_urls:
        f.write(f'  <url><loc>{url}</loc><priority>{prio}</priority></url>\n')
    f.write('</urlset>\n')
print(f" -> SEO em {len(seo['paginas'])} páginas, sitemap.xml com {len(sitemap_urls)} URLs")

# -------
# 4. Sincronização com pasta Deploy Legada (opcional)
# -------
LEGACY_DEPLOY = os.path.join(BASE_DIR, 'deploy', 'BariatricChannel')
if os.path.exists(LEGACY_DEPLOY):
    print("\nSincronizando com pasta de deploy legada...")
    # Copia os arquivos principais gerados para a pasta legada
    files_to_sync = ['index.html', 'home.html', 'bc_amazon_week.html', 'checkin_bc.html', 'config_evento.html', 'bcflix.html']
    for f in files_to_sync:
        src = os.path.join(DEPLOY_DIR, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(LEGACY_DEPLOY, f))
            # Se for index.html, copia também para a raiz do BariatricChannel se necessário
            # mas o shutil.copy já está fazendo para a pasta destino.
    print(" -> Sincronização concluída.")

print("\nDeploy concluído em:", DEPLOY_DIR)
