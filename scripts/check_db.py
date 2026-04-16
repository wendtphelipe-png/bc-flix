import urllib.request, json

SUPABASE_URL = 'https://jlygyfsaupdknvwljvql.supabase.co/rest/v1/eventos_bc'
API_KEY = 'sb_publishable_A-Gxbkir7foDZgZvaOuiHw_pMVXXdEV'

# Dummy data from Corpo Docente (Amazon Week context)
payload = {
    "titulo": "2º BC Amazon Week (Demonstração)",
    "imagem": "https://bariatricchannel.com/assets/on%C3%A7a%20low.jpg",
    "palestrantes": [
        {"nome": "Alex Escalona", "pais": "Chile", "foto": ""},
        {"nome": "Sérgio Verboonen", "pais": "Mexico", "foto": ""},
        {"nome": "Patrick Noel", "pais": "France", "foto": ""},
        {"nome": "Ricardo Zorron", "pais": "Germany", "foto": ""},
        {"nome": "Júlio Teixeira", "pais": "USA", "foto": ""},
        {"nome": "Paulo Reis", "pais": "Brazil", "foto": ""}
    ]
}

req = urllib.request.Request(SUPABASE_URL, data=json.dumps(payload).encode('utf-8'), headers={
    'apikey': API_KEY,
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
})

try:
    resp = urllib.request.urlopen(req)
    print("Database populated:", resp.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())
