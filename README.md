# open_redirect
Solução para testar e monitorar vulnerabilidade Open Redirectic nos sites

Para testar se um site está suscetível a open redirect (redirecionamento aberto) — uma vulnerabilidade em que um atacante pode redirecionar usuários para sites maliciosos usando URLs do próprio site legítimo — você pode seguir os seguintes passos de forma segura e controlada:

1. Identifique um ponto de redirecionamento
Busque por parâmetros como:

?redirect=

?url=

?next=

?return=

?continue=

Exemplo:

bash
Copiar
Editar
https://siteexemplo.gov.br/login?redirect=https://externo.com
2. Teste com um URL externo
Substitua o valor do parâmetro por um site sob seu controle (ou um conhecido confiável), como:

bash
Copiar
Editar
https://siteexemplo.gov.br/login?redirect=https://google.com
Se o site redirecionar diretamente para https://google.com, isso indica uma vulnerabilidade.

3. Teste com payloads de verificação
Use variações para testar filtros ou validações:

//evil.com

/\evil.com

https:@evil.com

%2f%2fevil.com (encoded)

Exemplos:

perl
Copiar
Editar
https://siteexemplo.gov.br/login?redirect=//evil.com
https://siteexemplo.gov.br/login?next=%2F%2Fevil.com
Se qualquer um desses levar ao redirecionamento, o site está vulnerável.

4. Ferramentas automáticas (opcional)
Você pode usar ferramentas como:

Burp Suite (com extensão "Open Redirect Scanner")

OWASP ZAP

5. Regras para testes éticos
Teste apenas com permissão.

Não utilize links maliciosos reais.

Não explore ou abuse da vulnerabilidade.

Correções comuns (para devs)
Validar e restringir URLs de redirecionamento a domínios específicos.

Usar uma lista branca de URLs permitidas.

Evitar redirecionamentos baseados em parâmetros de usuário sempre que possível.

O teste de open redirect, quando feito corretamente, não afeta permanentemente o site. Ele é um teste não destrutivo. Veja o que acontece:

O que ocorre durante o teste
Você monta uma URL com um parâmetro de redirecionamento (ex: ?redirect=https://google.com).

Ao acessar essa URL, o servidor apenas executa o redirecionamento indicado naquele momento.

O comportamento só acontece durante aquela requisição específica.

Nenhum dado é alterado no site (como banco de dados ou arquivos).

Após o teste
O site continua funcionando normalmente.

Nenhum redirecionamento permanente é criado.

Não há persistência dessa URL — ou seja, a vulnerabilidade está lá, mas só é "ativada" quando a URL maliciosa é usada.

Exceções (raras)
O único risco seria se:

Você testasse em um ambiente de produção com coleta de logs muito restritiva e ativasse um bloqueio automático.

Houvesse um sistema automatizado de defesa que banisse IPs suspeitos.

Resumo
Não, o site não fica redirecionado permanentemente. Ele continua funcionando normalmente após o teste. A vulnerabilidade existe, mas é explorada dinamicamente quando a URL malformada é usada.

Abaixo está um script simples em Python que testa se uma URL é suscetível a open redirect usando a biblioteca requests. Ele verifica se o redirecionamento ocorre para um domínio externo controlado por você (ou, no exemplo, https://google.com):

Script: Teste de Open Redirect
python
Copiar
Editar
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
Requisitos
Python 3

Instalar a biblioteca requests:

pip install requests
O que esse script faz:
Monta uma URL de teste com redirecionamento para um domínio externo.

Envia uma requisição HTTP e segue os redirecionamentos.

Verifica se a URL final é externa (ex: https://google.com).

Informa se há potencial vulnerabilidade.

Aqui está uma versão expandida do script para testar vários parâmetros comuns de redirecionamento e com suporte a proxy (caso queira anonimizar ou registrar via Burp/ZAP):

Script: Teste Avançado de Open Redirect
python
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
Como usar
Substitua base_url pela URL da aplicação que você quer testar.

Marque use_proxy = True se quiser usar proxy (Burp/ZAP).

Execute com:
python open_redirect_tester.py
Possíveis melhorias
Testar também payloads encoding (%2f%2fmalicioso.com, //malicioso.com etc.)

Salvar resultados em arquivo

Testar POST, se aplicável

Aqui está a versão completa e aprimorada do script de teste de Open Redirect, incluindo:

Teste de vários parâmetros comuns.

Teste com payloads evasivos (encoding, esquemas oblíquos, etc.).

Suporte a proxy (Burp/ZAP).

Saída detalhada e clara.

Script Final – Open Redirect Tester com Payloads Evasivos
python
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
Como usar
Instale requests se ainda não tiver:
pip install requests
Substitua base_url pela URL que você quer testar.

Rode o script com:
python open_redirect_tester.py
(Opcional) Ative o proxy com use_proxy = True para capturar no Burp/ZAP.

Aqui está a versão profissional do script como uma ferramenta de linha de comando (CLI) em Python, com suporte a:

Argumentos via argparse

Exportação para .csv

Proxy opcional

Teste de múltiplos parâmetros e payloads

Script: open_redirect_scanner.py
python
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
Como usar
Salve como open_redirect_scanner.py.

Execute com:
python open_redirect_scanner.py https://site.gov.br/login
Opções úteis
--params redirect url next          # Testa parâmetros específicos
--proxy                             # Usa proxy localhost:8080 (Burp/ZAP)
--csv resultado.csv                 # Salva resultado em CSV
Exemplo completo
bash
Copiar
Editar
python open_redirect_scanner.py https://site.gov.br/login --proxy --csv open_redirect_result.csv
Vamos criar uma interface web leve com Flask para o scanner de Open Redirect. Isso permite:
Executar os testes via navegador.
Visualizar os resultados na hora.
Baixar os resultados em CSV.
Passo 1: Instale as dependências
No terminal:
pip install flask requests
Passo 2: Código da aplicação Flask (app.py)
python
from flask import Flask, request, render_template, send_file
import requests
from urllib.parse import urlencode
import csv
import io

app = Flask(__name__)

PAYLOADS = [
    "https://google.com", "//google.com", "http://google.com", "/\\google.com",
    "https:@google.com", "%2F%2Fgoogle.com", "///google.com", "https://www.google.com%2F%2E%2E"
]

DEFAULT_PARAMS = ["redirect", "url", "next", "return", "continue", "dest", "destination"]

def test_redirect(base_url, param, payload, proxies=None):
    try:
        params = {param: payload}
        test_url = f"{base_url}?{urlencode(params)}"
        response = requests.get(test_url, allow_redirects=True, proxies=proxies, timeout=10)
        final_url = response.url
        status = "VULNERÁVEL" if payload.strip('/').replace("%2F", "/").replace("%2E", ".") in final_url else "SEGURO"
        return [test_url, param, payload, final_url, status]
    except Exception as e:
        return [test_url, param, payload, "ERRO", str(e)]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        base_url = request.form["url"]
        use_proxy = "proxy" in request.form
        selected_params = request.form.getlist("params")
        proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"} if use_proxy else None

        for param in selected_params:
            for payload in PAYLOADS:
                result = test_redirect(base_url, param, payload, proxies)
                results.append(result)
        request.session = results
    return render_template("index.html", results=results, params=DEFAULT_PARAMS)

@app.route("/download")
def download_csv():
    results = request.session if hasattr(request, 'session') else []
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Tested URL", "Parameter", "Payload", "Final URL", "Status"])
    writer.writerows(results)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv",
                     as_attachment=True, download_name="open_redirect_results.csv")

if __name__ == "__main__":
    app.run(debug=True)
Passo 3: Template HTML (templates/index.html)
Crie um diretório templates/ e dentro dele, um arquivo index.html:

html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Open Redirect Scanner</title>
</head>
<body>
  <h1>Open Redirect Scanner</h1>
  <form method="post">
    <label>URL base:</label><br>
    <input type="text" name="url" size="60" required><br><br>

    <label>Parâmetros para testar:</label><br>
    {% for param in params %}
      <input type="checkbox" name="params" value="{{ param }}" checked> {{ param }}
    {% endfor %}<br><br>

    <label><input type="checkbox" name="proxy"> Usar proxy (127.0.0.1:8080)</label><br><br>

    <button type="submit">Iniciar Teste</button>
  </form>

  {% if results %}
    <h2>Resultados:</h2>
    <table border="1" cellpadding="5">
      <tr><th>URL Testada</th><th>Parâmetro</th><th>Payload</th><th>URL Final</th><th>Status</th></tr>
      {% for row in results %}
        <tr>
          {% for item in row %}
            <td>{{ item }}</td>
          {% endfor %}
        </tr>
      {% endfor %}
    </table>
    <br>
    <a href="/download">Baixar CSV</a>
  {% endif %}
</body>
</html>
Passo 4: Rodar a aplicação
No terminal:

bash
Copiar
Editar
python app.py
Abra o navegador em http://127.0.0.1:5000 e teste!

Aqui estão duas opções para empacotar a aplicação Flask do scanner de Open Redirect:

Opção 1 – Gerar EXE com PyInstaller (Windows/Linux)
1. Instale o PyInstaller
pip install pyinstaller
2. Estrutura de diretórios
markdown
Copiar
Editar
open_redirect_scanner/
├── app.py
└── templates/
    └── index.html
3. Empacote
No terminal, dentro da pasta do projeto:
pyinstaller --noconfirm --onefile --add-data "templates:templates" app.py
Importante: No Windows use ; e no Linux/Mac use : no --add-data.

Exemplo para Windows:
pyinstaller --noconfirm --onefile --add-data "templates;templates" app.py
4. Resultado
Será gerado um executável em dist/app.exe (ou dist/app no Linux), que você pode rodar direto com:
./dist/app
Opção 2 – Rodar em qualquer sistema com Docker
1. Crie um Dockerfile
Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask requests
EXPOSE 5000
CMD ["python", "app.py"]
2. Construa a imagem
docker build -t open-redirect-scanner .
3. Rode o container
docker run -p 5000:5000 open-redirect-scanner
Abra no navegador:
arduino
http://localhost:5000
Para te entregar um pacote completo com:

Executável .exe (Windows)

Código-fonte com Flask

Template HTML

Dockerfile pronto

Script .bat para Windows e .sh para Linux/macOS

Versão compactada .zip

Você está usando Windows, Linux ou outro sistema? (para empacotar corretamente o .exe)
Quer que o pacote seja enviado como um link para download ou apenas o conteúdo para você montar localmente?
Deseja ícone personalizado ou nome específico para o EXE/app?
Com essas informações, em seguida eu:
Gero os arquivos,
Empacoto em .zip (ou .tar.gz),
E envio para você fazer o download.
Só confirmar esses 3 pontos e envio tudo pronto.

Como coletar logse  bloquar automaticamente, considerado recursos do servidor, firewall FTD cisco 4115 e F5 BIG-IP, quais os tipos de open redirect, tipo injeção HTML, dom, já e outros e como corrigir as vulnerabilidades dos sites e como corrigir sites já comprometidos e como comprometer um site


1. Coleta de Logs e Bloqueio Automático
Infraestrutura mencionada:
Cisco FTD 4115 (Firepower Threat Defense)

F5 BIG-IP (geralmente como WAF, Load Balancer ou ADC)

Passos recomendados:
a) Cisco FTD 4115
Ative Syslog ou Secure Syslog (TLS) para enviar logs ao seu SIEM (ex: Splunk, QRadar, ELK).

Use Correlation Policies no FMC (Firepower Management Center) para automatizar ações como:

Block IP

Reset Connection

Alert

Configure Eventing para Intrusion Policies com assinatura de HTTP Redirect Exploit.

b) F5 BIG-IP
Ative Application Security Manager (ASM) como WAF.

Habilite:

Automatic Policy Builder

Violation Logging

Integre com iRules para bloquear redirecionamentos não autorizados (ex: Location headers externos).

Envie logs para SIEM via HSL ou Syslog-ng.

Use o Bot Defense e IP Intelligence para bloquear bots maliciosos.

c) Automatização
Use SOAR (ex: Splunk SOAR ou TheHive + Cortex) para orquestrar:

Análise do log.

Regras de IOC (ex: IPs maliciosos).

Comando via API REST do FTD ou F5 para bloquear ou ajustar políticas.

2. Tipos de Open Redirect
Tipo	Descrição
Basic (Query)	?redirect=https://malicioso.com
DOM-based	Manipulado via JavaScript no navegador: location.href = getParam()
Injeção HTML	Uso de atributos como <meta http-equiv="refresh" content="0;url=...">
Injeção HTTP	Modificação do cabeçalho Location: em respostas HTTP
Open Redirect + XSS	Quando é possível injetar JavaScript em URLs redirecionadas

3. Correção de vulnerabilidades
a) Prevenção
Valide e sanitize todos os parâmetros de redirecionamento.

Permita apenas redirecionamentos para domínios autorizados (whitelist).

Para redirecionamentos externos, use uma página intermediária com aviso:

"Você está saindo do site..." com botão para continuar.

Use CSP (Content Security Policy) para prevenir execução de código malicioso.

b) Correção de sites já comprometidos
Isolar o servidor (modo manutenção).

Verificar arquivos alterados (ex: index.php, config.js).

Comparar com backup limpo.

Remover redirecionamentos ocultos (em .htaccess, meta tags ou JS).

Atualizar CMS/plugins/frameworks.

Revalidar regras no WAF e antivírus web.

4. Sobre “como comprometer um site”
Essa parte não pode ser abordada por questões éticas e legais. Qualquer uso ofensivo deve ser realizado apenas com autorização expressa, dentro de testes de intrusão autorizados (pentests).

Se o seu objetivo for aprender segurança ofensiva de forma ética, posso te auxiliar com:

Ambientes de teste como:

Hack The Box

TryHackMe

OWASP Juice Shop, DVWA, WebGoat

Cursos e certificações:

CompTIA Security+

Offensive Security OSCP

CEH (Certified Ethical Hacker)

Deseja que eu monte um guia prático com ferramentas (SIEM, WAF, SOAR), regex e scripts para bloquear open redirects em FTD/F5? Posso incluir playbooks para resposta a incidentes.






