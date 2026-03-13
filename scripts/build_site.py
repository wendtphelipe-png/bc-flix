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

# Copia logo animado se existir
logo_src = os.path.join(BASE_DIR, 'Logo_branco.mp4')
if os.path.exists(logo_src):
    shutil.copy(logo_src, os.path.join(DEPLOY_DIR, 'assets', 'Logo_branco.mp4'))

# Carrega os dados principais
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Carrega a nova base de palestrantes
PALESTRANTES_FILE = os.path.join(BASE_DIR, 'data', 'palestrantes_raw.json')
with open(PALESTRANTES_FILE, 'r', encoding='utf-8') as f:
    palestrantes_data = json.load(f)

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
print(" -> professores/index.html gerado.")

print("\nDeploy concluído em:", DEPLOY_DIR)
