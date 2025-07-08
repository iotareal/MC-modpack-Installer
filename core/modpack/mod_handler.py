# CRUD ops on mods, handle mod centric api requests
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from tinydb import TinyDB, Query
import os
# from core.mods_ops import ensure_mod_available, set_mod_active
import shutil
import requests

###{
ModPack = Query()
###}

