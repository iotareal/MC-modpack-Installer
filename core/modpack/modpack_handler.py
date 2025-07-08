# Perform CRUD operation on modpack entity and modpacks.json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.directory import dir_handler as dir
from core.exceptions import ModPackExceptions as err
from core.exceptions import VersionExceptions as verr
from core.modpack import mod_handler as md
from core.api import version_handler as ver
from tinydb import TinyDB, Query
import json

###{{{
MODPACKS_JSON=dir.get_modpacks_json()
ModPack=Query()
###}}}

def pack_entity(name:str, version:str, loader:str, active=False, mods=[]):
    return {
        "name" : name,
        "version" : version,
        "loader" : loader,
        "active" : active,
        "mods" : mods,
    }
    
def get_db():
    return TinyDB(MODPACKS_JSON)

def prettify():
    with open(MODPACKS_JSON, 'r') as f:
        data = json.load(f)
    with open(MODPACKS_JSON, 'w') as f:
        json.dump(data, f, indent=2)

# CREATE
def create_pack(pack_name:str,version:str,loader:str,active=False):
    versions=ver.get_all_versions()
    loaders=ver.get_loaders()
    
    if not version in versions:
        raise verr.VersionNotFoundError(version)
    if not loader in loaders:
        raise verr.LoaderNotFoundError(loader)
    
    with get_db() as db:
        pack=db.get(ModPack.name==pack_name.title())
        if pack:
            raise err.ModPackExistsError(pack_name.title())
        
        db.insert(pack_entity(pack_name.title(),version,loader,active))
        prettify()
        print(f"modpacks.json: added {pack_name}")

# READ
def get_modpacks():
    with get_db() as db:
        return db.all()

def get_active(active=True):
    with get_db() as db:
        return db.get(ModPack.active == active)

def get_modpack_by_name(pack_name):
    with get_db() as db:
        pack = db.get(ModPack.name == pack_name)
        if not pack:
            raise err.ModPackNotExistsError(pack_name)
        return pack

# UPDATE

# create_pack("Modpack 1","1.16.3","fabric")
# print(get_active(False))
# print(get_modpack_by_name("Performance Mods"))