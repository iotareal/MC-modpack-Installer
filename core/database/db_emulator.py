import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.directory import Paths as dir
from core.api import version_handler as version
from core.api import api_handler as api
from core.exceptions import ModPackExceptions as mperr
from tinydb import TinyDB, Query

MODPACKS_TABLE = TinyDB(dir.get_modpacks_json()).table("ModPacks")
MODS_TABLE = TinyDB(dir.get_mods_json()).table("Mods")
query =  Query()

# SETTER
#Entity
def ModPack(name:str, version:str, loader:str, active=False, mods=[]):
    """
    Returns dictionary encapsulated with args
    Args:
        name (str): Name of Modpack
        version (str): Version of ModPack
        loader (str): Loader of ModPack
        active (bool, optional): Applicablility of Mods. Defaults to False.
        mods (list, optional): List of mods. Defaults to [].

    Returns:
        dict: ModPack Entity
    """
    return {
        "name" : name,
        "version" : version,
        "loader" : loader,
        "active" : active,
        "mods" : mods,
    }
#Entity
def Mod(mod:dict, active=False):
    """
    Returns Mod Entity for mods.json
    Args:
        mod (dict): json response from the Modrinth API
        active (bool, optional): Applicablility of Mod. Defaults to False.

    Returns:
        dict: Mod Entity
    """
    mod["Packlist"] = []
    mod["active"] = active
    return mod
    
# GETTER

#ndirec
def get_mod_by_id(mod_id:str):
    return MODS_TABLE.get(query.id == mod_id)

#ndirec
def get_pack_by_id(mod_id:int):
    return MODPACKS_TABLE.get(query.id == mod_id)

#ndirec
def get_active_mods(active = True):
    return MODS_TABLE.search(query.active == False)

# VALIDATOR
def check_pack(pack_id:int):
    return MODPACKS_TABLE.get(query.id == pack_id).get("active")

# CREATE 
def create_modpack_entry(name = "MyModpack", version=version.get_latest_release(), loader=version.get_random_loader()):
    if MODPACKS_TABLE.contains(query.name == name):
        raise mperr.ModPackExistsError(name)
    pack_id = MODPACKS_TABLE.insert(ModPack(name,version,loader))
    MODPACKS_TABLE.update({'id': pack_id}, doc_ids=[pack_id])
    print(f"modpacks.json: created pack {name}, id {pack_id}")

#ndirec
def create_mod_entry(mod:dict,pack_id):
    mod_from_table = get_mod_by_id(mod['id'])
    if mod_from_table:
        new_packlist = mod_from_table.get("Packlist", [])
        if pack_id not in new_packlist:
            new_packlist.append(pack_id)
            MODS_TABLE.update({"Packlist": new_packlist}, query.id == mod['id'])
            print(f"mods.json: created entry for mod_id {mod['id']}")
        return
    pack = get_pack_by_id(pack_id)
    mod = Mod(mod,pack['active'])
    mod['Packlist'].append(pack_id)
    MODS_TABLE.upsert(mod,query.id == mod['id'])
    
#UPDATE 
def update_modpack_name(old_name,new_name):
    if not MODPACKS_TABLE.contains(query.name == old_name):
        raise mperr.ModPackNotExistsError(old_name)
    
    MODPACKS_TABLE.update({"name" : new_name}, query.name == old_name)
    print(f"modpacks.json: updated name of pack {old_name} to {new_name}")

def add_mod_to_pack(pack_id,mod:dict):
    ModPack = get_pack_by_id(pack_id)
    if mod['id'] in ModPack["mods"]:
        raise mperr.ModExistsError(mod['id'],pack_id)
    
    ModPack["mods"].append(mod["id"])
    MODPACKS_TABLE.update(ModPack,query.id == pack_id)
    print(f"modpacks.json: added mod_id {mod['id']} to modpack_id {pack_id}")
    create_mod_entry(mod=mod,id=pack_id)

def activate_pack(pack_id:int,active = True):
    pack = get_pack_by_id(pack_id)
    mods = pack['mods']
    for mod in mods:
        activate_mod(mod,active=active)
    MODPACKS_TABLE.update({"active" : active},query.id == pack_id)
    print(f"modpacks.json: {pack["name"]} active is {active}")
    
#ndirec
def activate_mod(mod_id:str,active = True):
    MODS_TABLE.update({'active' : active}, query.id == mod_id)
    print(f"mods.json: {mod_id} active is {active}")
    
# DELETE

# ndirec
def del_mod_entry(mod_id:str):
    if len(MODS_TABLE.get(query.id == mod_id).get("Packlist")) == 0:
        MODS_TABLE.remove(query.id == mod_id)
        print(f"mods: deleted mod_id {mod_id}")
        
def del_modpack_entry(pack_id:int):
    if check_pack(pack_id):
        activate_pack(pack_id,active=False)
    MODPACKS_TABLE.remove(query.id == pack_id)
    print(f"modpacks.json: removed pack of id {pack_id}")
# TRY TO MAKE A SOLUTION SUCH THAT THE PACK IS REMOVED FORM PACK.JSON AND THE LIST OF MODS.JSON
del_modpack_entry(1)
    
# def delete_mod():
# mod = api.get_manipulated_response('sodium','1.21.1')
# add_mod_to_pack(1,mod)
# print(MODS_TABLE.contains(query.id == mod['id']))
# print(get_pack_by_id(1))
# create_modpack_entry("Performance")
# print(add_mod_to_pack(1,"sodium"))
