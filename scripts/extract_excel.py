import pandas as pd
import json
import math

# Caminho do arquivo
excel_file = r"c:\Users\WMcirurgia\Desktop\BC Web\Bariatric Channel - Palestrantes (foto, nome, currículo).xlsx"

# Lendo a planilha (forçando para converter para string, substituindo NaNs)
try:
    df = pd.read_excel(excel_file)
    df = df.fillna("")
    
    palestrantes = []
    
    # Mapeando os nomes das colunas de forma genérica caso sejam diferentes (ex: Nome, Currículo, Nacionalidade, Foto)
    # Assumindo a primeira linha como header ou vamos investigar as colunas primeiro
    print("Colunas encontradas:", list(df.columns))
    
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        palestrantes.append(row_dict)
        
    # Salvando temporariamente para análise
    with open(r"c:\Users\WMcirurgia\Desktop\BC Web\data\palestrantes_raw.json", "w", encoding="utf-8") as f:
        json.dump(palestrantes, f, ensure_ascii=False, indent=4)
        
    print(f"Extraídos {len(palestrantes)} palestrantes.")

except Exception as e:
    print(f"Erro ao processar o Excel: {e}")
