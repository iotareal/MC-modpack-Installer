class ModPackExistsError(Exception):
    def __init__(self, name):
        super().__init__(f"Modpack '{name}' is already active.")

class ModPackNotExistsError(Exception):
    def __init__(self, name):
        super().__init__(f"Modpack '{name}' doesn't exist.")

class ModExistsError(Exception):
    def __init__(self, mod_name,pack_name):
        super().__init__(f"Mod '{mod_name}' already exist in {pack_name}.")