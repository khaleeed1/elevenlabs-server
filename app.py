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

    voices = r.json()["voices"]

    options = ""

    for v in voices:
        options += f'<option value="{v["voice_id"]}">{v["name"]}</option>'

    return f"""
    <html>
    <body style="font-family:Arial;text-align:center;margin-top:40px">

    <h2>ElevenLabs Voice Generator</h2>

    <form action="/voice" method="post">

    <select name="voice" style="width:300px;height:40px">
    {options}
    </select>

    <br><br>

    <textarea name="text"
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

    data = {"text": text}

    r = requests.post(
        f"{API_URL}/text-to-speech/{voice}",
        json=data,
        headers=headers
    )

    return Response(r.content, mimetype="audio/mpeg")
body {{
font-family: Arial;
background:#f2f2f2;
text-align:center;
}}

.box {{
background:white;
width:360px;
margin:auto;
margin-top:40px;
padding:20px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,0.2);
}}

select,textarea,button {{
width:100%;
padding:10px;
margin-top:10px;
}}

button {{
background:#4CAF50;
color:white;
border:none;
}}

#status {{
margin-top:10px;
font-weight:bold;
}}

audio {{
margin-top:15px;
width:100%;
}}

</style>

</head>

<body>

<div class="box">

<h3>ElevenLabs Voice Generator</h3>

<select id="voice">
{options}
</select>

<textarea id="text" placeholder="Write text here"></textarea>

<button onclick="generate()">Generate Voice</button>

<div id="status"></div>

<audio id="player" controls style="display:none"></audio>

<a id="download" style="display:none">Download Audio</a>

</div>

<script>

async function generate(){{

let text=document.getElementById("text").value
let voice=document.getElementById("voice").value

document.getElementById("status").innerText="Generating..."

try{{

let res=await fetch("/voice",{{

method:"POST",
headers:{{"Content-Type":"application/json"}},
body:JSON.stringify({{text:text,voice:voice}})

}})

if(!res.ok){{

let err=await res.text()
document.getElementById("status").innerText="Error: "+err
return

}}

let blob=await res.blob()

let url=URL.createObjectURL(blob)

let player=document.getElementById("player")

player.src=url
player.style.display="block"

let dl=document.getElementById("download")

dl.href=url
dl.download="voice.mp3"
dl.innerText="Download"
dl.style.display="block"

document.getElementById("status").innerText="Done"

}}

catch(e){{

document.getElementById("status").innerText="Server error"

}}

}}

</script>

</body>

</html>
"""

@app.route("/voice", methods=["POST"])
def voice():

    if not API_KEY:
        return "API_KEY missing", 400

    data=request.json

    text=data.get("text")
    voice=data.get("voice")

    headers={
        "xi-api-key":API_KEY,
        "Content-Type":"application/json",
        "Accept":"audio/mpeg"
    }

    payload={"text":text}

    r=requests.post(
        f"{API_URL}/text-to-speech/{voice}",
        json=payload,
        headers=headers
    )

    if r.status_code!=200:
        return r.text,400

    return Response(r.content,mimetype="audio/mpeg")
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

body {{
font-family: Arial;
text-align:center;
background:#f2f2f2;
}}

.box {{
background:white;
width:350px;
margin:auto;
padding:20px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,0.2);
}}

select,textarea,button {{
width:100%;
margin-top:10px;
padding:10px;
font-size:14px;
}}

button {{
background:#4CAF50;
color:white;
border:none;
cursor:pointer;
}}

button:hover {{
background:#45a049;
}}

#status {{
margin-top:10px;
font-weight:bold;
}}

audio {{
margin-top:15px;
width:100%;
}}

</style>

</head>

<body>

<div class="box">

<h3>ElevenLabs Voice Generator</h3>

<select id="voice">
{options}
</select>

<textarea id="text" placeholder="Write text to convert"></textarea>

<button onclick="generate()">Generate Voice</button>

<div id="status"></div>

<audio id="player" controls style="display:none"></audio>

<br>

<a id="download" style="display:none">Download Audio</a>

</div>

<script>

async function generate(){{

let text = document.getElementById("text").value
let voice = document.getElementById("voice").value

document.getElementById("status").innerText="Generating..."
document.getElementById("player").style.display="none"
document.getElementById("download").style.display="none"

try{{

let res = await fetch("/voice",{{

method:"POST",
headers:{{"Content-Type":"application/json"}},
body:JSON.stringify({{text:text,voice:voice}})

}})

if(!res.ok){{

let err = await res.text()
document.getElementById("status").innerText="Error: "+err
return

}}

let blob = await res.blob()

let url = URL.createObjectURL(blob)

let player=document.getElementById("player")
player.src=url
player.style.display="block"

let dl=document.getElementById("download")
dl.href=url
dl.download="voice.mp3"
dl.innerText="Download Audio"
dl.style.display="block"

document.getElementById("status").innerText="Done"

}}

catch(e){{

document.getElementById("status").innerText="Server error"

}}

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

    payload = {
        "text": text
    }

    r = requests.post(
        f"{API_URL}/text-to-speech/{voice}",
        json=payload,
        headers=headers
    )

    if r.status_code != 200:
        return r.text, 400

    return Response(r.content, mimetype="audio/mpeg")
