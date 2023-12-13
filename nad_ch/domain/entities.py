class DataProvider:
    def __init__(self, name: str):
        self.name = name


class DataSubmission:
    def __init__(self, file_path: str, provider: DataProvider):
        self.file_path = file_path
        self.provider = provider
