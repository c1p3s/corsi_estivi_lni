from flask import Flask, render_template, session, redirect, url_for
from flask_cors import CORS
from flask_sock import Sock
import os 
import json
from routes.auth import auth_bp


app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
sock = Sock(app)
with open("config.json") as f:
    config = json.load(f)
    config_host_key = config.get("host_key")
    config_password = config.get("password")


CORS(app, resources={r"/api/*"})
app.register_blueprint(auth_bp)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # assicurati che sia False per HTTP
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # oppure 'None' se stai usando domini tipo .ts.net
app.secret_key = config_host_key

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/orari', methods=['POST', 'GET'])
def orari():
    with open("courses.json", "r", encoding="utf-8") as f:
        corsi = json.load(f)
    return render_template('orari.html', corsi=corsi)

@app.route('/iscrizione', methods=['POST', 'GET'])
def iscrizione():
    with open("courses.json", "r", encoding="utf-8") as f:
        corsi = json.load(f)
    return render_template('iscrizione.html', corsi = corsi)

@app.route('/carpediem', methods=['POST', 'GET'])
def carpediem():
    return render_template('carpediem.html')

@app.route('/console', methods=['POST', 'GET'])
def console():
    if not session.get('logged_in'):
        return redirect(url_for('carpediem'))
    return render_template('console.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5200))
    app.run(host="localhost", port=port)