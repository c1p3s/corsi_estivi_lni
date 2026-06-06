import os
import json

# BASE_DIR punta a: .../corsi_estivi_lni/backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PARENT_DIR punta a: .../corsi_estivi_lni (la cartella fuori da backend)
PARENT_DIR = os.path.dirname(BASE_DIR)

# Percorso per config.json (dentro backend)
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# Percorso per courses.json (fuori da backend, nella cartella principale)
COURSES_PATH = os.path.join(PARENT_DIR, "courses.json")

# 1. Carica la configurazione
try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
        config_host_key = config.get("host_key")
        config_password = config.get("password")
except FileNotFoundError as e:
    print(f"Errore: json_reader non trova config.json in: {CONFIG_PATH}")
    raise e

# 2. Carica i corsi (courses.json)
try:
    with open(COURSES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f) # Questo conterrà i corsi reali
except FileNotFoundError as e:
    print(f"Errore: json_reader non trova courses.json in: {COURSES_PATH}")
    raise e