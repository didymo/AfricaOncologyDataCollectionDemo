from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class OncologyData:
    autoincrement_id: Optional[int] = field(
        default=None
    )  # Primary key, auto-incremented; None for new entries
    record_creation_datetime: datetime
    patient_id: str
    event: str
    event_date: datetime
    diagnosis: Optional[str] = None
    histo: Optional[str] = None
    grade: Optional[str] = None
    factors: Optional[str] = None
    stage: Optional[str] = None
    careplan: Optional[str] = None
    death_date: Optional[datetime] = None
    death_cause: Optional[str] = None
    note: Optional[str] = None
