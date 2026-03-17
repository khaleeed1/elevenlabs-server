import requests
import os
from flask import Flask, request, jsonify, send_file
import uuid

API_KEY = os.getenv("sk_03e7cd15467c5f0218f2b1f68a667ad4e58b0701c1617019")
API_URL = "https://api.elevenlabs.io/v1"

app = Flask(__name__)

@app.route("/")
def home():

    headers = {"xi-api-key": API_KEY}
    r = requests.get(f"{API_URL}/voices", headers=headers)

    voices = r.json()["voices"]

    options = ""
    for v in voices:
        options += f'<option value="{v["voice_id"]}">{v["name"]}</option>'

    return f"""
<html>
<body style="font-family:Arial;text-align:center;margin-top:40px">

<h2>ElevenLabs Voice Generator</h2>

<select id="voice" style="width:300px;height:40px">
{options}
</select>

<br><br>

<textarea id="text"
placeholder="Write text here"
style="width:300px;height:120px"></textarea>

<br><br>

<button onclick="generate()" style="width:200px;height:40px">
Generate Voice
</button>

<p id="status"></p>

<audio id="player" controls style="margin-top:20px;display:none"></audio>

<script>

async function generate() {{

document.getElementById("status").innerText = "Generating voice...";
document.getElementById("player").style.display = "none";

let voice = document.getElementById("voice").value
let text = document.getElementById("text").value

let res = await fetch("/voice", {{
method: "POST",
headers: {{ "Content-Type": "application/json" }},
body: JSON.stringify({{voice:voice,text:text}})
}})

if(res.status != 200) {{
let err = await res.text()
document.getElementById("status").innerText = "Error: " + err
return
}}

let blob = await res.blob()
let url = URL.createObjectURL(blob)

let player = document.getElementById("player")
player.src = url
player.style.display = "block"

document.getElementById("status").innerText = "Done"

}}

</script>

</body>
</html>
"""

@app.route("/voice", methods=["POST"])
def voice():

    data = request.json
    text = data.get("text")
    voice = data.get("voice")

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {"text": text}

    r = requests.post(
        f"{API_URL}/text-to-speech/{voice}",
        json=payload,
        headers=headers
    )

    if r.status_code != 200:
        return r.text, 400

    filename = f"{uuid.uuid4()}.mp3"

    with open(filename,"wb") as f:
        f.write(r.content)

    return send_file(filename, mimetype="audio/mpeg")
    <br><br>

    <textarea name="text"
    placeholder="Write text here"
    style="width:300px;height:120px"></textarea>

    <br><br>

    <button type="submit"
    style="width:200px;height:40px">
    Generate Voice
    </button>

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

    data = {
        "text": text
    }

    r = requests.post(
        f"{API_URL}/text-to-speech/{voice}",
        json=data,
        headers=headers
    )

    return Response(r.content, mimetype="audio/mpeg")
