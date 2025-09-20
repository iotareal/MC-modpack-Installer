import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.api import api_service
from core.database import database_service as db
from core.directory import paths
# from core.directory import fileops
from core import models

_active_pack = None
def create_modpack(name:str,version:str,loader:str,active=False):
    db.checkfordupe_mpack(name) # database_service
    api_service.validate_version(version) #api_service
    api_service.validate_loader(loader) #api_service
    pack = models.Modpack(
        name=name,
        minecraft_version=version,
        loader=loader,
        active=active
    )
    return db.create_modpack_entry(pack)

pack = models.Modpack(
        name="Performance",
        minecraft_version="1.21.1",
        loader="fabric"
    )
# FILE OPERATIONS


# GETTERS
def get_packs():
    return db.get_packs()

def get_active_pack():
    if not _active_pack:
        raise Exception("[modpack] No modpack is currently selected.")
    return _active_pack

# SELECTORS
def select_pack(id:str):
    global _active_pack
    print(db.activate_pack(id))

def list_mod_version(id:str) -> list[dict]:
    global _active_pack
    api_service.get_project_version(id,_active_pack)
    

# SETTERS     
def rename_active_pack(new_name: str):
    active_pack = get_active_pack()
    message = db.rename_pack(active_pack['id'], new_name)
    select_pack(active_pack['id'])
    print(message)

# UPDATORS
def change_selected_pack_version(new_version: str):
    """
    This is your "one-click update" feature.
    It will be the most complex function you write.
    """
    active_pack = get_active_pack()
    print(f"Beginning update for '{active_pack['name']}' to version {new_version}...")

    # 1. Validate the new version using the API service
    if not api_service.validate_version(new_version):
        raise Exception("Invalid Minecraft version.")

    # 2. Get the full list of mod objects in the current pack
    current_mods = api_service.get_mods(db.get_pack_mods(active_pack['id'])) ## SUCESS FULLY IMPLEMENTED api_service::getmods()
    # SEND ALL MODS TO BUFFER FOLDER
    
    # 3. Loop through each mod...
    for mod in current_mods:
        # ...call the API service to find a compatible version for the new MC version...
        new_mod_version = api_service.get_mod_by_mcversion(mod['slug'], new_version)

        if new_mod_version:
            # ...if found, download the new file and update the database.
            print(f"Updating {mod['title']}...")
            api_service.download_mod_file(new_mod_version)
            # DOWNLOAD AND SAVE MODS TO MAIN FOLDER
        else:
            # ...if not found, notify the user and maybe remove it from the pack.
            print(f"Warning: No compatible version found for {mod['title']}.")

    # 4. Finally, update the modpack's version in the database
    db.change_pack_version(active_pack['id'], new_version)
    print("Update complete!")
    

    
    
