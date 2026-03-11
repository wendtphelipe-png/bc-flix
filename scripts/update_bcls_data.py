import json
import re

# Lista extraída do texto do site
cirurgioes_names = ["Carlos Domene", "Carlos Madalosso", "Diogo Kfouri", "Guilherme Goyano", "Hiroji Okano", "Nicholas Kruel"]
palestrantes_names = ["Admar Concon", "André Teixeira", "Antelmo Sasso", "Carlos Dillemburg", "Carlos Madalosso", "Daiane Weber", "Diogo Kfouri", "Eduardo Grecco", "Hiroji Okano", "Hugo Santos", "Joe Waltrick", "Jéssica Zandoná", "Luiz Gustavo Quadros", "Manoel Galvão Neto", "Milton Kawahara", "Márcia Murussi", "Paulo Reis", "Persio Stobbe", "Raquel Fraga", "Renato Souza", "Victor Dib"]

# Convidados principais (uma amostra, mas vamos ler o que der match)
convidados_names = ["Alonso Alvarado", "Aluísio Stoll", "André Bigolin", "Angelo Muniz", "Antelmo Sasso", "Antônio Torres", "Bruno Filippi Ricciardi", "Caio Aquino", "Carlos Dillemburg", "Carlos Domene", "Crislei Casamali", "Diogo Kfouri", "Elias Gianni", "Enrique Luque de Leon", "Eudes Godoy", "Felipe Koleski", "Felippe Camarotto", "Felix Santos", "Fernando Fornari", "Fernando Manso", "Francisco Diaz", "Gabriel Vargas", "Geisson Beck Hahn", "Glauco Alvarez", "Guilherme Goyano", "Henrique W. de Albuquerque", "Igor Wolwacz Jr", "Jarbas Cavalheiro", "Joe Waltrick", "Juarez Antonio Dal Vesco", "Kali Fontana", "Katia Souto", "Lucas Rossi", "Lucas Schmitt", "Lucian El-Kadre", "Luciano Santos", "Luiz Alberto De Carli", "Luiz Poggi", "Luís Fernando Martinez Pereira", "Mariana Calanca", "Mariano Menezes", "Maurice Formighieri", "Mauricio Ramos", "Maurilio Ribeiro Jr", "Márcia Murussi", "Paula Volpe", "Rafael Rothbarth", "Ricardo L Zanin", "Rodolfo Oviedo", "Rui Ribeiro", "Victor Dib"]

with open('debug_scrape.json', 'r', encoding='utf-8') as f:
    scraped = json.load(f)

# Criar map simplificado string -> URL
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

image_map = {}
for item in scraped:
    if item['src']:
        url = item['src']
        # Remover o blur e aumentar a resolução das fotos do Wix
        url = re.sub(r'blur_\d+,?', '', url)
        url = re.sub(r'w_\d+,h_\d+', 'w_400,h_400', url)
        
        nome_url = url.split('/')[-1].lower()
        nome_url = nome_url.replace('%20', ' ').replace('_', ' ').replace('edited', '').replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
        nome_url = re.sub(r'[^a-záéíóúãõç ]', ' ', nome_url).strip()
        nome_url = remove_accents(nome_url)
        
        image_map[nome_url] = url

def find_image(name):
    name_clean = remove_accents(name.lower())
    parts = name_clean.split()
    
    # Tentativa 1: Correspondência exata
    for key, url in image_map.items():
        if name_clean in key or key in name_clean:
            return url
            
    # Tentativa 2: Primeiro + Último nome
    if len(parts) > 1:
        first_last = parts[0] + " " + parts[-1]
        for key, url in image_map.items():
            if parts[0] in key and parts[-1] in key:
                return url
                
    # Tentativa 3: Só o primeiro nome (se for um nome muito específico, mas arriscado)
    for key, url in image_map.items():
        if parts[0] in key and len(parts[0]) > 3:
            return url

    return "https://api.dicebear.com/7.x/initials/svg?seed=" + name.replace(" ", "") + "&backgroundColor=B22222"

def build_person_list(names):
    res = []
    for n in names:
        res.append({
            "nome": n,
            "foto": find_image(n)
        })
    # Remove duplicatas por nome
    seen = set()
    final = []
    for x in res:
        if x['nome'] not in seen:
            seen.add(x['nome'])
            final.append(x)
    return final

cirurgioes = build_person_list(cirurgioes_names)
palestrantes = build_person_list(palestrantes_names)
convidados = build_person_list(convidados_names)

# Carregar e atualizar database.json
with open('data/database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Atualizar o evento
for evento in db['eventos']:
    if evento['id'] == 'ix-bc-live-surgery':
        evento['cirurgioes'] = cirurgioes
        evento['palestrantes'] = palestrantes
        evento['convidados'] = convidados
        evento['localizacao'] = [
            {
                "dia": "Dia 1 - 27/02",
                "titulo": "Hospital de Clínicas de Passo Fundo",
                "endereco": "Rua Uruguai, 590, Centro - Passo Fundo, RS",
                "horario": "8h às 18h",
                "link_maps": "https://www.google.com/maps/place/R.+Uruguai,+590+-+Centro,+Passo+Fundo+-+RS,+99010-110/@-28.2563142,-52.4083686,17z/"
            },
            {
                "dia": "Dia 2 - 28/02",
                "titulo": "Auditório Carlos Madalosso",
                "endereco": "Rua Uruguai 1953, 9º andar - Passo Fundo, RS",
                "horario": "8h às 12h30",
                "link_maps": "https://www.google.com/maps/place/R.+Uruguai,+1953+-+9%C2%BA+andar+-+Centro,+Passo+Fundo+-+RS,+99010-111/@-28.2619889,-52.4185818,17z/"
            }
        ]

with open('data/database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Database updated with people and maps!")
