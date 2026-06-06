from flask import Blueprint, request, abort 
import subprocess
import os
import json

webhook_bp = Blueprint("webhook_bp", __name__)

@webhook_bp.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        script_path = '/home/lorehh/update.sh'
        
        if os.path.exists(script_path):
            # Esegue lo script in background
            subprocess.Popen(['/bin/bash', script_path])
            return 'Aggiornamento avviato!', 200
        else:
            return 'Script non trovato', 404
    else:
        abort(400)