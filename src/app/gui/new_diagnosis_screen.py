# new_diagnosis_screen.py
import tkinter as tk
from tkinter import ttk


class NewDiagnosisScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_header()
        self.create_patient_info()
        self.create_cancer_details()
        self.create_care_plan()
        self.create_notes()
        self.create_footer()

    def create_header(self):
        """Create the header with navigation buttons."""
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=5, pady=5)

        # Navigation buttons
        new_dx_btn = ttk.Button(header_frame, text="New Dx", style="Active.TButton")
        followup_btn = ttk.Button(header_frame, text="FollowUp")
        death_btn = ttk.Button(header_frame, text="Death")

        new_dx_btn.pack(side="left", padx=2)
        followup_btn.pack(side="left", padx=2)
        death_btn.pack(side="left", padx=2)

    def create_patient_info(self):
        """Create patient identification section."""
        info_frame = ttk.LabelFrame(self, padding=5)
        info_frame.pack(fill="x", padx=5, pady=2)

        # Patient ID
        ttk.Label(info_frame, text="Patient ID").grid(row=0, column=0, sticky="w")
        ttk.Entry(info_frame).grid(row=0, column=1, sticky="ew", padx=5)

        # Date of Diagnosis
        ttk.Label(info_frame, text="Date of Diagnosis").grid(
            row=1, column=0, sticky="w"
        )
        ttk.Entry(info_frame).grid(row=1, column=1, sticky="ew", padx=5)

        # Diagnosis
        ttk.Label(info_frame, text="Diagnosis").grid(row=2, column=0, sticky="w")
        ttk.Entry(info_frame).grid(row=2, column=1, sticky="ew", padx=5)

        info_frame.grid_columnconfigure(1, weight=1)

    def create_cancer_details(self):
        """Create cancer details section with aligned stage label."""
        details_frame = ttk.LabelFrame(self, padding=5)
        details_frame.pack(fill="x", padx=5, pady=2)

        # Histo and Grade
        ttk.Label(details_frame, text="Histo").grid(row=0, column=0, sticky="w")
        ttk.Entry(details_frame).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Label(details_frame, text="Grade").grid(row=0, column=2, sticky="w")
        ttk.Entry(details_frame).grid(row=0, column=3, sticky="ew", padx=5)

        # Factors
        ttk.Label(details_frame, text="Factors").grid(row=1, column=0, sticky="w")
        factors_entry = ttk.Entry(details_frame)
        factors_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5)

        # Stage - Now aligned with Factors entry
        stage_frame = ttk.Frame(details_frame)
        stage_frame.grid(row=2, column=1, columnspan=3, sticky="w")

        ttk.Label(stage_frame, text="Stage").pack(side="left")
        ttk.Entry(stage_frame, width=8).pack(side="left", padx=5)
        ttk.Label(stage_frame, text="T").pack(side="left", padx=5)
        ttk.Entry(stage_frame, width=4).pack(side="left", padx=5)
        ttk.Label(stage_frame, text="N").pack(side="left", padx=5)
        ttk.Entry(stage_frame, width=4).pack(side="left", padx=5)
        ttk.Label(stage_frame, text="M").pack(side="left", padx=5)
        ttk.Entry(stage_frame, width=4).pack(side="left", padx=5)
        ttk.Label(stage_frame, text="Initial Stage").pack(side="left", padx=5)

        details_frame.grid_columnconfigure(1, weight=1)

    def create_care_plan(self):
        """Create care plan section."""
        care_frame = ttk.LabelFrame(self, padding=5)
        care_frame.pack(fill="x", padx=5, pady=2)

        ttk.Label(
            care_frame, text="Care Planned First", font=("Arial", 10, "bold")
        ).pack(anchor="w")

        treatments = [
            ["Observe"],
            ["Surgery", "Radiation"],
            ["Chemo", "Brachy"],
            ["Immuno", "Hormones"],
            ["Small mol."],
        ]

        for row in treatments:
            treatment_row = ttk.Frame(care_frame)
            treatment_row.pack(fill="x", pady=2)
            for treatment in row:
                ttk.Checkbutton(treatment_row, text=treatment).pack(side="left", padx=5)

    def create_notes(self):
        """Create notes section."""
        notes_frame = ttk.LabelFrame(self, padding=5)
        notes_frame.pack(fill="both", expand=True, padx=5, pady=2)

        ttk.Label(notes_frame, text="Notes").pack(anchor="w")
        notes_text = tk.Text(notes_frame, height=4)
        notes_text.pack(fill="both", expand=True, pady=5)

    def create_footer(self):
        """Create footer with copy button."""
        footer_frame = ttk.Frame(self)
        footer_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(footer_frame, text="COPY").pack(side="right")
