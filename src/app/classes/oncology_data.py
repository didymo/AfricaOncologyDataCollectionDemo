from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class OncologyData:
    patient_id: str = ""
    event: str = ""
    diagnosis: str = ""
    histo: str = ""
    grade: str = ""
    factors: str = ""
    stage: str = ""
    careplan: str = ""
    note: str = ""
    record_creation_datetime: datetime = field(default_factory=datetime.now)
    event_date: datetime = field(default_factory=datetime.now)
    death_date: Optional[datetime] = None
    death_cause: str = ""
