from dataclasses import dataclass

@dataclass
class Mod:
    slug: str
    version: str
    loader: str
    url: str
    filename: str
    active: bool = True