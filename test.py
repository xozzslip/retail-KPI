
import base64
import json
import requests


if __name__ == "__main__":
    with open("voice3/audio_2018-10-27_19-06-17.ogg", 'rb') as f:
        voice = f.read()
    r = requests.post("http://127.0.0.1:5000", json={"voice": base64.b64encode(voice).decode(), "words": [["тушёнка"], ["деньги", "ололо"]]})
    print(r.text)