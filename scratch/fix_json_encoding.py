import json
import os

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

def clean_json():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for speaker in data:
        # Limpar Nome e Mini currículo
        if 'Nome' in speaker:
            speaker['Nome'] = fix_mojibake(speaker['Nome'])
        if 'Mini currículo' in speaker:
            speaker['Mini currículo'] = fix_mojibake(speaker['Mini currículo'])
        
        # Aproveitar para garantir que o nome de Ana Carolina Martins e outros estão corretos
        if speaker.get('Nome') == 'Ana carolina Martins':
            speaker['Nome'] = 'Ana Carolina Martins'
        if speaker.get('Nome') == 'Tiago Ferreira Paula':
             speaker['Nome'] = 'Tiago Ferreira'

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("JSON limpo de Mojibake com sucesso.")

if __name__ == "__main__":
    clean_json()
