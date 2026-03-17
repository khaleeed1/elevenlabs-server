import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

API_KEY = os.getenv("sk_03e7cd15467c5f0218f2b1f68a667ad4e58b0701c1617019")
API_URL = "https://api.elevenlabs.io/v1"

@app.route("/")
def home():

    headers = {"xi-api-key": API_KEY}

    r = requests.get(f"{API_URL}/voices", headers=headers)

    voices = r.json().get("voices", [])

    options = ""

    for v in voices:
        options += f'<option value="{v["voice_id"]}">{v["name"]}</option>'

    return f"""
<html>
<body>

<h2>ElevenLabs Voice Generator</h2>

<form action="/voice" method="post">

<select name="voice">
{options}
</select>

<br><br>

<textarea name="text" rows="5" cols="40"></textarea>

<br><br>

<button type="submit">Generate Voice</button>

</form>

</body>
</html>
"""

@app.route("/voice", methods=["POST"])
def voice():

    text = request.form.get("text")
    voice = request.form.get("voice")

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    data = {"text": text}

    r = requests.post(
        f"{API_URL}/text-to-speech/{voice}",
        json=data,
        headers=headers
    )

    return Response(r.content, mimetype="audio/mpeg")
