from flask import Flask, request, Response
import base64
import json
import uuid
import subprocess
from script import is_scripted, stt
from flask import jsonify
app = Flask(__name__)


"""
{
    "voice": "base64string",
    "words": [["добрый вечер", "здравствуйте"], ["пакет"]]
}
"""
@app.route("/", methods=('POST', 'GET'))
def hello():
    if request.method == 'GET':
        return "OK!"
    else:
        assert request.is_json
        voice = request.json['voice'].encode()
        voice = base64.b64decode(voice)  
        words = request.json['words']
        voice_fname = convert(voice)
        for i in range(len(words)):
            words[i] = tuple(words[i])
        text = stt(voice_fname)
        if not text:
            data = {'text': "<NO TEXT>", 'quality': 0, 'not_found': []}
        elif not words:
            data = {'text': text, 'quality': 1, 'not_found': []}
        else:
            not_found = is_scripted(text, words)
            data = {'text': text, 'quality': 1 - len(not_found) / len(words), 
                    'not_found': [nf_t[0] for nf_t in not_found]}
        return Response(json.dumps(data), mimetype='application/json; charset=utf-8')
    

def convert(binary_voice):
    voice_id = uuid.uuid4()
    fname = "/tmp/{}.m4a".format(voice_id)
    result_fname = "/tmp/{}.mp3".format(voice_id)
    with open(fname, "wb") as f:
        f.write(binary_voice)
    subprocess.run("ffmpeg -i {} {}".format(fname, result_fname), shell=True, check=True)
    return result_fname
