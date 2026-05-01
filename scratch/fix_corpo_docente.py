import os
import re

path = r"g:\Outros computadores\Meu laptop\Web Projects\BC Web\professores\corpo_docente.html"

with open(path, 'rb') as f:
    content = f.read()

# Replace corrupted patterns in bytes
# currculo -> currículo
# atualizaǜo -> atualização

# Since we don't know the exact bytes of the corruption, we'll search for the surrounding text.
# document.getElementById('modal-curriculo').innerText = p['Mini curr...'] || p['Mini curr...'] || 'Curr... detalhado em processo de atualiza...';

pattern = rb"document\.getElementById\('modal-curriculo'\)\.innerText = p\['Mini curr.*?\] \|\| p\['Mini curr.*?\] \|\| 'Curr.*? detalhado em processo de atualiza.*?';"
replacement = rb"document.getElementById('modal-curriculo').innerText = p['Mini curr\xedculo'] || p['Mini curr\xedculo'] || 'Curr\xedculo detalhado em processo de atualiza\xe7\xe3o.';"

new_content = re.sub(pattern, replacement, content)

if new_content != content:
    with open(path, 'wb') as f:
        f.write(new_content)
    print("Fixed.")
else:
    print("Not found.")
