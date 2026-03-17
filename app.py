import requests
from flask import Flask, request, Response

API_KEY = "sk_03e7cd15467c5f0218f2b1f68a667ad4e58b0701c1617019"

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():

    text = request.json.get("text")
    voice = request.json.get("voice")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    data = {
        "text": text
    }

    r = requests.post(url, json=data, headers=headers)

    return Response(r.content, mimetype="audio/mpeg")

app.run(host="0.0.0.0", port=10000)
