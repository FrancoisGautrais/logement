from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
CONF_DIR = BASE_DIR / "conf"

def default_file(path, value):
    if path.is_file(): return
    if not path.parent.is_dir():
        path.parent.mkdir(parent=True)

    path.write_text(value)


default_file(CONF_DIR / "password", "")
default_file(CONF_DIR / "exclude", "")
default_file(CONF_DIR / "include", "")
default_file(CONF_DIR / "conf.json", "{}")
