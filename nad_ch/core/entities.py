from datetime import datetime, timezone, UTC
from enum import Enum
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
    all_fields = [
        "AddNum_Pre",
        "Add_Number",
        "AddNum_Suf",
        "AddNo_Full",
        "St_PreMod",
        "St_PreDir",
        "St_PreTyp",
        "St_PreSep",
        "St_Name",
        "St_PosTyp",
        "St_PosDir",
        "St_PosMod",
        "StNam_Full",
        "Building",
        "Floor",
        "Unit",
        "Room",
        "Seat",
        "Addtl_Loc",
        "SubAddress",
        "LandmkName",
        "County",
        "Inc_Muni",
        "Post_City",
        "Census_Plc",
        "Uninc_Comm",
        "Nbrhd_Comm",
        "NatAmArea",
        "NatAmSub",
        "Urbnztn_PR",
        "PlaceOther",
        "PlaceNmTyp",
        "State",
        "Zip_Code",
        "Plus_4",
        "UUID",
        "AddAuth",
        "AddrRefSys",
        "Longitude",
        "Latitude",
        "NatGrid",
        "Elevation",
        "Placement",
        "AddrPoint",
        "Related_ID",
        "RelateType",
        "ParcelSrc",
        "Parcel_ID",
        "AddrClass",
        "Lifecycle",
        "Effective",
        "Expire",
        "DateUpdate",
        "AnomStatus",
        "LocatnDesc",
        "Addr_Type",
        "DeliverTyp",
        "NAD_Source",
        "DataSet_ID",
    ]

    required_fields = [
        "Add_Number",
        "St_Name",
        "St_PosTyp",
        "Unit",
        "Inc_Muni",
        "Post_City",
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
        return all(
            field in self.mapping and self.mapping[field] not in (None, "")
            for field in ColumnMap.required_fields
        )


class DataSubmissionStatus(Enum):
    PENDING_SUBMISSION = "PENDING_SUBMISSION"
    CANCELED = "CANCELED"
    PENDING_VALIDATION = "PENDING_VALIDATION"
    FAILED = "FAILED"
    VALIDATED = "VALIDATED"


class DataSubmission(Entity):
    def __init__(
        self,
        name: str,
        file_path: str,
        status: DataSubmissionStatus,
        producer: DataProducer,
        column_map: ColumnMap,
        report: Optional[Dict[any, any]] = None,
        id: Optional[int] = None,
    ):
        super().__init__(id)
        self.name = name
        self.file_path = file_path
        self.status = (
            status if status is not None else DataSubmissionStatus.PENDING_SUBMISSION
        )
        self.producer = producer
        self.column_map = column_map
        self.report = report

    def __repr__(self):
        return f"DataSubmission \
            {self.id}, , {self.name}, {self.file_path}, {self.producer}, {self.status}"

    @staticmethod
    def generate_file_path(file_path: str, producer: DataProducer) -> str:
        return os.path.basename(file_path)

    def get_mapped_data_dir(
        self, source_path: str, base_path: str, remote: bool = False
    ) -> str:
        file_path, _ = os.path.splitext(
            self.generate_file_path(source_path, self.producer)
        )
        if remote:
            # Defines the path for remote storage such as s3
            partition_dt = datetime.today().strftime("%Y_%m_%d")
            path = f"data_submissions/{self.producer.name}/{partition_dt}/{file_path}"
        else:
            # Defines the path for local storage of post-mapped data
            path = os.path.join(base_path, f"data_submissions/{self.id}/{file_path}")
        return path

    @staticmethod
    def generate_zipped_file_path(name: str, producer: DataProducer) -> str:
        s = re.sub(r"\W+", "_", producer.name)
        s = s.lower()
        s = s.strip("_")
        formatted_producer_name = re.sub(r"_+", "_", s)

        s = re.sub(r"\W+", "_", name)
        s = s.lower()
        s = s.strip("_")
        formatted_name = re.sub(r"\W+", "_", s)

        current_time_utc = datetime.now(timezone.utc)
        timestamp = current_time_utc.timestamp()
        datetime_obj = datetime.fromtimestamp(timestamp, UTC)
        datetime_str = datetime_obj.strftime("%Y%m%d_%H%M%S")

        file_path = f"{formatted_producer_name}/{formatted_name}_{datetime_str}.zip"
        return file_path

    def has_report(self) -> bool:
        return self.report is not None


class User(Entity):
    def __init__(
        self,
        email,
        login_provider,
        logout_url,
        activated=False,
        producer: DataProducer = None,
        id: int = None,
    ):
        super().__init__(id)
        self.email = email
        self.login_provider = login_provider
        self.logout_url = logout_url
        self.activated = activated
        self.producer = producer

    # The following property definitions and get_id method are required in order for the
    # Flask-Login library to be able to handle instances of the User domain entity.
    @property
    def is_active(self):
        return isinstance(self.producer, DataProducer) and self.activated

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
        return f"User {self.id}, {self.email}, {self.activated}, {self.producer.name})"

    def associate_with_data_producer(self, producer: DataProducer):
        self.producer = producer
        return self


class Permission:
    CREATE_MAPPING = "create_mapping"
    CREATE_SUBMISSION = "create_submission"
    ACTIVATE_USER = "activate_user"


class Role(Entity):
    def __init__(self, name: str, permissions: list, id: Optional[int] = None):
        super().__init__(id)
        self.name = name
        self.permissions = permissions

    def __repr__(self):
        return f"Role {self.id}, {self.name}, {self.permissions})"

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions
