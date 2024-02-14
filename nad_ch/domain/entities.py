from datetime import datetime, timezone, UTC
import os
import re


class Entity:
    def __init__(self, id: int = None):
        self.id = id
        self.created_at: datetime = None
        self.updated_at: datetime = None

    def set_created_at(self, created_at: datetime):
        self.created_at = created_at

    def set_updated_at(self, updated_at: datetime):
        self.updated_at = updated_at


class DataProducer(Entity):
    def __init__(self, name: str, id: int = None):
        super().__init__(id)
        self.name = name

    def __repr__(self):
        return f"DataProducer {self.id}, {self.name})"


class DataSubmission(Entity):
    def __init__(
        self,
        filename: str,
        producer: DataProducer,
        report=None,
        id: int = None,
    ):
        super().__init__(id)
        self.filename = filename
        self.producer = producer
        self.report = report

    def __repr__(self):
        return f"DataSubmission \
            {self.id}, {self.filename}, {self.producer}"

    @staticmethod
    def generate_filename(file_path: str, producer: DataProducer) -> str:
        s = re.sub(r"\W+", "_", producer.name)
        s = s.lower()
        s = s.strip("_")
        formatted_producer_name = re.sub(r"_+", "_", s)

        current_time_utc = datetime.now(timezone.utc)
        timestamp = current_time_utc.timestamp()
        datetime_obj = datetime.fromtimestamp(timestamp, UTC)
        datetime_str = datetime_obj.strftime("%Y%m%d_%H%M%S")

        _, file_extension = os.path.splitext(file_path)
        filename = f"{formatted_producer_name}_{datetime_str}{file_extension}"
        return filename

    def has_report(self) -> bool:
        return self.report is not None
