import requests
import pickle
import os

def search(name):
    # searching and getting list of mods
    url = f"https://api.modrinth.com/v2/search?query={name}"
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
            
def get_mods_bulk(slug_list):
    url = "https://api.modrinth.com/v2/projects"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=slug_list, headers=headers)
    if response.status_code == 200:
        data = response.json()
        mods=[items for items in data.get("hits",[])]
        return mods
    else:
        print("Error:", response.status_code)
        print("Response:", response.text)
        return
    
def update_supported_lists(save_path="core/api/supported.pkl"):
    try:
        game_versions = requests.get("https://api.modrinth.com/v2/tag/game_version").json()
        loaders = requests.get("https://api.modrinth.com/v2/tag/loader").json()

        supported = {
            "versions": sorted([v["version"] for v in game_versions]),
            "loaders": sorted([l["name"] for l in loaders])
        }

        with open(save_path, "wb") as f:
            pickle.dump(supported, f)

        print("✅ Binary-supported list saved successfully!")
    except Exception as e:
        print("❌ Failed to update supported list:", e)