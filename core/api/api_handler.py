# Handles api requests to show in frontend
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.modpack import modpack_handler as mdpck
from core.directory import dir_handler as dir
from core.classes.enums import facets
from core.classes.Filters import Filters
import requests
import os
FILTER = Filters()
def set_perma_filter():
    modpack = mdpck.get_active()
    FILTER.add_filter("categories", modpack['loader'])
    FILTER.add_filter("versions",modpack['version'])
    
def search(name):
    # searching and getting list of mods
    set_perma_filter()
    url = f"https://api.modrinth.com/v2/search?q={name}&f={FILTER}"
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
    mod=[items for items in data if (version in items["game_versions"] and items["version_type"]=="release")]
    return mod[0]

def download_mod(mod):
    # got download link
    dl = mod["files"][0]["url"]
    filename = mod["files"][0]["filename"]
    save_path = os.path.join(dir.get_buffer_dir(), filename)

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


    
