from dataclasses import dataclass


@dataclass
class File:
    name: str
    content: str


@dataclass
class FileMetadata:
    name: str
    size: int
