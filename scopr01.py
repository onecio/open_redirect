import requests
from urllib.parse import urlencode

# URL base do site a testar (ajuste conforme necessário)
base_url = "https://siteexemplo.gov.br/login"

# Parâmetro de redirecionamento (ajuste conforme a aplicação: ?redirect=, ?url=, ?next=, etc.)
param_name = "redirect"
test_redirect_url = "https://google.com"  # Ou algum domínio que você controla

# Montar a URL de teste
params = {param_name: test_redirect_url}
test_url = f"{base_url}?{urlencode(params)}"

# Fazer requisição (permitindo redirecionamento)
response = requests.get(test_url, allow_redirects=True)

# Verificar resultado
if response.url.startswith(test_redirect_url):
    print("[VULNERÁVEL] Redirecionamento externo permitido!")
else:
    print("[SEGURO] Sem redirecionamento externo.")
print("URL final:", response.url)

'''
#Requisitos
#Python 3

Instalar a biblioteca requests:
#pip install requests

O que esse script faz:
Monta uma URL de teste com redirecionamento para um domínio externo.
Envia uma requisição HTTP e segue os redirecionamentos.
Verifica se a URL final é externa (ex: https://google.com).
Informa se há potencial vulnerabilidade.
'''
