from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_cors import CORS
from flask_sock import Sock
import os 
import json
from routes.auth import auth_bp
from routes.webhook import webhook_bp
from json_reader import config_host_key, data, COURSES_PATH

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
sock = Sock(app)

CORS(app, resources={r"/api/*"})
app.register_blueprint(auth_bp)
app.register_blueprint(webhook_bp)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # assicurati che sia False per HTTP
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # oppure 'None' se stai usando domini tipo .ts.net
app.secret_key = config_host_key

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/orari', methods=['POST', 'GET'])
def orari():
    return render_template('orari.html', corsi=data)

@app.route('/iscrizione', methods=['POST', 'GET'])
def iscrizione():
    with open(COURSES_PATH, "r", encoding="utf-8") as f:
        corsi = json.load(f)
    return render_template('iscrizione.html', corsi = corsi)

@app.route('/carpediem', methods=['POST', 'GET'])
def carpediem():
    return render_template('carpediem.html')

@app.route('/console', methods=['POST', 'GET'])
def console():
    if not session.get('logged_in'):
        return redirect(url_for('carpediem'))
    
    from json_reader import COURSES_PATH
    import json
    with open(COURSES_PATH, "r", encoding="utf-8") as f:
        corsi = json.load(f)
        
    return render_template('console.html', corsi = corsi)


@app.route("/api/update-available", methods=["POST"])

def update_available():
    try:
        payload = request.get_json()
        corso = payload["corso"]
        index = int(payload["index"])
        available = bool(payload["available"])
        with open(COURSES_PATH, "r", encoding="utf-8") as f:
            corsi = json.load(f)

        corsi[corso]["turni"][index]["available"] = available
        with open(COURSES_PATH, "w", encoding="utf-8") as f:
            json.dump(corsi, f, indent=2, ensure_ascii=False)

        return jsonify({
            "status": "ok",
            "corso": corso,
            "index": index,
            "available": available
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5200))
    app.run(host="localhost", port=port)
    
    