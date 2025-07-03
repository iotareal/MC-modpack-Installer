from core.directory import dir_handler as dir
from core.exceptions import ModPackExceptions as error
from core.modpack import mod_handler as md
from tinydb import TinyDB, Query
import os
import json

###{{{
dir.default_dir()
MODPACK_FILE = os.path.join(dir.get_modman_folder(), "modpacks.json")
if not os.path.exists(MODPACK_FILE):
    dir.create_modpacks_json()
dir.change_to_modman_dir()
ModPack=Query()
###}}}

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
    print(f"\nModpack: {name} for {loader}-{version} created.")
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
    md.assign_modpack(pack_name,mod)
    with get_db() as db:
        pack=db.get(ModPack.name==pack_name)
        if not pack:
            raise error.ModPackNotExistsError(pack_name)
        
        if any(_mod['id'] == mod['id'] for _mod in pack["mods"]):
            raise error.ModExistsError(mod["name"],pack_name)

        pack["mods"].append(mod)
        db.update({"mods": pack["mods"]}, ModPack.name == pack_name)
    print(f"\nMod: {mod["name"]} from {pack_name} created")
    prettify_modpack_file()

def delete_modpack(pack_name):
    with get_db() as db:
        pack=db.get(ModPack.name==pack_name)
        if not pack:
            raise error.ModPackNotExistsError(pack_name)
        
        db.remove(ModPack.name == pack_name)
    print(f"\nModpack: {pack_name} deleted.")
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
    print(f"\nMod: {mod["name"]} from {pack_name} deleted")
    prettify_modpack_file()
    
def remove_mod_by_name(pack_name,mod):
    with get_db() as db:
        pack=db.get(ModPack.name==pack_name)
        if not pack:
            prettify_modpack_file()
            raise error.ModPackNotExistsError(pack_name)
        
        if not any(_mod["name"] == mod for _mod in pack["mods"]):
            prettify_modpack_file()
            raise error.ModNotExistsError(mod, pack_name)
        
        updated_pack = [_mod for _mod in pack["mods"] if _mod["name"] != mod]
        db.update({"mods": updated_pack}, ModPack.name == pack_name)
    print(f"\nMod: {mod} from {pack_name} deleted")
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

def get_modpack(pack_name):
    with get_db() as db:
        pack=db.get(ModPack.name==pack_name)
        if not pack:
            raise error.ModPackNotExistsError(pack_name)
        return pack
    
    
        
            
