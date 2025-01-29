import json
import uuid

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Swish API-konfiguration
SWISH_URL = "https://mss.cpc.getswish.net/swish-cpcapi/api/v1/paymentrequests"
CERT_PATH = "/api/mss/v1"
CERT_KEY_PATH = "path_to_client_key.key"
SWISH_NUMBER = "1231271816"  # Ditt Swish-nummer
CALLBACK_URL = "https://your-server.com/callback"


@app.route("/create_payment", methods=["POST"])
def create_payment():
    data = request.json
    amount = data.get("amount", "100")  # Standardvärde 100 SEK
    currency = "SEK"

    payment_request = {
        "payeeAlias": SWISH_NUMBER,
        "amount": amount,
        "currency": currency,
        "message": "Resa med ResRobot",
        "callbackUrl": CALLBACK_URL,
        "payeePaymentReference": str(uuid.uuid4())[:10],
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            SWISH_URL,
            data=json.dumps(payment_request),
            headers=headers,
            cert=(CERT_PATH, CERT_KEY_PATH),
        )
        response_data = response.json()
        return jsonify(response_data), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
