# oncology_patient_data.py
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class OncologyPatientData:
    # Corresponds to: AutoincrementID INTEGER PRIMARY KEY AUTOINCREMENT
    autoincrement_id: Optional[int] = None

    # Corresponds to: record_creation_datetime TEXT NOT NULL
    record_creation_datetime: str = ""

    # Corresponds to: PatientID TEXT NOT NULL
    patient_id: str = ""

    # Corresponds to: Event TEXT NOT NULL
    event: str = ""

    # Corresponds to: Event_Date TEXT NOT NULL
    event_date: str = ""

    # Corresponds to: Histo TEXT
    histo: Optional[str] = None

    # Corresponds to: Grade TEXT
    grade: Optional[str] = None

    # Corresponds to: Factors TEXT
    factors: Optional[str] = None

    # Corresponds to: Stage TEXT
    stage: Optional[str] = None

    # Corresponds to: Careplan TEXT
    careplan: Optional[str] = None

    # Corresponds to: Note TEXT
    note: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert the OncologyPatientData instance to a dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "OncologyPatientData":
        """
        Create an OncologyPatientData instance from a dictionary.
        The dictionary keys should match the field names.
        """
        return cls(
            autoincrement_id=data.get("autoincrement_id"),
            record_creation_datetime=data.get("record_creation_datetime", ""),
            patient_id=data.get("patient_id", ""),
            event=data.get("event", ""),
            event_date=data.get("event_date", ""),
            histo=data.get("histo"),
            grade=data.get("grade"),
            factors=data.get("factors"),
            stage=data.get("stage"),
            careplan=data.get("careplan"),
            note=data.get("note"),
        )
