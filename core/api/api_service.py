import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.exceptions import VersionExceptions as err
import random
import requests
import pickle
import time
import json
import os
import re
VERSION_FILE = "versions.pkl"
def update_supported_lists(save_path=VERSION_FILE,max_age_seconds=28800,force=False):
    try:
        if not os.path.exists(save_path):
            with open(VERSION_FILE,'x') as _:
                pass
        if os.path.exists(save_path) or not force:
            last_modified = os.path.getmtime(save_path)
            if time.time() - last_modified < max_age_seconds:
                return
        game_versions = requests.get("https://api.modrinth.com/v2/tag/game_version").json()
        loaders = requests.get("https://api.modrinth.com/v2/tag/loader").json()
        
        release_versions = []
        snapshots = []
        betas = []
        alphas = []
        rcs = []
        pre_releases = []
        others = []

        for v in game_versions:
            version_str = v["version"] if isinstance(v, dict) and "version" in v else v
            if re.match(r'^\d+\.\d+(\.\d+)?$', version_str):
                release_versions.append(version_str)
            elif re.match(r'^\d{2}w\d{2}[a-z]$', version_str):
                snapshots.append(version_str)
            elif re.match(r'^b\d', version_str):
                betas.append(version_str)
            elif re.match(r'^a\d', version_str):
                alphas.append(version_str)
            elif 'rc' in version_str:
                rcs.append(version_str)
            elif 'pre' in version_str:
                pre_releases.append(version_str)
            else:
                others.append(version_str)

        supported = {
            "all_versions" : sorted((v["version"] for v in game_versions if "version" in v), reverse=True),
            "release_versions" : tuple(release_versions),
            "snapshots" : tuple(snapshots),
            "betas" : tuple(betas),
            "alphas" : tuple(alphas),
            "rcs" : tuple(rcs),
            "pre_releases" : tuple(pre_releases),
            "others" :tuple(others),
            "loaders": sorted((l["name"] for l in loaders),reverse=True)
        }

        with open(save_path, "wb") as f:
            pickle.dump(supported, f)

        print("\n[api] 'versions.pkl' updated")
    except Exception as e:
        print("\n[api] 'versions.pkl' failed to update",e)

update_supported_lists()
# version getters
def get_all_versions():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported["all_versions"]
    
def get_release_versions():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['release_versions']

def get_snapshots():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['snapshots']

def get_betas():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['betas']

def get_alphas():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['alphas']

def get_rcs():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['rcs']

def get_pre_releases():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['pre_releases']

def get_others():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['others']

def get_loaders():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['loaders']

def get_latest_release():
    update_supported_lists(force=True)
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['release_versions'][0]

def get_latest_snapshot():
    update_supported_lists(force=True)
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    return supported['snapshots'][0]

def get_random_loader():
    with open(VERSION_FILE,'rb') as file:
        supported=pickle.load(file)
    idx = random.randint(0,len(supported["loaders"])-1)
    return supported["loaders"][idx]

def validate_version(version:str) -> None:
    versions = get_all_versions()
    if version.casefold() not in versions:
        raise err.VersionNotFoundError(version)

def validate_loader(loader:str) -> None:
    loaders = get_loaders()
    if loader.casefold() not in loaders:
        raise err.LoaderNotFoundError(loader)

# GETTERS
# search by selected pack
def search_mods(query:str,selected_pack) -> list[dict]:
    url = "https://api.modrinth.com/v2/search"
    
    facets = [[f"versions:{selected_pack["minecraft_version"]}"],
              [f"categories : {selected_pack["loader"]}"]
            ]
    
    params = {
        "query" : query,
        "facets" : json.dumps(facets)
    }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()["hits"]
    except requests.exceptions.RequestException as e:
        print(f"[api] an error occured: {e}")
        return []

# seach by query and version NO USAGE
def search_mods(query:str,version,loader) -> list[dict]:
    url = "https://api.modrinth.com/v2/search"
    
    facets = [[f"versions:{version}"],
              [f"categories : {loader}"]
            ]
    
    params = {
        "query" : query,
        "facets" : json.dumps(facets)
    }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()["hits"]
    except requests.exceptions.RequestException as e:
        print(f"[api] an error occured: {e}")
        return []
    
def get_mod(id:str,selected_pack):
    url = f"https://api.modrinth.com/v2/project/{id}"
    params = {
        "game_versions" : json.dumps([selected_pack["minecraft_version"]]),
        "loaders" : json.dumps([selected_pack["loader"]])
    }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        response = response.json()
        response['versions'].clear()
        return response
    except Exception as e:
        print(e)
        return []

def get_mod_version(id:str,selected_pack):
    url = f"https://api.modrinth.com/v2/project/{id}/version"
    params = {
        "game_versions" : json.dumps([selected_pack["minecraft_version"]]),
        "loaders" : json.dumps([selected_pack["loader"]])
    }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)
        return []
    
def get_bulk_mods(project_ids:list[str]) -> list[dict]:
    url = "https://api.modrinth.com/v2/projects"
    params = {
        'ids': json.dumps(project_ids)
    }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[api] an error occured: {e}")
        return []

def get_latest_mod_version(id:str,version:str,loader:str) -> dict:
    url = f"https://api.modrinth.com/v2/project/{id}/version"
    params = {
        "game_versions" : json.dumps([version]),
        "loaders" : json.dumps([loader])
    }
    try:
        response = requests.get(url,params=params)
        response.raise_for_status()
        return response.json()[0]
    except Exception as e:
        print(e)
        return []
