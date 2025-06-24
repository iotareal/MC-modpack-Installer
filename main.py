import requests
import os

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
    return mod
def download_mod(mod):
# got download link
    dl=mod[0]["files"][0]["url"]
    filename=mod[0]["files"][0]["filename"]

    # Choose the folder to save in
    folder = "d:\\Stuff\\Random Projects Stuff\\[Python] MC modpack Installer\\Downloaded"
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

if __name__=="__main__":
    mod_to_search=str(input("Enter mod name: "))
    mods=search(mod_to_search)
    for mod in mods:
        print("Mod name:",mod["title"],sep=" ")
        print("Author:",mod["author"],sep=" ")
        print("Description:",mod["description"],sep=" ")
        print("Downloads:",mod["downloads"],sep=" ")
        print("Versions: ")
        for version in mod["versions"]:
            print(version+",",end=" ")
        print("Slug(for selection):",mod["slug"],sep=" ")
        print("\n")
        print()
    mod_slug=str(input("Enter slug of mod to download(case-sensitive): "))
    mod_loader=str(input("Enter loader(case-sensitive): "))
    mod_version=str(input("Enter version(case-sensitive): "))
    mod=select_mod(mod_slug,mod_loader,mod_version)
    download_mod(mod)
    
        
        