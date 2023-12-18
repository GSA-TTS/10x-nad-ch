class DataProvider:
    def __init__(self, name: str, id: int = None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'DataProvider {self.id}, {self.name}'


class DataSubmission:
    def __init__(
        self,
        file_name: str,
        url: str,
        provider: DataProvider,
        id: int = None,
    ):
        self.id = id
        self.file_name = file_name
        self.url = url
        self.provider = provider

    def __repr__(self):
        return f'DataSubmission \
            {self.id}, {self.file_name}, {self.url}, {self.provider}'
