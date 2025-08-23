#only creates, and gets directory or file
# and handles ini (paths)
from tkinter import Tk, filedialog
from tinydb import TinyDB, Query
import configparser
import os
import platform
# {{{
    
CONFIG_INI = "config.ini"
SECTION = "paths"
    
#}}}

def safe_get(config_path,section=SECTION):
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            f.write("")
            
    if not config.has_section(section):
        config.add_section(section)
    
    config.read(CONFIG_INI)
    return config

def set_value(key, value):
    config=safe_get(CONFIG_INI)
    config.set(SECTION, key, value)
    with open(CONFIG_INI, "w") as f:
        config.write(f)
    print(f"config: in '{SECTION}' written {key} = {value}")

def get_path(key):
    config=safe_get(CONFIG_INI)
    if config.has_section(SECTION):
        return config.get(SECTION, key, fallback=None)
    else:
        return False 

def get_mc_dir():
    path=get_path("MC_DIR")
    if path and os.path.exists(path):
        return path
    
    path = os.path.expanduser("~")
    if platform.system() == "Windows":
        path = os.path.join(path, "AppData", "Roaming", ".minecraft")
    elif platform.system() == "Darwin":  
        path = os.path.join(path, "Library", "Application Support", "minecraft")
    else: 
        path = os.path.join(path, ".minecraft")
    
    if os.path.exists(path):
        set_value("MC_DIR",path)
        return path
    
    else:
        Root = Tk()
        Root.withdraw()
        selectedFolder = filedialog.askdirectory(title="Select your Minecraft folder")
        Root.destroy()
        if selectedFolder:
            set_value("MC_DIR",selectedFolder)
            return selectedFolder  
        else: 
            get_mc_dir()
    
def get_modman_dir():
    path=get_path("MODMAN_DIR")
    if path and os.path.exists(os.path.join(get_mc_dir(),"modman")):
        return path
    
    path=os.path.join(get_mc_dir(),"modman")
    if not os.path.exists(path):
        os.makedirs(path)
        
    set_value("MODMAN_DIR",path)
    return path 

def get_mods_dir():
    path=get_path("MODS_DIR")
    if path and os.path.exists(os.path.join(get_mc_dir(),"mods")):
        return path
    
    path=os.path.join(get_mc_dir(),"mods")
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"dir: 'mods' made at {get_mc_dir()}")
        
    set_value("MODS_DIR",path)
    return path

def get_rpacks_dir():
    path=get_path("RPACKS_DIR")
    if path and os.path.exists(os.path.join(get_mc_dir(),"resourcepacks")):
        return path
    
    path=os.path.join(get_mc_dir(),"resourcepacks")
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"dir: 'resourcepacks' made at {get_mc_dir()}")
        
    set_value("RPACKS_DIR",path)
    return path

def get_shaderpacks_dir():
    path=get_path("SHADERPCKS_DIR")
    path=get_path("BUFFER_DIR")
    if path and os.path.exists(os.path.join(get_mc_dir(),"shaderpacks")):
        return path
    
    path=os.path.join(get_mc_dir(),"shaderpacks")
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"dir: 'shaderpacks' made at {get_mc_dir()}")
        
    set_value("SHADERPCKS_DIR",path)
    return path

def get_buffer_dir():
    path=get_path("BUFFER_DIR")
    if path and os.path.exists(os.path.join(get_modman_dir(),"buffer")):
        return path
    
    path=os.path.join(get_modman_dir(),"buffer")
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"dir: 'buffer' made at {get_modman_dir()}")
        
    set_value("BUFFER_DIR",path)
    return path

def get_modpacks_json():
    path=get_path("MODPACKS_JSON")
    if path and os.path.exists(path):
        return path
    
    path=os.path.join(get_modman_dir(),"modpacks.json")
    if not os.path.exists(path):
        with open(path,'x') as file:
            pass
        print(f"dir: file 'modpacks.json' created at {get_modman_dir()}")
        
    set_value("MODPACKS_JSON",path)
    return path

def get_mods_json():
    path=get_path("MODS_JSON")
    if path and os.path.exists(path):
        return path
    
    path=os.path.join(get_modman_dir(),"mods.json")
    if not os.path.exists(path):
        with open(path,'x') as file:
            pass
        print(f"dir: file 'mods.json' created at {get_modman_dir()}")
        
    set_value("MODS_JSON",path)
    return path

