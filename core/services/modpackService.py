# For testing
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.classes.ModPack import ModPack
from core.api import apiService as api
from core.api import versionService as vers
from core.exceptions import ModPackExceptions as mperr
from core.directory import paths 
from tabulate import tabulate
from colorama import Fore,Style,init
import shutil 
import pickle

init(autoreset=True)
SELECTED_PACK = None
SELECTED_PACK_FILE = ".\\selectedpack.pkl"
MODPACKS = ".\\packs.pkl"


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

def getActivepack():
    packs = getPacks()
    for pack in packs:
        if pack.active:
            return pack

def updateAllPacks():
    global SELECTED_PACK
    setLastSelectedPack()
    packs = getPacks()
    for i,pack in enumerate(packs):
        if pack.id == SELECTED_PACK.id:
            break
    packs[i] = SELECTED_PACK
    writeall(packs)
    print(f"{Fore.GREEN}[modpackService] updated all packs")
    
def createModpack(name:str, version:str, loader:str):
    pack = ModPack(name=name, version=version, loader=loader)
    write(pack)
    print(f"{Fore.GREEN}[modpackService] create modpack id: {pack.id}")

def changeActive(id,active=True):
    packs = getPacks()
    for pack in packs:
        pack.active = False
        
    for pack in packs:
        if(pack.id == id): 
            pack.active = active
            writeall(packs)
            print(f"{Fore.GREEN}[modpackService] Modpack: {id} active:{active}")
            return
    raise mperr.ModPackNotExistsError(id)

def selectModPack(id):
    global SELECTED_PACK
    packs = getPacks()
    for pack in packs:
        if pack.id == id: 
            SELECTED_PACK = pack
            changeActive(SELECTED_PACK.id)
            setLastSelectedPack()            
            print(f"{Fore.GREEN}[modpackService] Modpack: {SELECTED_PACK.id} is now selected")
    
    raise mperr.ModPackNotExistsError(id)

def addModtoSelectedPack(query):
    global SELECTED_PACK
    foundmods = api.searchProjects(query,SELECTED_PACK)
    headers = ["Project_ID", "Title", "Project_Type"]
    tabledata = []
    for mod in foundmods:
        tabledata.append([
            mod.get('project_id', 'N/A'), 
            mod.get('title', 'N/A'), 
            mod.get('project_type', 'N/A')
        ])
    print(tabulate(tabledata,headers=headers, tablefmt="rounded_grid",showindex="always"))
    while(True):
        try:
            choice = int(input("\nPlease Enter the Index No: "))
            if(choice < 0 or choice >=len(tabledata)):
                print(f"Only acceptable values are from {0} to {len(tabledata)-1}")
                continue
            else:
                break
        except Exception:
            print(f"Only acceptable values are from {0} to {len(tabledata)-1}")
            continue
    selected_mod = foundmods[choice]
    print(f"You've Selected {selected_mod["title"]} which is a {selected_mod["project_type"]}")
    
    ptype = selected_mod["project_type"]
    # GETTING VERSION
    foundmods = api.get_mod_version(selected_mod,SELECTED_PACK)
    tabledata.clear()
    headers = ["version ID","version number"]
    for mod in foundmods:
        tabledata.append([
            mod.get('id','N/A'),
            mod.get('version_number','N/A')
        ])
    print(tabulate(tabledata,headers=headers, tablefmt="rounded_grid",showindex="always"))
    while(True):
        try:
            choice = int(input("\nPlease Enter the Index No: "))
            if(choice < 0 or choice >=len(tabledata)):
                print(f"{Fore.RED}Only acceptable values are from {0} to {len(tabledata)-1}")
                continue
            else:
                break
        except Exception:
            print(f"{Fore.RED}Only acceptable values are from {0} to {len(tabledata)-1}")
            continue
    selected_mod = foundmods[choice]
    selected_mod['project_type'] = ptype
    SELECTED_PACK.mods.append(selected_mod)
    updateAllPacks()
    api.download_mod(selected_mod)

def removeModfromSelectedPack():
    if len(SELECTED_PACK.mods) == 0:
        print(f"{Fore.GREEN}[modpackService] {SELECTED_PACK.name} has no mods")
        return 
    mods = []
    for mod in SELECTED_PACK.mods:
        mods.append(mod['project_id'])
    mods = api.getModsBulk(mods)
    headers = ["Mod title","Mod type"]
    tabledata = []
    for mod in mods:
        tabledata.append([
            mod.get("title","N/A"),
            mod.get('project_type',"N/A")
        ])
    print(tabulate(tabledata,headers=headers, tablefmt="rounded_grid",showindex="always"))
    while(True):
        try:
            choice = int(input("\nPlease Enter the Index No: "))
            if(choice < 0 or choice >=len(tabledata)):
                print(f"{Fore.RED}Only acceptable values are from {0} to {len(tabledata)-1}")
                continue
            else:
                break
        except Exception:
            print(f"{Fore.RED}Only acceptable values are from {0} to {len(tabledata)-1}")
            continue
    for i,mod in enumerate(SELECTED_PACK.mods):
        if mod == mods[choice]: break
    if SELECTED_PACK.mods[i]['project_type'] == 'mod':
        src = os.path.join(paths.get_mods_dir(),SELECTED_PACK.mods[i]['files'][0]['filename'])
    elif SELECTED_PACK.mods[i]['project_type'] == 'resourcepack':
        src = os.path.join(paths.get_rpacks_dir(),SELECTED_PACK.mods[i]['files'][0]['filename'])
    elif SELECTED_PACK.mods[i]['project_type'] == 'shader':
        src = os.path.join(paths.get_shaderpacks_dir(),SELECTED_PACK.mods[i]['files'][0]['filename'])
    
    if not os.path.exists(src):
        SELECTED_PACK.mods.pop(i)
        updateAllPacks()
        return None
    
    dest = paths.get_buffer_dir()
    shutil.move(src,dest)
    SELECTED_PACK.mods.pop(i)
    updateAllPacks()
    
# MAIN COURSE
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    print(f"{Fore.GREEN} removed all contents of {folder_path}")
    
def updateModPack(version):
    global SELECTED_PACK
    print(f"\n{Fore.YELLOW} Removing existing mods")
    clear_folder(paths.get_mods_dir())
    clear_folder(paths.get_rpacks_dir())
    clear_folder(paths.get_shaderpacks_dir())
    print(f"\n{Fore.GREEN} All mods removed successfully")
    
    print(f"\n{Fore.YELLOW} Attempting to update pack {SELECTED_PACK.name}")
    SELECTED_PACK.version = version
    mods = []
    for mod in SELECTED_PACK.mods:
        mods.append(mod["project_id"])
    
    mods = api.getModsBulk(mods)
    
    newmods = []
    for mod in mods:
        newmod = api.get_mod_version(mod,SELECTED_PACK)
        if newmod:
            newmod = newmod[0]
            newmod['project_type'] = mod['project_type']
            newmods.append(newmod)
        else:
            print(f"{Fore.RED}[modpackService] failed to update {mod['title']}")
            newmods.append(mod)
        
    for mod in newmods:
        api.downloadMod(mod)
    SELECTED_PACK.mods = newmods
    updateAllPacks()
    print(f"{Fore.GREEN} updated pack {SELECTED_PACK.name}")
    
    

# TEST
# def moveFilestoBuffer():
# selectModPack("0b55be5d-c878-4d1b-a167-bba0e930dfd5")
# packs = getPacks()
# for pack in packs:
#     print(pack.name)
#     print(pack.version)
#     for mod in pack.mods:
#         print(mod['project_id'],mod['version_number'],sep=" --- ")
#     print("\n")
    
    
SELECTED_PACK = getLastSelectedPack()
# updateAllPacks()
# print(getLastSelectedPack())
# # SELECTED_PACK.mods.append("lol")
# # setLastSelectedPack()
# print(getLastSelectedPack())
# # print(SELECTED_PACK)
# query = input("Enter query: ")
# addModtoSelectedPack(query)
# print(getLastSelectedPack())


# removeModfromSelectedPack()
