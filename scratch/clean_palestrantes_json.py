import json
import os

# Caminho dos arquivos
JSON_PATH = r'g:\Outros computadores\Meu laptop\Web Projects\BC Web\data\palestrantes_raw.json'
ASSETS_DIR = r'assets/'

# Mapeamento de Correção de Nomes e Fotos novas
corrections = {
    "VICTOR RAMOS MUSSA DIB": {"Nome": "Victor Dib"},
    "CARLOS EDUARDO DOMENE": {"Nome": "Carlos Domene"},
    "ALMINO CARDOSO RAMOS": {"Nome": "Almino Ramos"},
    "ELINTON ADAMI CHAIM": {"Nome": "Elinton Chaim"},
    "JORGE BRAVO LOPEZ": {"Nome": "Jorge Bravo"},
    "AMADOR GARCIA RUIZ DE GORDEJUELA": {"Nome": "Amador Garcia"},
    "HALIT EREN TASKIN": {"Nome": "Eren Taskin"},
    "MANOEL PASSOS GALVÃO NETO": {"Nome": "Manoel Galvão", "Foto URL": "assets/Manoel passos galvão neto.jpg"},
    "ANTELMO SASSO FIN": {"Nome": "Antelmo Sasso"},
    "DIOGO SWAIN KFOURI": {"Nome": "Diogo Kfouri"},
    "Felix Antonio Insaurriaga dos Santos": {"Nome": "Felix Santos"},
    "HIROJI OKANO JUNIOR": {"Nome": "Hiroji Okano"},
    "IBRAHIM MASSUQUETO ANDRADE GOMES DE SOUZA": {"Nome": "Ibrahim Massuqueto"},
    "Joe JoaquimWaltrick": {"Nome": "Joe Waltrick", "Foto URL": "assets/Joe Waltrick.jpg"},
    "Rafel Abaid": {"Nome": "Rafael Abaid", "Foto URL": "assets/Rafael Abaid.jpeg"},
    "ANA CAROLINA CALDEIRA CARVALHO FERNANDES": {"Nome": "Ana Carolina Martins", "Foto URL": "assets/Ana Carolina Martins.webp"},
    # Outros com fotos novas
    "ANDRÉ WEISS": {"Foto URL": "assets/Andre Weiss.jpg"},
    "CARLOS TANIZAWA": {"Foto URL": "assets/Carlos Tanizawa.jpg"},
    "GUILHERME GOYANO": {"Foto URL": "assets/Guilherme Goyano.jpg"},
    "MARIANA CALANCA": {"Foto URL": "assets/Mariana Calanca.jpg"},
    "MAURÍLIO RIBEIRO JUNIOR": {"Foto URL": "assets/Maurilio Ribeiro Junior.jpg"},
    "NAIARA PORTUGAL": {"Foto URL": "assets/Naiara Portugal.jpeg"},
    "PATRICK NOEL": {"Foto URL": "assets/Patrick Noel.jpg"},
    "REINALDO MORIOKA": {"Foto URL": "assets/Reinaldo Morioka..png"},
    "RODRIGO FERNANDES": {"Foto URL": "assets/Rodrigo Fernandes.png"}
}

def clean_json():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    for speaker in data:
        name = speaker.get('Nome', '')
        
        # Procurar na lista de correção
        found = False
        for original, mods in corrections.items():
            if original.upper() == name.upper():
                found = True
                for key, val in mods.items():
                    speaker[key] = val
                updated_count += 1
                break
        
        # Se não achou por nome exato, tentar normalizar para checar
        if not found:
            # Caso especial para nomes que possam estar quebrados mas são o que queremos
            pass

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"JSON atualizado com sucesso. {updated_count} registros modificados.")

if __name__ == "__main__":
    clean_json()
