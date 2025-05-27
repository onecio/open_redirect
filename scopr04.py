import requests
import argparse
import csv
from urllib.parse import urlencode

# Payloads evasivos comuns
PAYLOADS = [
    "https://google.com",
    "//google.com",
    "http://google.com",
    "/\\google.com",
    "https:@google.com",
    "%2F%2Fgoogle.com",
    "///google.com",
    "https://www.google.com%2F%2E%2E"
]

# Parâmetros padrão de redirecionamento
DEFAULT_PARAMS = ["redirect", "url", "next", "return", "continue", "dest", "destination"]

def test_redirect(base_url, param, payload, proxies):
    params = {param: payload}
    test_url = f"{base_url}?{urlencode(params)}"

    try:
        response = requests.get(test_url, allow_redirects=True, proxies=proxies, timeout=10)
        final_url = response.url
        is_vulnerable = payload.strip('/').replace("%2F", "/").replace("%2E", ".") in final_url
        return (test_url, param, payload, final_url, "VULNERÁVEL" if is_vulnerable else "SEGURO")
    except requests.RequestException as e:
        return (test_url, param, payload, "ERRO", str(e))

def main():
    parser = argparse.ArgumentParser(description="Scanner de Open Redirect")
    parser.add_argument("url", help="URL base para testar (ex: https://site.com/login)")
    parser.add_argument("--params", nargs="+", help="Parâmetros de redirecionamento a testar", default=DEFAULT_PARAMS)
    parser.add_argument("--proxy", action="store_true", help="Usar proxy localhost:8080 (Burp/ZAP)")
    parser.add_argument("--csv", help="Arquivo de saída CSV com os resultados")
    args = parser.parse_args()

    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    } if args.proxy else None

    print(f"\nIniciando testes em: {args.url}\n")

    results = []
    for param in args.params:
        for payload in PAYLOADS:
            result = test_redirect(args.url, param, payload, proxies)
            results.append(result)
            status = result[4]
            print(f"[{status}] {param} → {payload}")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Tested URL", "Parameter", "Payload", "Final URL", "Status"])
            writer.writerows(results)
        print(f"\n[+] Resultados salvos em: {args.csv}")

if __name__ == "__main__":
    main()


'''
#Como usar
Salve como open_redirect_scanner.py.

Execute com:
#python open_redirect_scanner.py https://site.gov.br/login
Opções úteis
--params redirect url next          # Testa parâmetros específicos
--proxy                             # Usa proxy localhost:8080 (Burp/ZAP)
--csv resultado.csv                 # Salva resultado em CSV

Exemplo completo
#python open_redirect_scanner.py https://site.gov.br/login --proxy --csv open_redirect_result.csv
'''