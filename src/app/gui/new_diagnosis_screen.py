# new_diagnosis_screen.py
import csv
import datetime
import os
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
        date_entry = ttk.Entry(info_frame)
        date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        date_entry.grid(row=1, column=1, sticky="ew", padx=5)

        # Diagnosis
        ttk.Label(info_frame, text="Diagnosis").grid(row=2, column=0, sticky="w")

        csv_path = os.path.join(
            os.path.dirname(__file__), "..", "csv_files", "Diagnosis.ICD10.csv"
        )
        diagnosis_options = []
        with open(csv_path, newline="", encoding="latin-1") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # ensure the row is not empty
                    diagnosis_options.append(" ".join(row).strip())

        diagnosis_combo = ttk.Combobox(info_frame, values=diagnosis_options)
        diagnosis_combo.grid(row=2, column=1, sticky="ew", padx=5)

        def on_keyrelease(event):
            typed = diagnosis_combo.get()
            if typed == "":
                diagnosis_combo["values"] = diagnosis_options
            else:
                filtered = [
                    option
                    for option in diagnosis_options
                    if typed.lower() in option.lower()
                ]
                diagnosis_combo["values"] = filtered
            # Optionally, open the dropdown list if there are matches.
            diagnosis_combo.event_generate("<Down>")

        diagnosis_combo.bind("<KeyRelease>", on_keyrelease)

        info_frame.grid_columnconfigure(1, weight=1)

    def create_cancer_details(self):
        """Create cancer details section with aligned stage label."""
        details_frame = ttk.LabelFrame(self, padding=5)
        details_frame.pack(fill="x", padx=5, pady=2)

        # Histo and Grade
        # Histo (Histopathology) with auto-complete based on Histopathology.CSV
        ttk.Label(details_frame, text="Histo").grid(row=0, column=0, sticky="w")

        csv_path = os.path.join(
            os.path.dirname(__file__), "..", "csv_files", "Histopathology.CSV"
        )
        histo_options = []
        with open(csv_path, newline="", encoding="latin-1") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    histo_options.append(" ".join(row).strip())

        histo_combo = ttk.Combobox(details_frame, values=histo_options)
        histo_combo.grid(row=0, column=1, sticky="ew", padx=5)

        def on_histo_keyrelease(event):
            typed = histo_combo.get()
            if typed == "":
                histo_combo["values"] = histo_options
            else:
                filtered = [
                    option
                    for option in histo_options
                    if typed.lower() in option.lower()
                ]
                histo_combo["values"] = filtered
            histo_combo.event_generate("<Down>")

        histo_combo.bind("<KeyRelease>", on_histo_keyrelease)

        # Grade
        ttk.Label(details_frame, text="Grade").grid(row=0, column=2, sticky="w")
        grade_combo = ttk.Combobox(details_frame, values=[1, 2, 3, 4, 9])
        grade_combo.grid(row=0, column=3, sticky="ew", padx=5)

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
        """
        Create care plan section with toggle buttons arranged in two equal-width
        columns, aligned to the right with a header label on top.
        """
        # The LabelFrame itself is aligned to the right.
        care_frame = ttk.LabelFrame(self, padding=5)
        care_frame.pack(fill="x", padx=5, pady=2, anchor="e")

        # Header label for the care plan group.
        ttk.Label(
            care_frame, text="Care Planned First", font=("Arial", 10, "bold")
        ).pack(anchor="center", pady=(0, 5))

        # Create a subframe to hold the grid of buttons.
        grid_frame = ttk.Frame(care_frame)
        grid_frame.pack(anchor="e")

        # Define treatments in rows. Some rows contain one button; others contain two.
        treatments = [
            ["Observe"],
            ["Surgery", "Radiation"],
            ["Chemo", "Brachy"],
            ["Immuno", "Hormones"],
            ["Small mol."],
        ]

        # Configure grid columns for equal expansion.
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Create buttons using grid layout.
        for row_index, row in enumerate(treatments):
            for col in range(2):
                if col < len(row):
                    treatment = row[col]
                    btn = tk.Button(grid_frame, text=treatment, width=12)
                    btn.selected = False
                    btn.default_bg = btn.cget("bg")
                    btn.config(command=lambda b=btn: self.toggle_button(b))
                    btn.grid(row=row_index, column=col, padx=5, pady=2, sticky="ew")
                else:
                    # Insert an empty placeholder to maintain two columns.
                    ttk.Label(grid_frame, text="").grid(
                        row=row_index, column=col, padx=5, pady=2
                    )

    def toggle_button(self, button):
        """Toggle the button's selected state and change its color."""
        if button.selected:
            # Unselect the button and revert its color.
            button.selected = False
            button.config(bg=button.default_bg)
        else:
            # Select the button and change its background to green.
            button.selected = True
            button.config(bg="green")

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
