from flask import Blueprint, request, jsonify, abort
import requests
import re
from backend.json_reader import config_google_script_url, config_google_sheets_secret

invia_bp = Blueprint("invia_bp", __name__)

GOOGLE_SCRIPT_URL = config_google_script_url

SECRET_KEY = config_google_sheets_secret

ALLOWED_FIELDS = {
    "nome",
    "cognome",
    "cf",
    "data_nascita",
    "luogo_nascita",
    "indirizzo",
    "comune_residenza",
    "cap",
    "corso",
    "settimana",
    "email",
    "telefono",
    "nome_genitore",
    "cognome_genitore",
    "data_nascita_genitore",
    "comune_nascita_genitore",
    "cf_genitore",
    "indirizzo_genitore",
    "comune_residenza_genitore",
    "cap_genitore",
    "telefono_genitore",
    "email_genitore",
    "tipo_doc",
    "num_doc",
    "luogo_rilascio_doc",
    "data_rilascio_doc",
    "note"
}

MAX_LENGTH_DEFAULT = 40
MAX_LENGTH_NOTES = 40


def sanitize(value):
    if value is None:
        return ""

    value = str(value)
    value = re.sub(r'[\x00-\x1F\x7F\uFEFF\u200B\u200C\u200D\u2060\u180E\u200E\u200F]+', '', value)
    value = value.strip()

    if value and value[0] in ("=", "+", "-", "@"):
        raise ValueError("Valore non valido: inizio con carattere non consentito")

    return value


def invalid_json(message):
    return jsonify({"success": False, "message": message}), 400


@invia_bp.route("/api/invio", methods=["POST"])
def invia():
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        return invalid_json("Corpo della richiesta non valido JSON")

    cleaned = {}
    for key, value in data.items():
        if key not in ALLOWED_FIELDS:
            continue

        try:
            value = sanitize(value)
        except ValueError as exc:
            return invalid_json(str(exc))

        max_len = MAX_LENGTH_NOTES if key == "note" else MAX_LENGTH_DEFAULT

        if len(value) > max_len:
            return invalid_json(f"Campo '{key}' troppo lungo")

        cleaned[key] = value

    cleaned["secret"] = SECRET_KEY

    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=cleaned,
            timeout=15
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        abort(502, description=f"Errore invio Google Sheets: {exc}")

    return jsonify({
        "success": True,
        "message": "Dati inviati correttamente"
    })
