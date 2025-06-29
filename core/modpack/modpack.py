import os
import json

MODPACK_FILE = os.path.join(os.getcwd(), "modpacks.json")

# Utility to load the JSON file
def load_modpacks():
    if not os.path.exists(MODPACK_FILE):
        return {"active": None, "modpacks": []}
    with open(MODPACK_FILE, "r") as f:
        return json.load(f)

# Utility to save the JSON file
def save_modpacks(data):
    with open(MODPACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Create a new modpack
def create_modpack(name):
    data = load_modpacks()
    if any(mp["name"] == name for mp in data["modpacks"]):
        print(f"Modpack '{name}' already exists.")
        return
    data["modpacks"].append({"name": name, "mods": []})
    save_modpacks(data)
    print(f"Modpack '{name}' created.")

# Add a mod to a modpack
def add_mod_to_pack(pack_name, mod_data):
    data = load_modpacks()
    for mp in data["modpacks"]:
        if mp["name"] == pack_name:
            # Prevent duplicates by slug + version
            if not any(m["slug"] == mod_data["slug"] and m["version"] == mod_data["version"] for m in mp["mods"]):
                mod_data["downloaded"] = False  # Track download state
                mp["mods"].append(mod_data)
                save_modpacks(data)
                print(f"Added '{mod_data['slug']}' to modpack '{pack_name}'")
            else:
                print("Mod already exists in the pack.")
            return
    print(f"Modpack '{pack_name}' not found.")

# Activate a modpack
def set_active_modpack(name):
    data = load_modpacks()
    if not any(mp["name"] == name for mp in data["modpacks"]):
        print(f"Modpack '{name}' does not exist.")
        return
    data["active"] = name
    save_modpacks(data)
    print(f"'{name}' is now the active modpack.")

# Prune mods (delete downloads, keep list)
def prune_modpack(name):
    data = load_modpacks()
    for mp in data["modpacks"]:
        if mp["name"] == name:
            for mod in mp["mods"]:
                mod["downloaded"] = False
            save_modpacks(data)
            print(f"Pruned downloaded mods from '{name}'.")
            return
    print(f"Modpack '{name}' not found.")

# Delete a modpack
def delete_modpack(name):
    data = load_modpacks()
    data["modpacks"] = [mp for mp in data["modpacks"] if mp["name"] != name]
    if data["active"] == name:
        data["active"] = None
    save_modpacks(data)
    print(f"Deleted modpack '{name}'.")

# List modpacks
def list_modpacks():
    data = load_modpacks()
    for mp in data["modpacks"]:
        print(f"📦 {mp['name']} ({len(mp['mods'])} mods){' [ACTIVE]' if mp['name'] == data['active'] else ''}")
