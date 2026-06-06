#!/bin/bash

# 1. Definiamo i percorsi per sicurezza
PROJECT_DIR="/home/lnimateramagnagrecia/corsi_estivi_lni/backend"
VENV_PATH="/home/lnimateramagnagrecia/corsi_estivi_lni/backend/venv"
WSGI_FILE="/var/www/lnimateramagnagrecia_pythonanywhere_com_wsgi.py"

echo "--- Inizio aggiornamento LNI Server ---"

# 2. Entriamo nella cartella del progetto
cd $PROJECT_DIR || { echo "Errore: cartella non trovata"; exit 1; }

# 3. Scarichiamo le ultime modifiche da GitHub
echo "Recupero aggiornamenti da GitHub..."
git pull origin main

# 4. Attiviamo la virtualenv e aggiorniamo i pacchetti
echo "Aggiornamento dipendenze (requirements.txt)..."
source $VENV_PATH/bin/activate
pip install --upgrade pip  # Opzionale: tiene aggiornato pip stesso
pip install -r requirements.txt

# 5. Riavviamo il server toccando il file WSGI
echo "Riavvio del server..."
touch $WSGI_FILE

echo "--- LNI Server è aggiornato e online! ---"