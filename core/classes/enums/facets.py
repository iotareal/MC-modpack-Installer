from core.api import version_handler as ver
from enum import Enum

class ProjectType(Enum):
    mod = "mod"
    resource_pack = "resource_pack"
    data_pack = "data_pack"
    shader = "shader"
    plugin =  "plugin"

class Categories(Enum):
    adventure = "adventure"
    cursed = "cursed"
    decoration = "decoration"
    economy = "economy"
    equipment = "equipment"
    food = "food"
    game_mechanics = "game_mechanics"
    library = "library"
    magic = "magic"
    management = "management"
    minigame = "minigame"
    mobs = "mobs"
    optimization = "optimization" 
    social = "social"
    storage = "storage"
    technology = "technology"
    transportation = "transportation"
    utility = "utility"
    world_generation = "world_generation"


    

