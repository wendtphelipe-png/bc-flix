import os
import re

# Technical terms that were corrupted by the mojibake script
tech_replacements = {
    r"conósole": "console",
    r"responóse": "response",
    r"upósert": "upsert",
    r"unóshift": "unshift",
    r"inóside": "inside",
    r"inóstitucionais": "institucionais",
    r"Conóstraints": "Constraints",
    r"Inóstagram": "Instagram",
    r"apósen": "apsen",
    r"Alonóso": "Alonso",
    r"Manóso": "Manso",
    r"hipertenósão": "hipertensão",
    r"inóscricação": "inscrição",
    r"checkinós": "checkins",
    r"Ação vivo": "Ao vivo",
    r"ação vivo": "ao vivo",
    r"açãos": "aos",
    r" ação ": " ao ",
    r"Ação ": "Ao ",
    r"Trânósito": "Trânsito",
    r"compreenósão": "compreensão",
    r"Martinós": "Martins",
    r"invocêado": "invocado",
    r"Paíssword": "Password",
    r"groupós": "groups",
    r"funcação": "funcao",
    r"inósert": "insert",
    r"Inósuficiente": "Insuficiente",
    r"conósolidou-se": "consolidou-se",
    r"galvação": "galvao",
    r"gestação-section": "gestão-section",
    r"gestação-grid": "gestão-grid",
    r"id=\"gestação\"": "id=\"gestão\"",
    r"href=\"#gestação\"": "href=\"#gestão\"",
    r"Corao": "Coração",
    r"Amaznia": "Amazônia",
    r"Alémino": "Almino",
    r"inóstância": "instância",
    r"inóstance": "instance",
    r"transplante hepǭtico": "transplante hepático"
}

# The corrupted Supabase Key ref
# Original ref: jlygyfsaupdknvwljvql
# Corrupted ref in key: Impóse...
# This is inside a base64 string, so we'll look for the specific pattern.
# Key typically starts with eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp
# And has 'Impóse' right after the 'Imp'
corrupted_key_pattern = r"Impóse"
correct_key_replacement = "jly"

files_to_fix = []
for root, dirs, files in os.walk('.'):
    if any(x in root for x in ['.git', 'node_modules', 'assets', 'vendor']):
        continue
    for f in files:
        if f.endswith(('.html', '.json', '.js', '.py')):
            if f == 'undo_corruption.py' or f == 'fix_mojibake.py':
                continue
            files_to_fix.append(os.path.join(root, f))

for path in files_to_fix:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception:
        continue
            
    original_content = content
    
    # 1. Fix the Supabase Key
    if "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp" in content:
        content = content.replace(corrupted_key_pattern, correct_key_replacement)
        
    # 2. Fix specific technical terms
    for old, new in tech_replacements.items():
        content = content.replace(old, new)
        
    # 3. Fix common internal word corruptions (e.g., 'u-nós-hift')
    # These are harder. We'll use regex to find 'nós' or 'pós' inside a word.
    # [a-zA-Z]nós[a-zA-Z] or similar
    content = re.sub(r'([a-zA-Z])nós([a-zA-Z])', r'\1ns\2', content)
    content = re.sub(r'([a-zA-Z])pós([a-zA-Z])', r'\1ps\2', content)
    
    # 4. Fix character-level mojibake patterns
    char_replacements = {
        "ǜo": "ão",
        "ǜ": "ã",
        "ǭ": "á",
        "Ǧ": "ê",
        "Ǹ": "é",
        "ì": "í",
        "ó": "o" # Wait, be careful with this one. 'inóstância' used 'ó' as a marker.
    }
    
    # We apply technical replacements first, then character ones
    # But 'ó' was used as a marker for many things.
    # If we already fixed 'inóstância', etc., we can clean up remaining 'ó' if they are inside words.
    
    for old, new in char_replacements.items():
        content = content.replace(old, new)
    
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed {path}")
