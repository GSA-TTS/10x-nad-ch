class DataProvider:
    def __init__(self, name: str, id: int = None):
        self.id = id
        self.name = name


class DataSubmission:
    def __init__(self, file_path: str, provider: DataProvider, id: int = None):
        self.id = id
        self.file_path = file_path
        self.provider = provider
