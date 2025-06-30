from core.api import api_handler as api
from core.directory import dir_handler as dir
import os
import json

if __name__=="__main__":
    
    
    # PHASE: 1.1 COMPLETED
    
    # mod_to_search=str(input("Enter mod name: "))
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
    
    # # PHASE 1.2 COMPLETED
    # # ...... PHASE 1 steps
    mods=api.search("sodium")
    mod=api.select_mod("sodium","fabric","1.21.1")
    # print(json.dumps(mod, indent=4))
    print("Mod name:",mod["name"],sep=" ")
    print("Downloads:",mod["downloads"],sep=" ")
    print("Versions: ")
    for version in mod["versions"]:
        print(version+",",end=" ")
    
    # PHASE 1.3
    
        
        
        
    
        

    
        