class ModFileNotExistsError(Exception):
    def __init__(self, filename):
        super().__init__(f"file '{filename}' not found.")