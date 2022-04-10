from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.conf import settings

def _serv(file):
    def _do_serv(req : HttpRequest):
        return HttpResponse(content=file.read_bytes(), content_type={
            ".js" : "text/javascript",
            ".css" : "text/css",
            ".html" : "text/html",
            ".png": "image/png",
            ".jpg": "image/jpg",
        }[file.suffix])
    return _do_serv

def find_static_files():
    files = []
    root = settings.BASE_DIR / "www" / "static"
    queue = [root]
    while queue:
        curr = queue.pop(0)
        for c in curr.iterdir():
            if c.is_file():
                files.append(c.relative_to(root))
            else:
                queue.append(c)
    return [
        path(str(x), _serv(root / x)) for x in files
    ]