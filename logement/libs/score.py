import re
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from unidecode import unidecode
allowed_chars=f"abcdefghijklmnopqrstuvwxyz0123456789"
rm_space = re.compile(r" +")

CRIT = settings.CRITERES if hasattr(settings, "CRITERES") else {}

def uniform_data(x):
    x = unidecode(x).lower()
    x = "".join([c if c in allowed_chars else " " for c in x])
    return re.sub(rm_space, " ", x).split(" ")

def parse_crtiere_file(file):
    file = Path(file).read_text().split("\n")
    tmp = [uniform_data(x) for x in file if x]
    ret = defaultdict(list)
    for words in tmp:
        ret[words[0]].append(words[1:])

    return ret



INCLUDE = parse_crtiere_file(CRIT.get("words.include"))
EXCLUDE = parse_crtiere_file(CRIT.get("words.exclude"))

def reload():
    global INCLUDE, EXCLUDE
    INCLUDE = parse_crtiere_file(CRIT.get("words.include"))
    EXCLUDE = parse_crtiere_file(CRIT.get("words.exclude"))



def _score(content, crit):
    ret = []
    nb = len(content)
    i=0
    while i<nb:
        word=content[i]
        if word in crit and i+len(crit[word])<nb:
            for arr in crit[word]:
                j=0
                while j<len(arr):
                    if content[i+j+1] != arr[j]:
                        break
                    j+=1
                else:
                    ret.append(" ".join([word] + arr))
                    i+=j
        i+=1
    return ret


def score(data):
    if not isinstance(data, dict):
        fields = ["content", "address", "title"]
        tmp = data
        data = { k: getattr(tmp, k) for k in fields}
    content = " ".join([
            data.get("content") or "",
            data.get("address") or "",
            data.get("title") or "",
    ])
    content = uniform_data(content)
    return len(_score(content, INCLUDE)) - len(_score(content, EXCLUDE))


def score_debug(data):
    if not isinstance(data, dict):
        fields = ["content", "address", "title"]
        tmp = data
        data = { k: getattr(tmp, k) for k in fields}
    content = " ".join([
            data.get("content") or "",
            data.get("address") or "",
            data.get("title") or "",
    ])
    content = uniform_data(content)
    return _score(content, INCLUDE), _score(content, EXCLUDE)




def is_relevant(data):
    if not isinstance(data, dict):
        fields = ["prix", "surface"]
        tmp = data
        data = { k: getattr(tmp, k) for k in fields}
    loyer = data.get("prix")
    surface = data.get("surface")
    if not (CRIT.get("loyer.min", -1) <= loyer <= CRIT.get("loyer.max", 9999999)):
        return False

    if surface and not (CRIT.get("surface.min", -1) <= surface <= CRIT.get("surface.max", 9999999)):
        return False

    return True





