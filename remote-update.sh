#!/bin/bash

SECRET=$(python3 -c "import json; print(json.load(open('backend/config.json'))['password'])")

URL="https://lnimateramagnagrecia.pythonanywhere.com/update"

response=$(curl -s -w "\nHTTP_CODE:%{http_code}" \
  -X POST \
  -H "X-UPDATE-KEY: $SECRET" \
  "$URL")

echo "$response"