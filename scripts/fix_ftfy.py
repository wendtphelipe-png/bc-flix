import os
import ftfy

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except UnicodeDecodeError:
        print(f"Skipping {filepath} due to decoding error.")
        return

    fixed_content = ftfy.fix_text(original_content)
    
    if fixed_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"Fixed mojibake in: {filepath}")

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or 'deploy' in root:
        continue
    for f in files:
        if f.endswith('.html') or f.endswith('.json'):
            process_file(os.path.join(root, f))
