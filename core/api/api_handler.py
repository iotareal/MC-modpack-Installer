# Handles api requests to show in frontend
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.modpack import modpack_handler as mdpck
from core.directory import Paths as dir
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

def get_manipulated_response(slug: str, mc_version: str) -> dict | None:
     # Endpoint to get a list of all versions for a project
    url = f"https://api.modrinth.com/v2/project/{slug}/version"
    
    # Parameters to filter the versions returned by the API
    params = {
        'game_versions': f'["{mc_version}"]'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        versions_list = response.json()
        
        # If the list is empty, no compatible version was found
        if not versions_list:
            print(f"Info: No version of '{slug}' found for Minecraft {mc_version}.")
            return None
            
        # The API returns versions sorted by creation date, so the first
        # item is the newest compatible version.
        latest_version_data = versions_list[0]
        
        # --- Manipulation Logic ---
        project_type = latest_version_data.get('project_type')
        loaders = latest_version_data.get('loaders', [])
        
        classification = "unknown"
        if project_type == 'mod':
            if 'datapack' in loaders:
                classification = "datapack"
            else:
                classification = "mod"
        elif project_type == 'resourcepack':
            classification = "resourcepack"
        elif project_type == 'shader':
            classification = "shader"
            
        # Add the new 'type' key to the dictionary
        latest_version_data['type'] = classification
        
        return latest_version_data

    except requests.exceptions.HTTPError as err:
        print(f"Error fetching '{slug}': Not Found or API error (Status: {err.response.status_code})")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: A network problem occurred: {e}")
        return None
    
