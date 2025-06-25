import requests
import os
import platform
from tkinter import Tk, filedialog
from tinydb import TinyDB, Query
import json
    

def search(query):
    # searching and getting list of mods
    url = f"https://api.modrinth.com/v2/search?query={query}"
    response = requests.get(url)
    data = response.json()

    # list of mods searched
    mods=[items for items in data.get("hits",[])]
    return mods

def select_mod(slug,loader,version):
    url=f"https://api.modrinth.com/v2/project/{slug}/version"
    response = requests.get(url)
    data = response.json()
    
    # details of selected mod by loader and version
    mod=[items for items in data if (loader in items["loaders"] and version in items["game_versions"] and items["version_type"]=="release")]
    return mod[0]

def download_mod(mod,folder):
    # got download link
    dl=mod["files"][0]["url"]
    filename=mod["files"][0]["filename"]
    save_path = os.path.join(folder, filename)

    # Downloading the file
    response = requests.get(dl, stream=True)
    if response.status_code == 200 and "java-archive" in response.headers.get("Content-Type", ""):
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"file downloaded successfully at: {folder}")
    else:
            print("Failed. Status:", response.status_code)
            print("Content-Type:", response.headers.get("Content-Type"))
            print("Message:", response.text[:200])
            
def get_mod_folder():
    path = os.path.expanduser("~")
    if platform.system() == "Windows":
        path = os.path.join(path, "AppData", "Roaming", ".minecraft")
    elif platform.system() == "Darwin":  
        path = os.path.join(path, "Library", "Application Support", "minecraft")
    else: 
        path = os.path.join(path, ".minecraft")
    
    if os.path.exists(path):
        return path
    else:
        root = Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory(title="Select your Minecraft folder")
        root.destroy()
        return folder_selected if folder_selected else get_mod_folder()
        
def modman(mc_folder):
    os.chdir(mc_folder)
    try:
        os.mkdir(".\\modman")
    except FileExistsError:
        return
        


if __name__=="__main__":
    
    
    # PHASE: 1.1 COMPLETED
    
    # mod_to_search=str(input("Enter mod name: "))
    # mods=search(mod_to_search)
    # for mod in mods:
    #     print("Mod name:",mod["title"],sep=" ")
    #     print("Author:",mod["author"],sep=" ")
    #     print("Description:",mod["description"],sep=" ")
    #     print("Downloads:",mod["downloads"],sep=" ")
    #     print("Versions: ")
    #     for version in mod["versions"]:
    #         print(version+",",end=" ")
    #     print("\nSlug(for selection):",mod["slug"],sep=" ")
    #     print("\n")
    #     print()
    # mod_slug=str(input("Enter slug of mod to download(case-sensitive): "))
    # mod_loader=str(input("Enter loader(case-sensitive): "))
    # mod_version=str(input("Enter version(case-sensitive): "))
    # mod=select_mod(mod_slug,mod_loader,mod_version)
    # print(json.dumps(mod[0], indent=4))
    # # download_mod(mod)
    
    # PHASE 1.2
    
    #mod man and mods
    mc_folder=get_mod_folder()
    modman(mc_folder)
    mods_folder=os.path.join(mc_folder,"mods")
    modman_folder=os.path.join(mc_folder,"modman")
    
    # ......
    # steps of phase 1
    mod=select_mod("sodium","fabric","1.21.1")
    download_mod(mod,mods_folder)
    mod["active"]=True
    # saving the download history in json file
    while(True):
        if os.path.exists(f"{mods_folder}\\{mod["files"][0]["filename"]}"):
            with TinyDB(os.path.join(modman_folder,"mods.json")) as mods_json:
                mods_json.insert(mod)
                mods_json.close()
            break
        else:
            download_mod(mod,mods_folder)
        
        
        
    
        

    
        