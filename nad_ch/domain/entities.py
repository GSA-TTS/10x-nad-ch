from datetime import datetime, timezone, UTC
import json
import os
import re
from typing import Optional, Dict


class Entity:
    def __init__(self, id: Optional[int] = None):
        self.id = id
        self.created_at: datetime = None
        self.updated_at: datetime = None

    def set_created_at(self, created_at: datetime):
        self.created_at = created_at

    def set_updated_at(self, updated_at: datetime):
        self.updated_at = updated_at


class DataProducer(Entity):
    def __init__(self, name: str, id: Optional[int] = None):
        super().__init__(id)
        self.name = name

    def __repr__(self):
        return f"DataProducer {self.id}, {self.name})"


class ColumnMap(Entity):
    required_fields = [
        "Add_Number",
        "AddNo_Full",
        "St_Name",
        "StNam_Full",
        "County",
        "Inc_Muni",
        "Post_City",
        "State",
        "UUID",
        "AddAuth",
        "Longitude",
        "Latitude",
        "NatGrid",
        "Placement",
        "AddrPoint",
        "DateUpdate",
        "NAD_Source",
        "DataSet_ID",
    ]

    def __init__(
        self,
        name: str,
        producer: DataProducer,
        mapping: Dict[str, str] = {},
        version_id: Optional[int] = None,
        id: Optional[int] = None,
    ):
        super().__init__(id)
        self.name = name
        self.producer = producer
        self.mapping = mapping
        self.version_id = version_id

    def __repr__(self):
        return f"ColumnMap {self.id}, {self.name})"

    def is_valid(self) -> bool:
        # The mapping must not be empty
        if not len(self.mapping):
            return False

        # The mapping must contain all required fields and they must not be empty
        if not all(
            field in self.mapping and self.mapping[field] for field in ColumnMap.required_fields
        ):
            return False

        return True


class DataSubmission(Entity):
    def __init__(
        self,
        filename: str,
        producer: DataProducer,
        column_map: ColumnMap,
        report: Optional[Dict[any, any]] = None,
        id: Optional[int] = None,
    ):
        super().__init__(id)
        self.filename = filename
        self.producer = producer
        self.column_map = column_map
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


class User(Entity):
    def __init__(self, email, login_provider, logout_url, id: int = None):
        super().__init__(id)
        self.email = email
        self.login_provider = login_provider
        self.logout_url = logout_url

    # The following property definitions and get_id method are required in order for the
    # Flask-Login library to be able to handle instances of the User domain entity.
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self) -> str:
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def __repr__(self):
        return f"User {self.id}, {self.email})"
