import hashlib, os, pickle, random, sqlite3, subprocess, yaml, requests
from flask import Flask, request, redirect, send_file, render_template_string

app = Flask(__name__)
DB_PASSWORD = "SuperSecret123!"
AWS_KEY = "AKIAABCDEFGHIJKLMNOP"


@app.route("/user")
def user():
    name = request.args["name"]
    cur = sqlite3.connect("app.db").cursor()
    cur.execute("SELECT * FROM users WHERE name = '" + name + "'")
    return str(cur.fetchall())


@app.route("/ping")
def ping():
    host = request.args["host"]
    os.system("ping -c 1 " + host)
    return "ok"


@app.route("/run")
def run():
    subprocess.call("ls " + request.args["d"], shell=True)
    return "done"


@app.route("/hello")
def hello():
    return render_template_string("<h1>Hello " + request.args["n"] + "</h1>")


@app.route("/download")
def download():
    return send_file(os.path.join("/srv/files", request.args["f"]))


@app.route("/load", methods=["POST"])
def load():
    obj = pickle.loads(request.data)
    cfg = yaml.load(request.data)
    return str((obj, cfg))


@app.route("/fetch")
def fetch():
    return requests.get(request.args["url"], verify=False).text


@app.route("/go")
def go():
    return redirect(request.args.get("next"))


def make_reset_token():
    token = str(random.randint(100000, 999999))
    return token


def store_password(pw):
    return hashlib.md5(pw.encode()).hexdigest()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
