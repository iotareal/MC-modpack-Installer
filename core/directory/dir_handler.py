#only creates, and gets directory or file
# and handles ini (paths)
from core.api import api_handler
from tkinter import Tk, filedialog
from tinydb import TinyDB, Query
from core.exceptions import ModPackExceptions as error
import configparser
import os
import platform
# {{{
    
CONFIG_PATH = "config.ini"
SECTION = "paths"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

if not config.has_section(SECTION):
    config.add_section(SECTION)
    
#}}}

def set_path(key, value):
    config.set(SECTION, key, value)
    with open(CONFIG_PATH, "w") as f:
        config.write(f)

def get_path(key):
    return config.get(SECTION, key, fallback=None)


def get_mc_folder():
    path = os.path.expanduser("~")
    if platform.system() == "Windows":
        path = os.path.join(path, "AppData", "Roaming", ".minecraft")
    elif platform.system() == "Darwin":  
        path = os.path.join(path, "Library", "Application Support", "minecraft")
    else: 
        path = os.path.join(path, ".minecraft")
    
    if os.path.exists(path):
        return path
    else:
        Root = Tk()
        Root.withdraw()
        selectedFolder = filedialog.askdirectory(title="Select your Minecraft folder")
        Root.destroy()
        return selectedFolder if selectedFolder else get_mc_folder()
    
def default_dir():
    os.chdir(get_mc_folder())                   
    return

def get_modman_folder():
    path=get_mc_folder()
    try:
        modman_folder=os.path.join(path, "modman")
        os.mkdir(modman_folder)
        return modman_folder
    
    except FileExistsError:
        return modman_folder

def get_mods_folder():
    path=get_mc_folder()
    try:
        mods_folder=os.path.join(path, "mods")
        os.mkdir(mods_folder)
        return mods_folder
    
    except FileExistsError:
        return mods_folder

def change_to_modman_dir():
    os.chdir(get_modman_folder())
    return

def change_to_mods_dir():
    os.chdir(get_mods_folder())      
    return

def create_modpacks_json():
    curr_path=os.getcwd()
    change_to_modman_dir()
    try:
        with open("modpacks.json",'x') as file:
            pass
        os.chdir(curr_path)
        return
    except FileExistsError:
        os.chdir(curr_path)
        return

def create_mods_json():
    curr_path=os.getcwd()
    change_to_modman_dir()
    try:
        with open("mods.json",'x') as file:
            pass
        
        os.chdir(curr_path)
        return
    except FileExistsError:
        os.chdir(curr_path)
        return

def get_buffer_folder():
    path=os.path.join(get_modman_folder(),"buffer")
    if not os.path.exists(path):
        os.mkdir(path)
    return path

 