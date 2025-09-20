import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
#FOR TESTING
from core.api import api_service
import json

from core.exceptions import ModPackExceptions as mperr
from core.directory import paths
from core.models import Modpack
from tinydb import TinyDB, Query
import os

# Tables
MODPACKS = TinyDB(paths.get_db(),indent=4).table("MODPACKS")
MODS = TinyDB(paths.get_db(),indent=4).table("MODS")
VERSIONS = TinyDB(paths.get_db(), indent=4).table("VERSIONS")

# Query
query = Query()

# GETTERS
def get_pack(name:str):
    return MODPACKS.get(query.name == name)

def get_packs():
    return MODPACKS.all()

def __get_active_packs():
    return MODPACKS.get(query.active == True)

def get_pack_mods(id:str):
    return MODPACKS.get(query.id == id)['mods']

def get_mod(id:str):
    return MODS.get(query.project_id == id)
    
def get_mods(mods:list) -> tuple:
    return (get_mod(id) for id in mods)
# SETTERS
    
    
# VALIDATORS
def checkfordupe_mpack(name:str):
    if get_pack(name):
        raise mperr.ModPackExistsError(name)
def deactivate_all_packs():
    active_packs = __get_active_packs()
    for pack in active_packs:
        set_pack_active(pack['id'],active=False)
    
# CRUD Operations
# CREATE
def create_modpack_entry(pack:Modpack) -> str:
    id = MODPACKS.insert(pack.model_dump())
    pack.id = id
    MODPACKS.update(pack.model_dump(), doc_ids=[id])
    return f"[database]: created entry for {pack.name}"

def __create_mod_entry(mod:dict):
    main_url = f"https://api.modrinth.com/v2/project/{mod['project_id']}"
    mod['main_url'] = main_url
    MODS.insert(query.id == mod['id'])

# READ
# UPDATE
def set_pack_active(id,active = True) -> str:
    deactivate_all_packs()
    MODPACKS.update({"active" : active},query.id == id)
    return f"[database]: pack_id {id} is now active" if active else f"[database]: pack_id {id} is now inactive"

def rename_pack(id:str,new_name:str) -> str:
    MODPACKS.update({"name":new_name},query.id == id)
    return f"[database] renamed pack_id {id} to {new_name}"

pack = __get_active_packs()
mod = api_service.get_mod("minihud",pack)
print(json.dumps(mod,indent = 4))