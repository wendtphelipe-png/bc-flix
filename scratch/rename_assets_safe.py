import os
import shutil

ASSETS_DIR = r'g:\Outros computadores\Meu laptop\Web Projects\BC Web\assets'

def make_safe(filename):
    # Dicionário de renomeação manual para garantir exatidão
    rename_map = {
        'Manoel passos galv': 'manoel_galvao',
        'Andre Weiss': 'andre_weiss',
        'Maurilio Ribeiro Junior': 'maurilio_junior',
        'Ana Carolina Martins': 'ana_carolina',
        'Carlos Tanizawa': 'carlos_tanizawa',
        'Guilherme Goyano': 'guilherme_goyano',
        'Mariana Calanca': 'mariana_calanca',
        'Naiara Portugal': 'naiara_portugal',
        'Reinaldo Morioka': 'reinaldo_morioka',
        'Rodrigo Fernandes': 'rodrigo_fernandes',
        'Rafael Abaid': 'rafael_abaid',
        'Joe Waltrick': 'joe_waltrick',
        'Patrick Noel': 'patrick_noel'
    }
    
    for key, safe in rename_map.items():
        if key.lower() in filename.lower():
            ext = os.path.splitext(filename)[1].lower()
            return safe + ext
    return None

def rename_assets():
    for filename in os.listdir(ASSETS_DIR):
        safe_name = make_safe(filename)
        if safe_name and safe_name != filename:
            src = os.path.join(ASSETS_DIR, filename)
            dst = os.path.join(ASSETS_DIR, safe_name)
            try:
                shutil.move(src, dst)
                print(f"Renomeado: {filename} -> {safe_name}")
            except Exception as e:
                print(f"Erro ao renomear {filename}: {e}")

if __name__ == "__main__":
    rename_assets()
