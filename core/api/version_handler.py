import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import random
import requests
import pickle
import time
import os
import re

def update_supported_lists(save_path="versions.pkl",max_age_seconds=28800,force=False):
    try:
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

        print("\nconfig: 'versions.pkl' updated")
    except Exception as e:
        print("\nconfig: 'versions.pkl' failed to update",e)

update_supported_lists()
# version getters
def get_all_versions():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported["all_versions"]
    
def get_release_versions():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['release_versions']

def get_snapshots():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['snapshots']

def get_betas():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['betas']

def get_alphas():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['alphas']

def get_rcs():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['rcs']

def get_pre_releases():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['pre_releases']

def get_others():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['others']

def get_loaders():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['loaders']

def get_latest_release():
    update_supported_lists(force=True)
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['release_versions'][0]

def get_latest_snapshot():
    update_supported_lists(force=True)
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    return supported['snapshots'][0]

def get_random_loader():
    with open("versions.pkl",'rb') as file:
        supported=pickle.load(file)
    idx = random.randint(0,len(supported["loaders"])-1)
    return supported["loaders"][idx]