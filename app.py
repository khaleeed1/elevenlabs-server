import requests
import os
import base64
from flask import Flask, request, render_template_string

API_KEY = os.environ.get("sk_03e7cd15467c5f0218f2b1f68a667ad4e58b0701c1617019")
API_URL = "https://api.elevenlabs.io/v1"

if not API_KEY:
    raise Exception("API_KEY not found in environment variables")

app = Flask(__name__)

history = []

HTML = """
<html>
<head>
<title>ElevenLabs Voice Generator</title>

<style>
body{font-family:Arial;background:#f2f2f2;text-align:center}
.box{background:white;padding:25px;border-radius:10px;width:420px;margin:auto;margin-top:40px}
textarea{width:100%;height:120px}
select,input{width:100%;height:35px;margin-top:8px}
button{background:#28a745;color:white;border:none;height:40px;width:100%;margin-top:12px;font-size:16px}
audio{margin-top:15px;width:100%}
.history{text-align:left;margin-top:25px}
</style>

</head>

<body>

<div class="box">

<h2>ElevenLabs Voice Generator</h2>

<form method="post" action="/generate">

<select name="voice">
{% for v in voices %}
<option value="{{v.voice_id}}">{{v.name}}</option>
{% endfor %}
</select>

<label>Speed</label>
<input type="range" name="speed" min="0.7" max="1.3" step="0.05" value="1">

<label>Quality</label>
<select name="model">
<option value="eleven_multilingual_v2">High Quality</option>
<option value="eleven_turbo_v2">Fast</option>
</select>

<textarea name="text" placeholder="Write text here"></textarea>

<button type="submit">Generate Voice</button>

</form>

{% if audio %}

<h3>Generated Voice</h3>

<audio controls autoplay>
<source src="data:audio/mpeg;base64,{{audio}}" type="audio/mpeg">
</audio>

<br><br>

<a download="voice.mp3" href="data:audio/mpeg;base64,{{audio}}">
<button>Download</button>
</a>

{% endif %}

{% if error %}
<h3 style="color:red">{{error}}</h3>
{% endif %}

<div class="history">

<h3>History</h3>

<ul>
{% for h in history %}
<li>{{h}}</li>
{% endfor %}
</ul>

</div>

</div>

</body>
</html>
"""

@app.route("/")
def home():

    headers = {"xi-api-key": API_KEY}

    r = requests.get(f"{API_URL}/voices", headers=headers)

    voices = r.json().get("voices", [])

    return render_template_string(
        HTML,
        voices=voices,
        audio=None,
        history=history,
        error=None
    )


@app.route("/generate", methods=["POST"])
def generate():

    text = request.form.get("text")
    voice = request.form.get("voice")
    model = request.form.get("model")
    speed = float(request.form.get("speed"))

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7,
            "style": speed
        }
    }

    r = requests.post(
        f"{API_URL}/text-to-speech/{voice}",
        headers=headers,
        json=data
    )

    if r.status_code != 200:

        headers = {"xi-api-key": API_KEY}
        voices = requests.get(f"{API_URL}/voices", headers=headers).json().get("voices", [])

        return render_template_string(
            HTML,
            voices=voices,
            audio=None,
            history=history,
            error=r.text
        )

    audio = base64.b64encode(r.content).decode("utf-8")

    history.insert(0, text[:80])

    headers = {"xi-api-key": API_KEY}
    voices = requests.get(f"{API_URL}/voices", headers=headers).json().get("voices", [])

    return render_template_string(
        HTML,
        voices=voices,
        audio=audio,
        history=history,
        error=None
    )

app.run(host="0.0.0.0", port=10000){% for v in voices %}
<option value="{{v.voice_id}}">{{v.name}}</option>
{% endfor %}
</select>

<label>Speed</label>
<input type="range" name="speed" min="0.7" max="1.3" step="0.05" value="1">

<label>Quality</label>
<select name="model">
<option value="eleven_multilingual_v2">High Quality</option>
<option value="eleven_turbo_v2">Fast</option>
</select>

<textarea name="text" placeholder="Write text here"></textarea>

<button type="submit">Generate Voice</button>

</form>

{% if audio %}

<h3>Generated Voice</h3>

<audio controls autoplay>
<source src="data:audio/mpeg;base64,{{audio}}">
</audio>

<br><br>

<a download="voice.mp3" href="data:audio/mpeg;base64,{{audio}}">
<button>Download</button>
</a>

{% endif %}

{% if error %}
<h3 style="color:red">{{error}}</h3>
{% endif %}

<div class="history">

<h3>History</h3>

<ul>
{% for h in history %}
<li>{{h}}</li>
{% endfor %}

</ul>

</div>

</div>

</body>
</html>
"""

@app.route("/")
def home():

    headers = {"xi-api-key": API_KEY}

    r = requests.get(f"{API_URL}/voices", headers=headers)

    voices = r.json().get("voices", [])

    return render_template_string(HTML, voices=voices, audio=None, history=history, error=None)


@app.route("/generate", methods=["POST"])
def generate():

    text = request.form.get("text")
    voice = request.form.get("voice")
    model = request.form.get("model")
    speed = float(request.form.get("speed"))

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": model,
        "voice_settings":{
            "stability":0.5,
            "similarity_boost":0.7,
            "style":speed
        }
    }

    r = requests.post(
        f"{API_URL}/text-to-speech/{voice}",
        headers=headers,
        json=data
    )

    if r.status_code != 200:

        headers = {"xi-api-key": API_KEY}
        voices = requests.get(f"{API_URL}/voices", headers=headers).json().get("voices", [])

        return render_template_string(
            HTML,
            voices=voices,
            audio=None,
            history=history,
            error=r.text
        )

    audio = base64.b64encode(r.content).decode("utf-8")

    history.insert(0, text[:80])

    headers = {"xi-api-key": API_KEY}
    voices = requests.get(f"{API_URL}/voices", headers=headers).json().get("voices", [])

    return render_template_string(
        HTML,
        voices=voices,
        audio=audio,
        history=history,
        error=None
    )

app.run(host="0.0.0.0", port=10000)
