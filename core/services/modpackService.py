# For testing
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.classes.ModPack import ModPack
from core.api import apiService as api
from core.api import versionService as vers
from core.exceptions import ModPackExceptions as mperr
import shutil 
import pickle

SELECTED_PACK = None
SELECTED_PACK_FILE = ".\\selectedpack.pkl"
MODPACKS = ".\\packs.pkl"

my_modpack = ModPack(name="My Modpack", version="1.21.1", loader="fabric")

def write(pack):
    try:
        with open(MODPACKS,'rb') as file:
            packs = pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        packs = []
    
    packs.append(pack)
    
    with open(MODPACKS, 'wb') as file:
        pickle.dump(packs, file)
        
def writeall(packs):
    with open(MODPACKS, 'wb') as file:
        pickle.dump(packs, file)

def read():
    try:
        with open(MODPACKS,'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return []
    

def getPacks():
    return read()

def getLastSelectedPack():
    with open(SELECTED_PACK_FILE,'rb') as file:
        return pickle.load(file)

def setLastSelectedPack():
    with open(SELECTED_PACK_FILE,'wb') as file:
        return pickle.dump(SELECTED_PACK,file)

def createModpack(name:str, version:str, loader:str):
    pack = ModPack(name=name, version=version, loader=loader)
    write(pack)
    return f"[modpackService] create modpack id: {pack.id}"

def changeActive(id,active=True):
    packs = getPacks()
    for pack in packs:
        pack.active = False
        
    for pack in packs:
        if(pack.id == id): 
            pack.active = active
            writeall(packs)
            return f"[modpackService] Modpack: {id} active:{active}"
    raise mperr.ModPackNotExistsError(id)

def selectModPack(id):
    global SELECTED_PACK
    packs = getPacks()
    for pack in packs:
        if pack.id == id: 
            SELECTED_PACK = pack
            changeActive(SELECTED_PACK.id)
            setLastSelectedPack()            
            return f"[modpackService] Modpack: {SELECTED_PACK.id} is now selected"
    
    raise mperr.ModPackNotExistsError(id)

def addModtoSelectedPack():
    global SELECTED_PACK
    query = input("Enter Modname: ")
    foundmods = api.search_mods(query,SELECTED_PACK)
    for mod in foundmods:
        print(f"{mod['project_id']}\t{mod['title']}\t{mod['project_type']}")
            
# MAIN COURSE
# def updateModPack(id,version):
#     global SELECTED_PACK
#     if SELECTED_PACK.version == version: return f"[modpackService] version is already {version}"
#     print(f"Updating Modpack: {SELECTED_PACK.name} please do not exit.. ")
#     SELECTED_PACK.version = version
#     print(f"[modpackService] changed version to {SELECTED_PACK.version}")
#     mods = SELECTED_PACK.mods
#     modids = tuple(s.split("-")[0] for s in mods)

# TEST
# def moveFilestoBuffer():
print(selectModPack("0b55be5d-c878-4d1b-a167-bba0e930dfd5"))
# packs = getPacks()
# print(getLastSelectedPack())
addModtoSelectedPack()
# for pack in packs:
#     print(pack)

