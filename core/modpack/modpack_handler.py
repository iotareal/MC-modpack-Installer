# Perform CRUD operation on modpack entity and modpacks.json
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.directory import Paths as dir
from core.exceptions import ModPackExceptions as err
from core.exceptions import VersionExceptions as verr
from core.modpack import mod_handler as md
from core.api import version_handler as ver
from tinydb import TinyDB, Query
import json

###{{{
MODPACKS_JSON=dir.get_modpacks_json()
MODPACK=Query()
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
        pack=db.get(MODPACK.name==pack_name.lower())
        if pack:
            raise err.MODPACKExistsError(pack_name.lower())
        
        db.insert(pack_entity(pack_name.lower(),version,loader,active))
        prettify()
        print(f"modpacks.json: added {pack_name.lower()}")

# READ
def get_modpacks():
    with get_db() as db:
        return db.all()

def get_active(active=True):
    with get_db() as db:
        return db.get(MODPACK.active == active)

def get_modpack_by_name(pack_name:str):
    with get_db() as db:
        pack = db.get(MODPACK.name == pack_name.lower())
        if not pack:
            raise err.ModPackNotExistsError(pack_name.lower())
        return pack

# UPDATE
def rename_pack(old_name:str,new_name:str):
    with get_db() as db:
        pack = db.get(MODPACK.name == old_name.lower())
        if not pack:
            raise err.ModPackNotExistsError(old_name)
        if db.get(MODPACK.name == new_name.lower()):
            raise err.ModPackExistsError(new_name)
        db.update({"name" : new_name.lower()}, MODPACK.name == old_name.lower())
        print(f"modpacks.json: renamed {old_name} to {new_name}")
        prettify()

def change_version(pack_name:str,version):
    versions=ver.get_all_versions()
    if version not in versions:
        raise verr.VersionNotFoundError(version)
    with get_db() as db:
        if not db.get(MODPACK.name == pack_name.lower()):
            raise err.ModPackNotExistsError(pack_name.lower())
        db.update({"version" : version}, MODPACK.name == pack_name.lower())
        print(f"modpacks.json: version changed to {version} for {pack_name}")
        prettify()

def add_mod(pack_name:str,mod:dict):
    with get_db as db:
        pack = db.get(MODPACK.name == pack_name.lower())
        if not pack:
            raise err.ModPackNotExistsError(pack_name)
        pack["mods"]
        prettify()
    
# DELETE
def remove_all_mods(pack_name:str):
    with get_db() as db:
        if not db.get(MODPACK.name == pack_name.lower()):
            raise err.ModPackNotExistsError(pack_name)
        db.update({"mods" : []}, MODPACK.name == pack_name.lower())
        print(f"modpacks.json: all mods removed from {pack_name.lower()}")
        prettify()
        
# create_pack("Modpack 1","1.16.3","fabric")
# print(get_active(False))
# print(get_modpack_by_name("Performance Mods"))
# rename_pack("Performance","Modpack 1")
# change_version("Modpack 1","1.21")
# remove_all_mods("Modpack 1")
