class ModPackExistsError(Exception):
    def __init__(self, name):
        super().__init__(f"Modpack '{name}' is already exists.")

class ModPackNotExistsError(Exception):
    def __init__(self, name):
        super().__init__(f"Modpack '{name}' doesn't exist.")

class ModExistsError(Exception):
    def __init__(self, mod_name,pack_name):
        super().__init__(f"Mod '{mod_name}' already exists in {pack_name}.")

class ModNotExistsError(Exception):
    def __init__(self, mod_name,pack_name):
        super().__init__(f"Mod '{mod_name}' do not exist in {pack_name}.")
    def __init__(self, mod_name,path):
        super().__init__(f"Mod '{mod_name}' do not exist at {path}.")
