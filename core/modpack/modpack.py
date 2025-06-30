from tinydb import TinyDB, Query
from core.directory import dir_handler as dir
from core.exceptions import ModPackExceptions as error
import os
import json

MODPACK_FILE = os.path.join(dir.get_modman_folder(), "modpacks.json")
db=TinyDB(MODPACK_FILE)
ModPack=Query()

# Initializes modpack.json file
def init_modpacks_json():
    os.chdir(dir.get_modman_folder())
    try:
        with open("modpacks.json",'x') as file:
            pass
    except FileExistsError:
        os.chdir(MODPACK_FILE)
        
def create_modpack(name):
    init_modpacks_json()
    if db.search(ModPack.name == name):
        raise error.ModPackExistsError(name)
    db.insert({"name":name, "mods":[], "active":False})

def set_active(name):
    if not db.search(ModPack.name == name):
        raise error.ModPackNotExistsError(name)
    packs=db.all()
    for pack in packs:
        db.update({"active":False}, ModPack.name==pack["name"])
    db.update({"active":False}, ModPack.name==name)
    
def add_mod(pack_name,mod):
    pack=db.get(ModPack.name==pack_name)
    if not pack:
        raise error.ModPackNotExistsError(pack_name)
    
    if any(m["slug"] == mod["slug"] and m["version"] == mod["version"] for m in pack["mods"]):
        raise error.ModExistsError(mod["title"],pack_name)

    pack["mods"].append(mod)
    db.update({"mods": pack["mods"]}, ModPack.name == pack_name)

def remove_mod(pack_name,mod):
    pack=db.get(ModPack.name==pack_name)
    if not pack:
        raise error.ModPackNotExistsError(pack_name)
    
    if any(m["slug"] == mod["slug"] and m["version"] == mod["version"] for m in pack["mods"]):
        raise error.ModExistsError(mod["title"],pack_name)
    for _mod in pack["mods"]:
        if _mod["name"] == mod[]
    