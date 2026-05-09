import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import requests
import json
import os
from core.directory import paths

# GETTERS
# search by selected pack


def searchProjects(query:str,selected_pack)-> list[dict]:
    loader = selected_pack.loader
    version = selected_pack.version
    return __searchMods(query,version,loader)+__searchShaders(query,version,loader)+__searchResourcepacks(query,version)

def __searchMods(query:str,version:str,loader:str) -> list[dict]:
    url = "https://api.modrinth.com/v2/search"
    
    compatible_categories = [f"categories:{loader}"]
    
    facets = [[f"versions:{version}"],
              ["project_type:mod"],
              compatible_categories
            ]
    
    params = {
        "query" : query.lower(),
        "facets" : json.dumps(facets)
    }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()["hits"]
    except requests.exceptions.RequestException as e:
        print(f"[api] an error occured: {e}")
        return []
        
    
    
def __searchShaders(query:str,version:str,loader:str) -> list[dict]:
    url = "https://api.modrinth.com/v2/search"
    compatibleCategories = []
    
    if loader == 'forge' or loader == 'neoforge':
        compatibleCategories = [
            "categories:optifine"
        ]
    else:
        compatibleCategories = [
            "categories:iris",
            "categories:canvas"
        ]
    facets=[
        [f"versions:{version}"],
        ["project_type:shader"],
        compatibleCategories
    ]
    
    params = {
        "query" : query.lower(),
        "facets" : json.dumps(facets)
    }
    
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()["hits"]
    
    except requests.exceptions.RequestException as e:
        print(f"[api] an error occured: {e}")
        return []

def __searchResourcepacks(query:str,version:str) -> list[dict]:
    url = "https://api.modrinth.com/v2/search"
    compatibleCategories = ["categories:minecraft"]
    
    facets=[
        [f"versions:{version}"],
        ["project_type:resourcepack"],
        compatibleCategories
    ]
    
    params = {
        "query" : query.lower(),
        "facets" : json.dumps(facets)
    }
    
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()["hits"]
    
    except requests.exceptions.RequestException as e:
        print(f"[api] an error occured: {e}")
        return []
    
def get_mod_version(mod,selected_pack):
    if mod['id']:
        url = f"https://api.modrinth.com/v2/project/{mod['id']}/version"
    else:
        url = f"https://api.modrinth.com/v2/project/{mod['project_id']}/version"
        
    
    if mod['project_type'] not in ['shader','resourcepack']:
        params = {
            "game_versions" : json.dumps([selected_pack.version]),
            "loaders" : json.dumps([selected_pack.loader]),
        }
    else:
        params = {
            "game_versions" : json.dumps([selected_pack.version])
        }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)
        return []

def getModsBulk(modids):
    url = "https://api.modrinth.com/v2/projects"
    params = {
         'ids': json.dumps(modids)
    }
    
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[api] an error occured: {e}")
        return []

def downloadMod(mod):
    file = mod['files'][0]
    # Create the full path for the file.
    if mod['project_type'] == 'shader':
        save_path = os.path.join(paths.get_shaderpacks_dir(), file['filename'])
    elif mod['project_type'] == 'resourcepack':
        save_path = os.path.join(paths.get_rpacks_dir(), file['filename'])
    elif mod['project_type'] == 'mod':
        save_path = os.path.join(paths.get_mods_dir(), file['filename'])
    else:
        save_path = os.path.join(paths.get_buffer_dir(), file['filename'])

    if os.path.exists(save_path):
        print("[api-service] mod already exists")
        return
    # Stream the download.
    response = requests.get(file['url'], stream=True)
    response.raise_for_status()  # Raises an error for bad responses.

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive chunks
                file.write(chunk)

    print(f"[api-service] downloaded file saved to {save_path}")

def downloadModLatest(mod):
    file = mod[0]['files'][0]
    # Create the full path for the file.
    if mod['project_type'] == 'shader':
        save_path = os.path.join(paths.get_shaderpacks_dir(), file['filename'])
    elif mod['project_type'] == 'resourcepack':
        save_path = os.path.join(paths.get_rpacks_dir(), file['filename'])
    elif mod['project_type'] == 'mod':
        save_path = os.path.join(paths.get_mods_dir(), file['filename'])
    else:
        save_path = os.path.join(paths.get_buffer_dir(), file['filename'])

    if os.path.exists(save_path):
        print("[api-service] mod already exists")
        return
    # Stream the download.
    response = requests.get(file['url'], stream=True)
    response.raise_for_status()  # Raises an error for bad responses.

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive chunks
                file.write(chunk)

    print(f"[api-service] downloaded file saved to {save_path}")
# DEPRECATED

# # seach by query and version NO USAGE
# def search_mods(query:str,version,loader) -> list[dict]:
#     url = "https://api.modrinth.com/v2/search"
    
#     facets = [[f"versions:{version}"],
#               [f"categories : {loader}"]
#             ]
    
#     params = {
#         "query" : query,
#         "facets" : json.dumps(facets)
#     }
#     try:
#         response = requests.get(url,params=params)
#         response.raise_for_status()
#         return response.json()["hits"]
#     except requests.exceptions.RequestException as e:
#         print(f"[api] an error occured: {e}")
#         return []
    
# def get_mod(id:str,selected_pack):
#     url = f"https://api.modrinth.com/v2/project/{id}"
#     params = {
#         "game_versions" : json.dumps([selected_pack["minecraft_version"]]),
#         "loaders" : json.dumps([selected_pack["loader"]])
#     }
#     try:
#         response = requests.get(url,params=params)
#         response.raise_for_status()
#         response = response.json()
#         response['versions'].clear()
#         return response
#     except Exception as e:
#         print(e)
#         return []

    
# def get_bulk_mods(project_ids:list[str]) -> list[dict]:
#     url = "https://api.modrinth.com/v2/projects"
#     params = {
#         'ids': json.dumps(project_ids)
#     }
#     try:
#         response = requests.get(url,params=params)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"[api] an error occured: {e}")
#         return []

# def get_latest_mod_version(id:str,version:str,loader:str) -> dict:
#     url = f"https://api.modrinth.com/v2/project/{id}/version"
#     params = {
#         "game_versions" : json.dumps([version]),
#         "loaders" : json.dumps([loader])
#     }
#     try:
#         response = requests.get(url,params=params)
#         response.raise_for_status()
#         return response.json()[0]
#     except Exception as e:
#         print(e)
#         return []
