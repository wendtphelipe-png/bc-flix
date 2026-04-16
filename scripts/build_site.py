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
    'unnamed.png': 'apoio_institucional_v2.png'
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
    
    # Consertar a URL das imagens que ficaram no servidor .com.br invés do .com principal
    if p.get('Foto URL'):
        p['Foto URL'] = p['Foto URL'].replace('bariatricchannel.com/event/', 'bariatricchannel.com.br/event/')

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

output_index = index_template.render(
    evento_destaque=evento_destaque
)

with open(os.path.join(DEPLOY_DIR, 'home.html'), 'w', encoding='utf-8') as f:
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

print("\nDeploy concluído em:", DEPLOY_DIR)
