import os
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

from logement.libs.utils import need_auth


@need_auth
def download(req : HttpRequest, id : str):
    cache = settings.CACHE_PATH / f"{id}.zip"
    if cache.is_file():
        ret = HttpResponse(content=cache.read_bytes(), content_type="application/zip", )
    else:
        return HttpResponse()

def mk_tree(dir):
    old = os.getcwd()
    os.chdir(dir)
    process = subprocess.run(["tree"], stdout=subprocess.PIPE)
    ret = process.stdout
    os.chdir(old)
    return "\n".join(ret.decode("utf8").split("\n")[1:-2])


def generate_note(dir, data):
    dir = Path(dir)
    (dir / "note.txt").touch()
    tree = mk_tree(dir)

    out = []
    if data.get("note"):
        out.append(f"Note:\n{data.get('note')}")

    out.append(f"Liste des fichiers:\n{tree}")
    (dir / "note.txt").write_text("\n\n".join(out))




def integrate_zip(dir, data):
    filename = Path(f"F. Gautrais T. Zaragoza {data.get('reference').replace(':', ' ')}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        zipfile = tmp / "data.zip"
        root = tmp / "tmp"
        zip_dir = root / "dossier"
        shutil.copy(settings.DATA_PATH / "data.zip", zipfile)
        with ZipFile(zipfile) as zip:
            zip.extractall(root)

        for d in dir.iterdir():
            shutil.copy(d, zip_dir / d.name)

        generate_note(zip_dir, data)

        if (settings.DATA_PATH / "cache" / "zip.zip").exists():
            (settings.DATA_PATH / "cache" / "zip.zip").unlink()
        with ZipFile(settings.DATA_PATH / "cache" / "zip.zip", "w") as zip:
            queue = [zip_dir]
            while queue:
                curr = queue.pop(0)
                for file in curr.iterdir():
                    if file.is_file():
                        zip.write(file, filename/file.relative_to(zip_dir))
                    else:
                        queue.append(file)

    return (settings.DATA_PATH / "cache" / "zip.zip").read_bytes(), f"{filename}.zip"



@need_auth
def upload(request : HttpRequest):
    if request.method == 'POST':
        if settings.PASSWORD != request.POST.get("password"):
            return HttpResponse('<h1>Mauvais mot de passe</h1>', content_type="text/html")
        with tempfile.TemporaryDirectory() as dir :
            dir = Path(dir)
            files = request.FILES.getlist("files")
            for f in files:
                with open(dir / f.name, "wb") as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            out, filename = integrate_zip(dir, request.POST)
            return HttpResponse(out, headers={
                "Content-Disposition" : f'attachment; filename="{filename}"',
                "Content-Type" : "application/zip"
            })

@need_auth
def page(req : HttpRequest):
    data = defaultdict(str)
    data.update(req.GET or req.POST)
    data = { k: x[0] if x else "" for k, x in data.items()}
    return render(req, "dossier.html", data)

@need_auth
def mail(req : HttpRequest):
    data = { k: v[0] if isinstance(v, (list,tuple)) else v for k, v in (req.POST or req.GET).items()}
    return render(req, "mail", data, content_type="text/plain")

urls = [
    path("download", download),
    path("upload", upload),
    path("mail", mail),
    path("", page),
]