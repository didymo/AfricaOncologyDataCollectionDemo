CREATE TABLE IF NOT EXISTS oncology_data (
    AutoincrementID INTEGER PRIMARY KEY AUTOINCREMENT,
    record_creation_datetime TEXT NOT NULL,
    PatientID TEXT NOT NULL,
    Event TEXT NOT NULL,
    Event_Date TEXT NOT NULL,
    Histo TEXT,
    Grade TEXT,
    Stage TEXT,
    Careplan TEXT,
    Factors TEXT,
    Note TEXT
);
