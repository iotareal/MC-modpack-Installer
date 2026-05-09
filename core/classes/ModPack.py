import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from dataclasses import dataclass, field, asdict
import uuid

@dataclass
class ModPack:
    id:str = field(default_factory = lambda:str(uuid.uuid4()))
    name:str = ""
    loader:str = ""
    version:str = ""
    active:bool = False
    mods:list = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)
    
    def __getitem__(self,key):
        return self.to_dict()[key]