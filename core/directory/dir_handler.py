import os
import platform
from core.api import api_handler
from tkinter import Tk, filedialog
from tinydb import TinyDB, Query


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
        
            
def get_modman_folder():
    path=get_mc_folder()
    os.chdir(path)
    try:
        modman_folder=os.path.join(path, "modman")
        os.mkdir(modman_folder)
        return modman_folder
    
    except FileExistsError:
        return modman_folder

def get_mods_folder():
    path=get_mc_folder()
    os.chdir(path)
    try:
        mods_folder=os.path.join(path, "mods")
        os.mkdir(mods_folder)
        return mods_folder
    
    except FileExistsError:
        return mods_folder