import json
import unicodedata

JSON_PATH = r'data/palestrantes_raw.json'

def norm(s):
    if not s: return ""
    # Remove acentos e converte para maiúsculas
    s = "".join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.upper()

def update_photos():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Nomes simplificados que o usuário usa vs arquivos de assets
    targets = {
        'MANOEL GALVAO': 'assets/Manoel passos galvão neto.jpg',
        'ANDRE WEISS': 'assets/Andre Weiss.jpg',
        'MAURILIO RIBEIRO JUNIOR': 'assets/Maurilio Ribeiro Junior.jpg'
    }

    updated_count = 0
    for speaker in data:
        name_raw = speaker.get('Nome', '')
        name_clean = norm(name_raw)
        
        for search_name, photo_path in targets.items():
            # Dividir o nome de busca em partes (ex: "MANOEL", "GALVAO")
            parts = search_name.split()
            # Verifica se todas as partes do nome de busca estão presentes no nome do JSON (após normalização)
            if all(part in name_clean for part in parts):
                speaker['Foto URL'] = photo_path
                updated_count += 1
                print(f"Match found: {name_raw} -> {photo_path}")
                break
    
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Total: {updated_count} registros atualizados.")

if __name__ == "__main__":
    update_photos()
