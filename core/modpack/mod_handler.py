# CRUD ops on mods, handle mod centric api requests
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.directory import Paths as dir
from tinydb import TinyDB, Query
import json
import shutil
import requests
import zipfile

###{
MODS_JSON = dir.get_mods_json()
MOD = Query()
###}
def get_db():
    return TinyDB(MODS_JSON)

def prettify():
    with open(MODS_JSON, 'r') as f:
        data = json.load(f)
    with open(MODS_JSON, 'w') as f:
        json.dump(data, f, indent=2)
        
def add_mod_to_db(mod:dict,type,active=False):
    mod["type"] = type
    mod["active"] = active
    with get_db() as db:
        db.upsert(mod,MOD.id == mod['id'])
    prettify()

def add_mod_file(file_path):
    file_path = os.path.join(dir.get_buffer_dir(),file_path)
    if not os.path.exists(file_path) and os.path.isdir():
        return False

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in [".jar", ".zip"]:
        return "unknown"

    try:
        with zipfile.ZipFile(file_path, 'r') as archive:
            files = archive.namelist()
            files_lower = [f.lower() for f in files]

            if ext == ".jar":
                return "mod"

            elif ext == ".zip":
                if 'pack.mcmeta' in files_lower:
                    if any(f.startswith("assets/") for f in files_lower):
                        return "resourcepack"
                    elif any(f.startswith("data/") for f in files_lower):
                        return "datapack"
                elif any(f.startswith("shaders/") for f in files_lower):
                    return "shaderpack"
                else:
                    return "unknown"

    except zipfile.BadZipFile:
        return "error:bad_zip"

print()