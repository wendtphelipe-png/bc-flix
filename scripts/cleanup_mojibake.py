import os
import re

def cleanup_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return

    original_content = content

    # Common replacements for the "ó" mojibake
    replacements = {
        'const': 'const',
        'JetBrains': 'JetBrains',
        'https': 'https',
        'Sans': 'Sans',
        'sections': 'sections',
        'institucional': 'institucional',
        'atualização': 'atualização',
        'currículo': 'currículo',
        'currículo': 'currículo',
        'atualização': 'atualização',
        'const': 'const',
        'Sans': 'Sans',
        'https': 'https',
        'JetBrains': 'JetBrains',
        'sections': 'sections',
        'atualização': 'atualização'
    }

    for target, replacement in replacements.items():
        content = content.replace(target, replacement)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {file_path}")

def walk_and_cleanup(directory):
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith(('.html', '.json', '.js', '.py', '.css')):
                cleanup_file(os.path.join(root, file))

if __name__ == "__main__":
    project_root = r"g:\Outros computadores\Meu laptop\Web Projects\BC Web"
    walk_and_cleanup(project_root)
    print("Cleanup complete.")
