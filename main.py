from core.api import api_handler as api
from core.directory import dir_handler as dir
from core.modpack import modpack as mp
import os
import json

if __name__=="__main__":
    
    
    # PHASE: 1.1 EXEMPTED
    
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
    
    # PHASE 1.2 EXEMPTED
    # PHASE 1.3
    
    # mods=api.search('sodium')
    # mod=api.select_mod('sodium','fabric','1.21.2')
    
    # mp.create_modpack("My Pack2","fabric",'1.21.1') # :D:D:D
    # mp.set_active("My Pack") # :D:D:D
    # mp.add_mod("My Pack",mod) # :D:D:D
    # mp.remove_mod("My Pack",mod) # :D:D:D
    
    
    # mp.rename_packname("Regular","My Pack") # :D:D:D
    # modpacks=mp.list_of_all_modpacks() #:D:D:D
    # for packs in modpacks:
    #     print(f"Name: {packs['name']}")
    #     print(f"Active: {packs['active']}")
    #     print('\n')
    
    mp.prettify_modpack_file()
    
    
    
    
    
    
    
    
    # mp.delete_modpack("My Pack")
    # print(json.dumps(mod, indent=4))
    # l=[]
    # print(len(l))
    
        
        
        
    
        

    
        