import datetime
import os
import re


class Entity:
    def __init__(self, id: int = None):
        self.id = id
        self.created_at = None
        self.updated_at = None

    def set_created_at(self, created_at):
        self.created_at = created_at

    def set_updated_at(self, updated_at):
        self.updated_at = updated_at


class DataProvider(Entity):
    def __init__(self, name: str, id: int = None):
        super().__init__(id)
        self.name = name

    def __repr__(self):
        return f"DataProvider {self.id}, {self.name} \
            (created: {self.created_at}; updated: {self.updated_at})"


class DataSubmission(Entity):
    def __init__(
        self,
        filename: str,
        provider: DataProvider,
        id: int = None,
    ):
        super().__init__(id)
        self.filename = filename
        self.provider = provider

    def __repr__(self):
        return f"DataSubmission \
            {self.id}, {self.filename}, {self.provider} \
                (created: {self.created_at}; updated: {self.updated_at})"

    @staticmethod
    def generate_filename(file_path: str, provider: DataProvider) -> str:
        s = re.sub(r"\W+", "_", provider.name)
        s = s.lower()
        s = s.strip("_")
        formatted_provider_name = re.sub(r"_+", "_", s)
        datetime_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        _, file_extension = os.path.splitext(file_path)
        filename = f"{formatted_provider_name}_{datetime_str}{file_extension}"
        return filename
