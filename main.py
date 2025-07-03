from core.api import api_handler as api
from core.directory import dir_handler as dir
from core.modpack import modpack_handler as mp
from core.modpack import mod_handler as md
import os
import json

if __name__=="__main__":
    
    # PHASE 1.3
    
    # Working
    # mods=api.search('sodium')
    # mod=api.select_mod('sodium','fabric','1.21.2')
    # mp.create_modpack("Performance mods","fabric",'1.21.1')
    # mp.add_mod("Performance mods",mod)
    # rem by name
    # mp.remove_mod("Performance mods","Sodium 0.6.13 for Fabric 1.21.3")
    # mp.remove_mod("Performance mods",mod)
    
    # Testing
    # md.move_to_buffer(filename=2)
    print(os.getcwd())
    dir.change_to_mods_dir()
    
    
    # Trash code
    # mp.delete_modpack("My Pack")
    # l=[]
    # print(len(l))
    
        
        
        
    
        

    
        