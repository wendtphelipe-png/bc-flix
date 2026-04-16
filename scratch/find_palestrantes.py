import json
# import jellyfish # Not available, will use basic matching

def find_speaker(names_list, data_path):
    with open(data_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    results = {}
    for search_name in names_list:
        matches = []
        search_lower = search_name.lower()
        for entry in data:
            entry_name = entry.get('Nome', '').lower()
            if search_lower in entry_name:
                matches.append(entry)
        results[search_name] = matches
    return results

names = [
    "VICTOR", "MADALOSSO", "PAULO REIS", "PATRICK NOEL",
    "DOMENE", "ANTONIO TORRES", "ALMINO",
    "RUI RIBEIRO", "ELINTON", "JORGE BRAVO", "AMADOR GARCIA", "GRECCO", "EREN TASKIN", "GALVÃO",
    "ANA CAROLINA", "WEISS", "ANTELMO", "DILLEMBURG", "TANIZAWA", "KFOURI", "FELIX", "GIORGIO BARETTA", "GOYANO", "OKANO",
    "MASSUQUETO", "WALTRICK", "CALANCA", "Maurílio", "NAIARA", "NICHOLAS", "ABAID", "RODRIGO FERNANDES", "MORIOKA"
]

results = find_speaker(names, r'g:\Outros computadores\Meu laptop\Web Projects\BC Web\data\palestrantes_raw.json')

for name, found in results.items():
    if found:
        print(f"MATCH [{name}]: {len(found)} results")
        for f in found:
            print(f"  -> {f['Nome']} (País: {f.get('País', '??')}) ID: {f['ID']}")
    else:
        print(f"MISSING [{name}]")
