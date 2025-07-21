import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.directory import dir_handler as dir
from core.api import version_handler as version
from core.api import api_handler as api
from core.exceptions import ModPackExceptions as mperr
from tinydb import TinyDB, Query

MODPACKS_TABLE = TinyDB(dir.get_modpacks_json()).table("ModPacks")
MODS_TABLE = TinyDB(dir.get_mods_json()).table("Mods")
query =  Query()

# SETTER
def ModPack(name:str, version:str, loader:str, active=False, mods=[]):
    return {
        "name" : name,
        "version" : version,
        "loader" : loader,
        "active" : active,
        "mods" : mods,
    }

def Mod(mod:dict, active=False):
        mod["Packlist"] = []
        mod["active"] = active
        return mod
    
# GETTER
def get_mod_by_id(id):
    return MODS_TABLE.get(query.id == id)
def get_pack_by_id(id):
    return MODPACKS_TABLE.get(query.id == id)

# CREATE 
def create_modpack_entry(name = "MyModpack", version=version.get_latest_release(), loader=version.get_random_loader()):
    if MODPACKS_TABLE.contains(query.name == name):
        raise mperr.ModPackExistsError(name)
    id = MODPACKS_TABLE.insert(ModPack(name,version,loader))
    MODPACKS_TABLE.update({'id': id}, doc_ids=[id])
    print(f"modpacks: created - {name}, id - {id}")

def create_mod_entry(mod:dict,id):
    mod_from_table = MODS_TABLE.get(query.id == mod['id'])
    if mod_from_table:
    # Only update the Packlist field
        new_packlist = mod_from_table.get("Packlist", [])
        if id not in new_packlist:
            new_packlist.append(id)
            MODS_TABLE.update({"Packlist": new_packlist}, query.id == mod['id'])
        return
    pack = get_pack_by_id(id)
    mod = Mod(mod,pack['active'])
    mod['Packlist'].append(id)
    MODS_TABLE.upsert(mod,query.id == mod['id'])
    
#UPDATE
    
    
def update_modpack_name(old_name,new_name):
    if not MODPACKS_TABLE.contains(query.name == old_name):
        raise mperr.ModPackNotExistsError(old_name)
    
    MODPACKS_TABLE.update({"name" : new_name}, query.name == old_name)

def add_mod_to_pack(id,mod:dict):
    ModPack = MODPACKS_TABLE.get(query.id == id)
    if mod['id'] in ModPack["mods"]:
        raise mperr.ModExistsError(mod['id'],id)
    
    ModPack["mods"].append(mod["id"])
    MODPACKS_TABLE.update(ModPack,query.id == id)
    print(f"modpacks: added {mod['id']} to modpack_id {id}")
    create_mod_entry(mod=mod,id=id)
    
    
mod = api.get_manipulated_response('ferrite-core','1.21.1')
add_mod_to_pack(2,mod)
# print(MODS_TABLE.contains(query.id == mod['id']))
# print(get_pack_by_id(1))
# create_modpack_entry("Performance")
# print(add_mod_to_pack(1,"sodium"))