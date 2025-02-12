import datetime
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Optional


class DatabaseService:
    """
    Thread-safe service class for handling database operations.
    Uses connection pooling and context managers to ensure safe concurrent access.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path: Optional[str] = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseService, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the database service with connection pooling."""
        if self._initialized:
            return

        self.db_path = db_path or str(
            Path.home() / "africa_oncology_settings" / "database.sqlite"
        )
        self._local = threading.local()
        self._lock = threading.Lock()
        self._initialized = True

    @contextmanager
    def get_connection(self):
        """Thread-safe context manager for database connections."""
        if not hasattr(self._local, "connection"):
            self._local.connection = sqlite3.connect(self.db_path)

        try:
            yield self._local.connection
        except Exception as e:
            self._local.connection.rollback()
            raise e
        else:
            self._local.connection.commit()

    def close_connections(self):
        """Close the connection for the current thread if it exists."""
        if hasattr(self._local, "connection"):
            self._local.connection.close()
            del self._local.connection

    def save_diagnosis_record(self, record_data: Dict) -> int:
        """
        Save a new diagnosis record to the database.
        Returns the AutoincrementID of the inserted record.
        """
        with self._lock:  # Ensure thread-safe write operation
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Prepare the SQL statement
                sql = """
                INSERT INTO oncology_data (
                    record_creation_datetime,
                    PatientID,
                    Event,
                    Event_Date,
                    Histo,
                    Grade,
                    Factors,
                    Stage,
                    Careplan,
                    Note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

                # Prepare the values tuple
                values = (
                    datetime.datetime.now().isoformat(),
                    record_data.get("Patient_ID", ""),
                    record_data.get("Event", ""),
                    record_data.get("Event_Date", ""),
                    record_data.get("Histo", ""),
                    record_data.get("Grade", ""),
                    record_data.get("Factors", ""),
                    record_data.get("Stage", ""),
                    record_data.get("Care_Plan", ""),
                    record_data.get("Note", ""),
                )

                cursor.execute(sql, values)
                return cursor.lastrowid

    def get_diagnosis_record(self, record_id: int) -> Dict:
        """Retrieve a specific diagnosis record by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM oncology_data WHERE AutoincrementID = ?
            """,
                (record_id,),
            )

            record = cursor.fetchone()
            if record:
                # Convert tuple to dictionary using column names
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, record))
            return {}

    def get_patient_records(self, patient_id: str) -> list:
        """Retrieve all records for a specific patient."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM oncology_data
                WHERE PatientID = ?
                ORDER BY Event_Date DESC
            """,
                (patient_id,),
            )

            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def update_diagnosis_record(self, record_id: int, record_data: Dict) -> bool:
        """Update an existing diagnosis record."""
        with self._lock:  # Ensure thread-safe write operation
            with self.get_connection() as conn:
                cursor = conn.cursor()

                update_fields = []
                values = []

                # Build dynamic update statement based on provided fields
                for field, value in record_data.items():
                    if field != "AutoincrementID":  # Skip the primary key
                        update_fields.append(f"{field} = ?")
                        values.append(value)

                if not update_fields:
                    return False

                # Add record_id to values
                values.append(record_id)

                sql = f"""
                UPDATE oncology_data
                SET {', '.join(update_fields)}
                WHERE AutoincrementID = ?
                """

                cursor.execute(sql, values)
                return cursor.rowcount > 0
