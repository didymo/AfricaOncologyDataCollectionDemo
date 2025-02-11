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
        self.patient_id_entry = ttk.Entry(info_frame)
        self.patient_id_entry.grid(row=0, column=1, sticky="ew", padx=5)

        # Date of Diagnosis
        ttk.Label(info_frame, text="Date of Diagnosis").grid(
            row=1, column=0, sticky="w"
        )
        self.date_entry = ttk.Entry(info_frame)
        self.date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, sticky="ew", padx=5)

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

        self.diagnosis_combo = ttk.Combobox(info_frame, values=diagnosis_options)
        self.diagnosis_combo.grid(row=2, column=1, sticky="ew", padx=5)
        # self.diagnosis_combo.bind('<KeyRelease>', on_keyrelease)

        def on_keyrelease(event):
            typed = event.diagnosis_combo.get()
            if typed == "":
                event.diagnosis_combo["values"] = diagnosis_options
            else:
                filtered = [
                    option
                    for option in diagnosis_options
                    if typed.lower() in option.lower()
                ]
                event.diagnosis_combo["values"] = filtered
            # Optionally, open the dropdown list if there are matches.
            event.diagnosis_combo.event_generate("<Down>")

        self.diagnosis_combo.bind("<KeyRelease>", on_keyrelease)

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

        self.histo_combo = ttk.Combobox(details_frame, values=histo_options)
        self.histo_combo.grid(row=0, column=1, sticky="ew", padx=5)
        # self.histo_combo.bind('<KeyRelease>', on_histo_keyrelease)

        def on_histo_keyrelease(event):
            typed = event.histo_combo.get()
            if typed == "":
                event.histo_combo["values"] = histo_options
            else:
                filtered = [
                    option
                    for option in histo_options
                    if typed.lower() in option.lower()
                ]
                event.histo_combo["values"] = filtered
            event.histo_combo.event_generate("<Down>")

        self.histo_combo.bind("<KeyRelease>", on_histo_keyrelease)

        # Grade
        ttk.Label(details_frame, text="Grade").grid(row=1, column=0, sticky="w")
        self.grade_combo = ttk.Combobox(details_frame, values=[1, 2, 3, 4, 9])
        self.grade_combo.grid(row=1, column=1, sticky="ew", padx=5)

        # Factors
        ttk.Label(details_frame, text="Factors").grid(row=2, column=0, sticky="w")
        self.factors_entry = ttk.Entry(details_frame)
        self.factors_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5)

        # Stage - Now aligned with Factors entry
        stage_frame = ttk.Frame(details_frame)
        stage_frame.grid(row=3, column=1, columnspan=3, sticky="w")

        ttk.Label(stage_frame, text="Stage").pack(side="left")
        ttk.Entry(stage_frame, width=8).pack(side="left", padx=5)

        ttk.Label(stage_frame, text="T").pack(side="left", padx=5)
        self.t_stage_combo = ttk.Combobox(
            stage_frame, values=["T0", "T1", "T2", "T3", "T4", "Tx"], width=4
        )
        self.t_stage_combo.pack(side="left", padx=5)

        ttk.Label(stage_frame, text="N").pack(side="left", padx=5)
        self.n_stage_combo = ttk.Combobox(
            stage_frame, values=["N0", "N1", "N2", "N3", "Nx"], width=4
        )
        self.n_stage_combo.pack(side="left", padx=5)

        ttk.Label(stage_frame, text="M").pack(side="left", padx=5)
        m_values = [
            "M0",
            "M1",
            "M1-adrenal",
            "M1-bladder",
            "M1-bone",
            "M1-cerebellum",
            "M1-cerebrum",
            "M1-eye",
            "M1-fat",
            "M1-headandneck",
            "M1-heart",
            "M1-kidneys",
            "M1-liver",
            "M1-lung",
            "M1-lymphnode",
            "M1-muscle",
            "M1-nasalcavity",
            "M1-oesophagus",
            "M1-ovary",
            "M1-pancreas",
            "M1-parathyroid",
            "M1-peritoneum",
            "M1-pleural",
            "M1-retroperitoneum",
            "M1-salivaryglang",
            "M1-sinuses",
            "M1-skin",
            "M1-spinalcanal",
            "M1-spinalcord",
            "M1-spleen",
            "M1-stomach",
            "M1-subcutaneous",
            "M1-thyroid",
            "M1-vagina",
        ]
        m_width = max(len(s) for s in m_values)
        self.m_stage_combo = ttk.Combobox(stage_frame, values=m_values, width=m_width)
        self.m_stage_combo.pack(side="left", padx=5)

        details_frame.grid_columnconfigure(1, weight=1)

    def create_care_plan(self):
        """Create care plan section."""
        care_frame = ttk.LabelFrame(self, padding=5)
        care_frame.pack(fill="x", padx=5, pady=2, anchor="e")
        ttk.Label(
            care_frame, text="Care Planned First", font=("Arial", 10, "bold")
        ).pack(anchor="center", pady=(0, 5))

        # Define treatment groups as before
        treatments = [
            ["Observe"],
            ["Surgery", "Radiation"],
            ["Chemo", "Brachy"],
            ["Immuno", "Hormones"],
            ["Small mol."],
        ]

        # Create a grid frame for two columns of buttons
        grid_frame = ttk.Frame(care_frame)
        grid_frame.pack(anchor="e")
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Create toggle buttons and store them in self.care_plan_buttons
        self.care_plan_buttons = []
        for row_index, row in enumerate(treatments):
            for col in range(2):
                if col < len(row):
                    treatment = row[col]
                    btn = tk.Button(grid_frame, text=treatment)
                    btn.selected = False
                    btn.default_bg = btn.cget("bg")
                    btn.config(command=lambda b=btn: self.toggle_button(b))
                    btn.grid(row=row_index, column=col, padx=5, pady=2, sticky="ew")
                    self.care_plan_buttons.append(btn)
                else:
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
        self.notes_text = tk.Text(notes_frame, height=4)
        self.notes_text.pack(fill="both", expand=True, pady=5)

    def create_footer(self):
        """Create footer with copy button."""
        footer_frame = ttk.Frame(self)
        footer_frame.pack(fill="x", padx=5, pady=5)

        def copy_to_clipboard():
            # Gather field values for copying:
            patient_id = self.patient_id_entry.get()
            event = self.diagnosis_combo.get()
            event_date = self.date_entry.get()
            histo = self.histo_combo.get()
            grade = self.grade_combo.get()
            stage = "{} {} {}".format(
                self.t_stage_combo.get(),
                self.n_stage_combo.get(),
                self.m_stage_combo.get(),
            )
            care_plan = ", ".join(
                btn.cget("text") for btn in self.care_plan_buttons if btn.selected
            )
            factors = self.factors_entry.get()
            note = self.notes_text.get("1.0", "end").strip()

            # Format the output string:
            output = (
                "Patient_ID: {}\n"
                "Event: {}\n"
                "Event_Date: {}\n"
                "Histo: {}\n"
                "Grade: {}\n"
                "Stage: {}\n"
                "Care_Plan: {}\n"
                "Factors: {}\n"
                "Note: {}"
            ).format(
                patient_id,
                event,
                event_date,
                histo,
                grade,
                stage,
                care_plan,
                factors,
                note,
            )

            # Copy to the clipboard.
            self.clipboard_clear()
            self.clipboard_append(output)

        # Replace the existing COPY button with one that calls copy_to_clipboard:
        ttk.Button(footer_frame, text="COPY", command=copy_to_clipboard).pack(
            side="right"
        )
