from typing import List, Optional
from pydantic import BaseModel

class Modpack(BaseModel):
    """Defines the data structure for a modpack entity."""
    
    # Optional because TinyDB assigns it after insertion
    id: Optional[int] = None 
    
    # Field provides extra validation, like ensuring name is lowercase
    name: str
    
    minecraft_version: str
    loader: str
    active: bool = False
    
    # A list that will hold the unique string IDs of the mods
    mods: List[str] = []