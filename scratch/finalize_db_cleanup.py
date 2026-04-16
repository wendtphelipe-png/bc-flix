import json
import unicodedata

JSON_PATH = r'g:\Outros computadores\Meu laptop\Web Projects\BC Web\data\palestrantes_raw.json'

def fix_mojibake(text):
    if not isinstance(text, str):
        return text
    try:
        # Tenta corrigir erro comum onde UTF-8 é lido como Latin-1
        # Ã³ -> ó, Ã¡ -> á, etc.
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

def norm(s):
    if not s: return ""
    return "".join(c for c in unicodedata.normalize('NFD', s.upper()) if unicodedata.category(c) != 'Mn')

def update_db():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Mapeamento Seguro (Slug -> Caminho Asset)
    asset_mapping = {
        'MANOEL GALVAO': 'assets/manoel_galvao.jpg',
        'MANOEL PASSOS GALVAO NETO': 'assets/manoel_galvao.jpg',
        'ANDRE WEISS': 'assets/andre_weiss.jpg',
        'MAURILIO RIBEIRO JUNIOR': 'assets/maurilio_junior.jpg',
        'ANA CAROLINA MARTINS': 'assets/ana_carolina.jpeg',
        'CARLOS TANIZAWA': 'assets/carlos_tanizawa.jpg',
        'GUILHERME GOYANO': 'assets/guilherme_goyano.jpg',
        'MARIANA CALANCA': 'assets/mariana_calanca.jpg',
        'NAIARA PORTUGAL': 'assets/naiara_portugal.jpeg',
        'REINALDO MORIOKA': 'assets/reinaldo_morioka.png',
        'RODRIGO FERNANDES': 'assets/rodrigo_fernamdes.png',
        'RAFAEL ABAID': 'assets/rafael_abaid.jpeg',
        'JOE WALTRICK': 'assets/joe_waltrick.jpg',
        'PATRICK NOEL': 'assets/patrick_noel.jpg'
    }

    for speaker in data:
        # 1. Fix Mojibake
        speaker['Nome'] = fix_mojibake(speaker.get('Nome', ''))
        if 'Mini currículo' in speaker:
            speaker['Mini currículo'] = fix_mojibake(speaker['Mini currículo'])
        
        # 2. Update Foto URL by matching
        sn = norm(speaker['Nome'])
        for key, path in asset_mapping.items():
            if key == sn or (key in sn and len(key) > 8):
                speaker['Foto URL'] = path
                print(f"Updated: {speaker['Nome']} -> {path}")
                break

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("Banco de dados atualizado com sucesso.")


if __name__ == "__main__":
    update_db()
