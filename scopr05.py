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
