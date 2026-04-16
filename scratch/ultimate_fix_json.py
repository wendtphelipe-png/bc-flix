import json
import os
import unicodedata

JSON_PATH = r'data/palestrantes_raw.json'
ASSETS_DIR = r'assets'

def norm(s):
    if not s: return ""
    return "".join(c for c in unicodedata.normalize('NFD', s.upper()) if unicodedata.category(c) != 'Mn')

def fix_all():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Dicionário de Correção por ID (Mais Seguro)
    overrides = {
        '66a706d2e4c9a688fbd0aca7': 'assets/manoel_galvao.jpg',
        'custom_weiss': 'assets/andre_weiss.jpg',
        'custom_ribeiro': 'assets/maurilio_junior.jpg',
        '66a11b0aa75874b7234a452a': 'assets/ana_carolina.jpeg',
        'custom_fernandes': 'assets/rodrigo_fernandes.png'
    }

    # Dicionário de Mapas de Nomes
    name_map = {
        'MANOEL GALVAO': 'assets/manoel_galvao.jpg',
        'ANDRE WEISS': 'assets/andre_weiss.jpg',
        'MAURILIO RIBEIRO': 'assets/maurilio_junior.jpg',
        'MAURILIO JUNIOR': 'assets/maurilio_junior.jpg',
        'ANA CAROLINA MARTINS': 'assets/ana_carolina.jpeg',
        'RODRIGO FERNANDES': 'assets/rodrigo_fernandes.png'
    }

    for speaker in data:
        # 1. Normalizar as chaves do dicionário (remover possíveis caracteres fantasmas)
        cleaned_speaker = {}
        for k, v in speaker.items():
            # Limpar chave de caracteres estranhos (mojibake)
            k_clean = k.encode('ascii', 'ignore').decode('ascii').strip()
            if 'Foto URL' in k or 'FotoURL' in k:
                k_clean = 'Foto URL'
            cleaned_speaker[k_clean] = v
        
        # 2. Aplicar Overrides por ID
        sid = cleaned_speaker.get('ID')
        if sid in overrides:
            cleaned_speaker['Foto URL'] = overrides[sid]
        
        # 3. Aplicar por Nome se ainda não tiver foto ou se for um dos alvos
        sn = norm(cleaned_speaker.get('Nome', ''))
        for target_name, path in name_map.items():
            if target_name in sn:
                cleaned_speaker['Foto URL'] = path
        
        # Atualizar no objeto original
        speaker.clear()
        speaker.update(cleaned_speaker)

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("Correção de JSON concluída (IDs e Slugs).")

if __name__ == "__main__":
    fix_all()
