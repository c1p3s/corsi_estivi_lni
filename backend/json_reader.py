import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Costruisce il percorso assoluto per config.json nella stessa cartella
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
        config_host_key = config.get("host_key")
        config_password = config.get("password")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f) 
    
except FileNotFoundError as e:
    print(f"Errore: json_reader non trova il file in: {CONFIG_PATH}")
    raise e