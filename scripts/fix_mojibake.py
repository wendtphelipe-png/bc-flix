import os
import json

replacements = {
    # HTML missing bytes (replaced by  or removed)
    "Inovao": "Inovação",
    "Inovao": "Inovação",
    "Tcnica": "Técnica",
    "Tcnica": "Técnica",
    "Corao": "Coração",
    "Corao": "Coração",
    "BIPARTIO": "BIPARTIÇÃO",
    "BIPARTIO": "BIPARTIÇÃO",
    "TRNSITO": "TRÂNSITO",
    "TRNSITO": "TRÂNSITO",
    "Baritrica": "Bariátrica",
    "Baritrica": "Bariátrica",
    "BARITRICA": "BARIÁTRICA",
    "BARITRICA": "BARIÁTRICA",
    "Metablica": "Metabólica",
    "Metablica": "Metabólica",
    "METABLICA": "METABÓLICA",
    "METABLICA": "METABÓLICA",
    "Clnica": "Clínica",
    "Clnica": "Clínica",
    "robtica": "robótica",
    "robtica": "robótica",
    "laparoscpica": "laparoscópica",
    "laparoscpica": "laparoscópica",
    "hbrido": "híbrido",
    "hbrido": "híbrido",
    "imersǜo": "imersão",
    "imerso": "imersão",
    "explicaes": "explicações",
    "explicaes": "explicações",
    "Cirurgies": "Cirurgiões",
    "Cirurgies": "Cirurgiões",
    "Amaznia": "Amazônia",
    "Amaznia": "Amazônia",
    "FGADO": "FÍGADO",
    "FGADO": "FÍGADO",
    "VARIAES": "VARIAÇÕES",
    "VARIAES": "VARIAÇÕES",
    "Mdica": "Médica",
    "Mdica": "Médica",
    "Mdico": "Médico",
    "Mdico": "Médico",
    "Residncia": "Residência",
    "Residncia": "Residência",
    "Colgio": "Colégio",
    "Colgio": "Colégio",
    "Fundao": "Fundação",
    "Fundao": "Fundação",
    "Corra": "Corrêa",
    "Corra": "Corrêa",
    "So ": "São ",
    "So ": "São ",
    "Jos ": "José ",
    "Jos ": "José ",
    "Pas": "País",
    "Pas": "País",
    "currculo": "currículo",
    "currculo": "currículo",
    "atualizao": "atualização",
    "atualizao": "atualização",
    " s ": " às ",
    " s ": " às ",
    
    # JSON corrupted chars
    "Mǟ?DICO": "MÉDICO",
    "EMERGǟNCIA": "EMERGÊNCIA",
    "DIVISǟ'O": "DIVISÃO",
    "CLǟ?NICA": "CLÍNICA",
    "CIRǟRGICA": "CIRÚRGICA",
    "Sǟ'O": "SÃO",
    "COLǟ?GIO": "COLÉGIO",
    "CIRURGIǟ?ES": "CIRURGIÕES",
    "Mǟ?DICO": "MÉDICO",
    "EMERGǟNCIA": "EMERGÊNCIA",
    "DIVISǟ'O": "DIVISÃO",
    "CLǟ?NICA": "CLÍNICA",
    "CIRǟRGICA": "CIRÚRGICA",
    "Sǟ'O": "SÃO",
    "COLǟ?GIO": "COLÉGIO",
    "CIRURGIǟ?ES": "CIRURGIÕES",
    "Bariǭtrica": "Bariátrica",
    "Mini curr├¡culo": "Mini currículo",
    "Pa├¡s": "País",
    "Olvio": "Olívio",
    "Jaraguǭ": "Jaraguá",
    "Jaragu": "Jaraguá",
    "?\"": "-",
    "?\"": "-",
    "MǸdico": "Médico",
    "MǸdica": "Médica",
    "ResidǦncia": "Residência",
    "ColǸgio": "Colégio",
    "Associaǜo": "Associação",
    "Associaǜo": "Associação",
    "Captulo": "Capítulo",
    "Captulo": "Capítulo",
    "Robtica": "Robótica",
    "Robtica": "Robótica",
    "Cirurgies": "Cirurgiões",
    "Prximo": "Próximo",
    "Prximos": "Próximos",
    "Alem": "Além",
    "Alm": "Além",
    "Atravs": "Através",
    "atravs": "através",
    "voc": "você",
    "Voc": "Você",
    "Ns": "Nós",
    "ns": "nós",
    "Ao": "Ação",
    "ao": "ação",
    "Especializao": "Especialização",
    "especializao": "especialização",
    "Graduao": "Graduação",
    "graduao": "graduação",
    "Ps": "Pós",
    "ps": "pós",
    "Sade": "Saúde",
    "sade": "saúde",
    "Clnico": "Clínico",
    "clnico": "clínico",
    "Excelncia": "Excelência",
    "excelncia": "excelência",
    "Referncia": "Referência",
    "referncia": "referência",
    "Atrs": "Atrás",
    "atrs": "atrás",
    "Dvida": "Dúvida",
    "dvida": "dúvida",
    "Dvidas": "Dúvidas",
    "dvidas": "dúvidas"
}

files_to_fix = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.html') or f.endswith('.json'):
            files_to_fix.append(os.path.join(root, f))

for path in files_to_fix:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='windows-1252', errors='ignore') as file:
            content = file.read()
            
    original_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed {path}")
