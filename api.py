import requests
import xml.etree.ElementTree as ET
URL = "https://asr.yandex.net/asr_xml?uuid=2ebb3f90fc3b454cbbcaa407f7b2b402&key=3427dc30-5eb2-4790-8065-d7ef6f4de74e&topic=queries&lang=ru-RU"


def stt(fname):
    with open(fname, 'rb') as f:
        data = f.read()
    r = requests.post(URL, data=data, headers={'Content-Type': 'audio/x-wav'})
    print(r.text)


stt("voice/20181027 140545.wav")

# curl -X POST -H "Content-Type: audio/x-wav" --data-binary "voice/1.wav" "https://asr.yandex.net/asr_xml?uuid=2ebb3f90-fc3b-454c-bbca-a407f7b2b402&key=3427dc30-5eb2-4790-8065-d7ef6f4de74e&topic=queries&lang=ru-RU"
# curl -X POST -H "Content-Type: audio/x-wav" --data-binary "@/home/xozzslip/coding/retail-KPI/voice/1.wav" "https://asr.yandex.net/asr_xml?uuid=2ebb3f90fc3b454cbbcaa407f7b2b402&key=3427dc30-5eb2-4790-8065-d7ef6f4de74e&topic=queries&lang=ru-RU"