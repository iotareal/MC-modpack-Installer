from core.exceptions import JarFileExceptions as error
from core.directory import dir_handler as dir
from core.modpack import modpack_handler as mp
from tinydb import TinyDB, Query
import shutil
import json
import os

###{{{
MODS_FILE = os.path.join(dir.get_mods_folder(), "mods.json")
if not os.path.exists(MODS_FILE):
    dir.create_mods_json()

if not os.path.exists(os.path.join(dir.get_modman_folder(),"buffer")):
    dir.get_buffer_folder()
    
query=Query()
###}}}

def prettify_mods_file():
    with open(MODS_FILE, 'r') as f:
        data = json.load(f)
    with open(MODS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print("mods.json: Prettyfied")

def get_db():
    return TinyDB(MODS_FILE)

def get_mod_file(filename):
    path1=os.path.join(dir.get_mods_folder(),filename)
    path2=os.path.join(dir.get_buffer_folder(),filename)
    if os.path.exists(path1):
        return path1
    elif os.path.exists(path2):
        return path2
    else:
        raise FileNotFoundError

def enlist_mod_entity(mod):
    mod["active"]=False
    mod["assigned_to"]=[]
    with get_db() as db:
        db.upsert(mod,query.id == mod['id'])
    prettify_mods_file()
    print(f"mods.json: {mod["name"]} upserted")

def delist_mod(mod_filename:str):
    with get_db() as db:
        db.remove(query.files[0].filename == mod_filename)
    print(f"mods.json: mod with name {mod_filename} delisted")

def set_active_true(filename:str):
    with get_db() as db:
        db.update({"active": True}, query.files[0].filename == filename)
        
def set_active_false(filename:str):
    with get_db() as db:
        db.update({"active": False}, query.files[0].filename == filename)

def move_to_buffer(filename):
    src=os.path.join(dir.get_mods_folder(),filename)
    if not os.path.exists(src):
        raise error.ModFileNotExistsError(filename,dir.get_mods_folder())
    dst=dir.get_buffer_folder()
    shutil.move(src,dst)
    set_active_false(filename)
    print(f"file: {filename} is moved to {dst}")

def move_to_mods(filename):
    src=os.path.join(dir.get_buffer_folder(),filename)
    if not os.path.exists(src):
        raise error.ModFileNotExistsError(filename,dir.get_buffer_folder())
    dst=dir.get_mods_folder()
    shutil.move(src,dst)
    set_active_true(filename)
    print(f"file: {filename} is moved to {dst}")

def assign_to_modpack(pack_name,filename):
    pack=mp.get_active_modpack()
    if pack_name in pack[]
    filename=get_mod_file(filename)
    with get_db() as db:
        mod=db.get(query.files[0].filename == filename)
        if not pack_name in mod["assigned_to"]:
            mod["assigned_to"].append()
            db.update({"assigned_to": mod["mods"]}, query.files[0].filename == filename)
        print(f"mod: {mod["name"]} is part of {pack_name}")
    prettify_mods_file()
        
        
    
    
    
    