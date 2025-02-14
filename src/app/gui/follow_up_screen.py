# follow_up_screen.py
import csv
import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk

from app.database.database_service import DatabaseService


class FollowUpScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Predefine instance attributes to satisfy the IDE.
        self.patient_id_combo = None
        self.date_entry = None
        self.diagnosis_combo = None
        self.histo_combo = None
        self.grade_combo = None
        self.factors_entry = None

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create content in scrollable frame instead of self
        self.create_header()
        self.create_patient_info()
        self.create_cancer_details()
        self.create_care_plan()
        self.create_notes()
        self.create_footer()

    def create_header(self):
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill="x", padx=5, pady=5)

        new_dx_btn = ttk.Button(
            header_frame,
            text="New Dx",
            style="Active.TButton",
            command=self.controller.show_new_diagnosis_screen,
        )
        followup_btn = ttk.Button(
            header_frame, text="FollowUp", command=self.controller.show_followup_screen
        )
        death_btn = ttk.Button(header_frame, text="Death")

        new_dx_btn.pack(side="left", padx=2)
        followup_btn.pack(side="left", padx=2)
        death_btn.pack(side="left", padx=2)

    def create_patient_info(self):
        """Create patient identification section.
        When a Patient ID is selected, populate Diagnosis, Histo, Grade, and Factors.
        """
        info_frame = ttk.LabelFrame(self.scrollable_frame, padding=5)
        info_frame.pack(fill="x", padx=5, pady=2)

        # --- Patient ID with live search ---
        ttk.Label(info_frame, text="Patient ID").grid(row=0, column=0, sticky="w")
        # Use a Combobox instead of an Entry
        self.patient_id_combo = ttk.Combobox(info_frame)
        self.patient_id_combo.grid(row=0, column=1, sticky="ew", padx=5)

        def on_patient_id_keyrelease(event):
            typed = event.widget.get()
            # Import DatabaseService here to avoid circular dependencies
            from app.database.database_service import DatabaseService

            db_service = DatabaseService()
            with db_service.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT DISTINCT PatientID FROM oncology_data "
                    "WHERE PatientID LIKE ?",
                    (typed + "%",),
                )
                results = [row[0] for row in cursor.fetchall()]
            if results:
                event.widget["values"] = results
                event.widget.event_generate("<Down>")
            else:
                event.widget["values"] = []

        self.patient_id_combo.bind("<KeyRelease>", on_patient_id_keyrelease)

        # When a Patient ID is selected, populate the fields below.
        def on_patient_id_selected(event):
            selected_patient_id = event.widget.get()
            from app.database.database_service import DatabaseService

            db_service = DatabaseService()
            records = db_service.get_patient_records(selected_patient_id)
            if not records:
                return
            # If more than one record exists, choose the first for simplicity.
            record = records[0]
            # The PatientID in the record is assumed to be
            # of the form "patientID.diagnosisCode"
            parts = record.get("PatientID", "").split(".")
            diagnosis_code = parts[1] if len(parts) > 1 else ""
            # Map the diagnosis code to the corresponding display value from the CSV
            if diagnosis_code in self.diagnosis_codes:
                index = self.diagnosis_codes.index(diagnosis_code)
                diagnosis_display_value = self.diagnosis_display[index]
            else:
                diagnosis_display_value = ""
            self.diagnosis_combo.set(diagnosis_display_value)
            # Populate Histo, Grade, and Factors fields from the record
            self.histo_combo.set(record.get("Histo", ""))
            self.grade_combo.set(record.get("Grade", ""))
            self.factors_entry.delete(0, tk.END)
            self.factors_entry.insert(0, record.get("Factors", ""))

        self.patient_id_combo.bind("<<ComboboxSelected>>", on_patient_id_selected)

        # --- Date of Diagnosis ---
        ttk.Label(info_frame, text="Date of Diagnosis").grid(
            row=1, column=0, sticky="w"
        )
        self.date_entry = ttk.Entry(info_frame)
        self.date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, sticky="ew", padx=5)

        # --- Diagnosis ---
        ttk.Label(info_frame, text="Diagnosis").grid(row=2, column=0, sticky="w")
        csv_path = os.path.join(
            os.path.dirname(__file__), "..", "csv_files", "Diagnosis.ICD10.csv"
        )
        self.diagnosis_codes = []  # Store just the codes
        self.diagnosis_display = []  # Store the full display strings for the combobox
        with open(csv_path, newline="", encoding="latin-1") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # ensure the row is not empty
                    self.diagnosis_codes.append(row[0].strip())
                    self.diagnosis_display.append(" ".join(row).strip())
        self.diagnosis_combo = ttk.Combobox(info_frame, values=self.diagnosis_display)
        self.diagnosis_combo.grid(row=2, column=1, sticky="ew", padx=5)

        def on_keyrelease(event):
            typed = event.widget.get()
            if typed == "":
                event.widget["values"] = self.diagnosis_display
            else:
                filtered = [
                    option
                    for option in self.diagnosis_display
                    if typed.lower() in option.lower()
                ]
                event.widget["values"] = filtered
            event.widget.event_generate("<Down>")

        self.diagnosis_combo.bind("<KeyRelease>", on_keyrelease)
        info_frame.grid_columnconfigure(1, weight=1)

    def create_cancer_details(self):
        """Create cancer details section with aligned stage label."""
        details_frame = ttk.LabelFrame(self.scrollable_frame, padding=5)
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
        default_factors = (
            "ER|PR|HER2|LN/|BRCA1|BRCA2|GS+|PSA|EPE|cores/|"
            "p16|EBV|ENE|PNI|PDL1%|EGFR|ALK|ROS1|BRAF|KRAS|R-mm"
        )
        self.factors_entry.insert(0, default_factors)
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
        care_frame = ttk.LabelFrame(self.scrollable_frame, padding=5)
        care_frame.pack(fill="x", padx=5, pady=2, anchor="e")
        ttk.Label(
            care_frame, text="Care Planned First", font=("Arial", 10, "bold")
        ).pack(anchor="center", pady=(0, 5))
        treatments = [
            ["Observe"],
            ["Surgery", "Radiation"],
            ["Chemo", "Brachy"],
            ["Immuno", "Hormones"],
            ["Small mol."],
        ]
        grid_frame = ttk.Frame(care_frame)
        grid_frame.pack(anchor="w")
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
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
            button.selected = False
            button.config(bg=button.default_bg)
        else:
            button.selected = True
            button.config(bg="green")

    def create_notes(self):
        """Create notes section."""
        notes_frame = ttk.LabelFrame(self.scrollable_frame, padding=5)
        notes_frame.pack(fill="both", expand=True, padx=5, pady=2)
        ttk.Label(notes_frame, text="Notes").pack(anchor="w")
        self.notes_text = tk.Text(notes_frame, height=4)
        self.notes_text.pack(fill="both", expand=True, pady=5)

    def create_footer(self):
        """Create footer with copy button."""
        footer_frame = ttk.Frame(self.scrollable_frame)
        footer_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(footer_frame, text="COPY", command=self.copy_to_clipboard).pack(
            side="right"
        )

    def copy_to_clipboard(self):
        """Copy diagnosis data to clipboard and save to database."""
        # Get the actual diagnosis code from the diagnosis combobox
        selected_index = self.diagnosis_display.index(self.diagnosis_combo.get())
        actual_code = self.diagnosis_codes[selected_index]
        # Create the combined patient ID with diagnosis code
        patient_diagnosis_id = f"{self.patient_id_combo.get()}.{actual_code}"
        record_data = {
            "Patient_ID": patient_diagnosis_id,
            "Event": "Follow Up",
            "Event_Date": self.date_entry.get(),
            "Histo": self.histo_combo.get(),
            "Grade": self.grade_combo.get(),
            "Stage": " ".join(
                [
                    self.t_stage_combo.get(),
                    self.n_stage_combo.get(),
                    self.m_stage_combo.get(),
                ]
            ).strip(),
            "Care_Plan": ", ".join(
                btn.cget("text") for btn in self.care_plan_buttons if btn.selected
            ),
            "Factors": self.factors_entry.get(),
            "Note": self.notes_text.get("1.0", "end").strip(),
        }
        output = (
            "Patient_ID: {Patient_ID}\n"
            "Event: {Event}\n"
            "Event_Date: {Event_Date}\n"
            "Histo: {Histo}\n"
            "Grade: {Grade}\n"
            "Factors: {Factors}\n"
            "Stage: {Stage}\n"
            "Care_Plan: {Care_Plan}\n"
            "Note: {Note}"
        ).format(**record_data)
        self.clipboard_clear()
        self.clipboard_append(output)
        try:
            db_service = DatabaseService()  # Singleton instance
            record_id = db_service.save_diagnosis_record(record_data)
            messagebox.showinfo(
                "Success", f"Record saved successfully (ID: {record_id})"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save record: {str(e)}")
