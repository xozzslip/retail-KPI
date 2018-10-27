import requests
import xml.etree.ElementTree as ET
URL = "https://asr.yandex.net/asr_xml?uuid=2ebb3f90fc3b454cbbcaa407f7b2b402&key=3427dc30-5eb2-4790-8065-d7ef6f4de74e&topic=queries&lang=ru-RU"


def stt(fname):
    with open(fname, 'rb') as f:
        data = f.read()
    r = requests.post(URL, data=data, headers={'Content-Type': 'audio/ogg;codecs=opus'})
    if not r.status_code == 200:
        raise requests.exceptions.HTTPError(r.text)
    root = ET.fromstring(r.text)
    if not int(root.attrib['success']) == 1:
        raise requests.exceptions.HTTPError(r.text)
    return list(root)[0].text


def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n+1)
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def is_scripted(text, rootwords_t):
    words = text.split()
    double_words = make_doublewords(words)
    rootwords_t = set(rootwords_t)
    found = set()
    for rword_t in rootwords_t:
        if find_rword_t(words, rword_t):
            found.add(rword_t)
    for rword_t in (rootwords_t - found):
        if find_rword_t(double_words, rword_t):
            found.add(rword_t)
    return len(found) / len(rootwords_t)


def find_rword_t(words, rword_t):
    for rword in rword_t:
        for word in words:
            if distance(word, rword) <= max(2, len(rword) // 3):
                return True
    return False


def make_doublewords(words):
    doublewords = []
    for i in range(len(words) - 1):
        doublewords.append("{} {}".format(words[i], words[i + 1]))
    return doublewords


r = stt("voice3/audio_2018-10-27_19-06-17.ogg")
print(is_scripted(r, [("наличные"), ("картой", "по карте")]))
print(r)

