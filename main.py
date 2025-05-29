import requests
import json

with open("mods.json","r") as f:
    mod_list=json.load(f)
for mod in mod_list:
    print(mod["slug"])
# mod_id = "AANobbMI"  # Replace with your mod's project ID
# url = f"https://api.modrinth.com/v2/project/{mod_id}"

# response = requests.get(url)
# data = response.json()

# print(data["slug"])