from flask import Blueprint, request, redirect, url_for, render_template, session
import json

auth_bp = Blueprint("auth_bp", __name__)
with open("./backend/config.json") as f:
    config = json.load(f)
    config_password = config.get("password")


        
@auth_bp.route('/auth', methods=['POST'])
def auth():
    text_input = request.form['password']

    if text_input == config_password: 
        session['logged_in'] = True
        return redirect(url_for('console'))
    else:
        error = "La password è errata, riprova"
        return render_template('carpediem.html', error=error)

@auth_bp.route('/logout', methods=['POST', 'GET']) 
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))