from tinydb import TinyDB, Query
from core.directory import dir_handler as dir
from core.exceptions import ModPackExceptions as error
import os
import json

MODPACK_FILE = os.path.join(dir.get_modman_folder(), "modpacks.json")
if not os.path.exists(MODPACK_FILE):
    with open("modpacks.json",'x') as file:
            pass
    os.chdir(dir.get_modman_folder())
else:
    os.chdir(dir.get_modman_folder())
ModPack=Query()


def prettify_modpack_file():
    with open(MODPACK_FILE, 'r') as f:
        data = json.load(f)
    with open(MODPACK_FILE, 'w') as f:
        json.dump(data, f, indent=2)
        
def get_db():
    return TinyDB(MODPACK_FILE)

def create_modpack(name,loader,version,set_active=False):
    with get_db() as db:
        if db.search(ModPack.name == name):
            raise error.ModPackExistsError(name)
        else:
            db.insert({"name":name,"for_version":version,"for_loader":loader, "active":set_active, "mods":[]})
    prettify_modpack_file()
            
def set_active(pack_name):
    with get_db() as db:
        if db.get(ModPack.name == pack_name) is None:
            raise error.ModPackNotExistsError(pack_name)
        packs=db.all()
        for pack in packs:
            db.update({"active":False}, ModPack.name==pack["name"])
        db.update({"active":True}, ModPack.name==pack_name)
    prettify_modpack_file()
    
def add_mod(pack_name,mod):
    set_active(pack_name)
    with get_db() as db:
        pack=db.get(ModPack.name==pack_name)
        if not pack:
            raise error.ModPackNotExistsError(pack_name)
        
        if any(_mod['id'] == mod['id'] for _mod in pack["mods"]):
            raise error.ModExistsError(mod["name"],pack_name)

        pack["mods"].append(mod)
        db.update({"mods": pack["mods"]}, ModPack.name == pack_name)
    prettify_modpack_file()

def delete_modpack(pack_name):
    with get_db() as db:
        pack=db.get(ModPack.name==pack_name)
        if not pack:
            raise error.ModPackNotExistsError(pack_name)
        
        db.remove(ModPack.name == pack_name)
    prettify_modpack_file()
    
def remove_mod(pack_name,mod):
    with get_db() as db:
        pack=db.get(ModPack.name==pack_name)
        if not pack:
            raise error.ModPackNotExistsError(pack_name)
        
        if not any(_mod['id'] == mod['id'] for _mod in pack["mods"]):
            raise error.ModNotExistsError(mod["name"], pack_name)
        
        updated_pack = [_mod for _mod in pack["mods"] if _mod['id'] != mod['id']]
        db.update({"mods": updated_pack}, ModPack.name == pack_name)
    prettify_modpack_file()
def get_active_modpack():
    with get_db() as db:
        return db.get(ModPack.active == True)
    
def list_of_all_modpacks():
    with get_db() as db:
        return db.all()
    
def rename_packname(new,old):
    with get_db() as db:
        pack=db.get(ModPack.name==old)
        if not pack:
            raise error.ModPackNotExistsError(old)
        db.update({'name':new},ModPack.name==old)
        print(f"Successfully Updated Name: {old} to {new}")
    prettify_modpack_file()
        
        
            
