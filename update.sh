#!/bin/bash

# 1. Definiamo i percorsi per sicurezza
PROJECT_DIR="/home/lnimateramagnagrecia/corsi_estivi_lni/backend"
VENV_PATH="/home/lnimateramagnagrecia/corsi_estivi_lni/backend/venv"
WSGI_FILE="/var/www/lnimateramagnagrecia_pythonanywhere_com_wsgi.py"
ROOT_DIR="/home/lnimateramagnagrecia/corsi_estivi_lni"

echo "--- Inizio aggiornamento LNI Server ---"

# 2. Entriamo nella cartella del progetto
cd $PROJECT_DIR || { echo "Errore: cartella non trovata"; exit 1; }

# 3. Scarichiamo le ultime modifiche da GitHub
echo "Recupero aggiornamenti da GitHub..."
git pull origin main

# 4. Attiviamo la virtualenv e aggiorniamo i pacchetti
echo "Aggiornamento dipendenze (requirements.txt)..."
if [ -f "$VENV_PATH/bin/activate" ]; then
    source $VENV_PATH/bin/activate
    pip install --upgrade pip
    
    # Controlla dove si trova il file requirements.txt
    if [ -f "$ROOT_DIR/requirements.txt" ]; then
        pip install -r "$ROOT_DIR/requirements.txt"
    elif [ -f "$PROJECT_DIR/requirements.txt" ]; then
        pip install -r "$PROJECT_DIR/requirements.txt"
    else
        echo "Avviso: requirements.txt non trovato!"
    fi
else
    echo "Errore: Ambiente virtuale non trovato in $VENV_PATH. Creo un nuovo venv..."
    python3 -m venv $VENV_PATH
    source $VENV_PATH/bin/activate
    pip install --upgrade pip
    [ -f "$ROOT_DIR/requirements.txt" ] && pip install -r "$ROOT_DIR/requirements.txt"
fi

# 5. Riavviamo il server toccando il file WSGI
echo "Riavvio del server..."
touch $WSGI_FILE

echo "--- LNI Server è aggiornato e online! ---"