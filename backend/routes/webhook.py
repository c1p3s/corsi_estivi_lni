from flask import Blueprint, request, abort
import subprocess
import os
from backend.json_reader import config_password 
webhook_bp = Blueprint("webhook_bp", __name__)

@webhook_bp.route('/update', methods=['POST'])
def update():
    auth = request.headers.get("X-UPDATE-KEY")
    if auth != config_password:
        return "Unauthorized", 401

    script_path = '/home/lnimateramagnagrecia/corsi_estivi_lni/update.sh'

    if os.path.exists(script_path):
        subprocess.Popen(['/bin/bash', script_path])
        return 'Aggiornamento avviato!', 200

    else:
        return 'Script non trovato', 404