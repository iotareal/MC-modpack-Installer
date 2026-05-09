class VersionNotFoundError(Exception):
    def __init__(self, version):
        super().__init__(f"version:'{version}' is invalid")
        
class LoaderNotFoundError(Exception):
    def __init__(self, loader):
        super().__init__(f"loader:'{loader}' is invalid")