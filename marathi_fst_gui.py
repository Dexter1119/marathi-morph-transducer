#####################################################################
#
# File Name    : marathi_fst_gui.py
# Description  : Tkinter GUI for the Marathi morphology FST model
# Author       : Pradhumnya Changdev Kalsait
# Date         : 16/04/26
#
#####################################################################

"""Tkinter GUI for the Marathi morphology finite state transducer model.

This interface works with the core engine in marathi_fst_system.py and
provides a simple desktop UI for generation, analysis, lexicon browsing,
and demo execution.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from marathi_fst_system import (
    CASES,
    POS_ADJECTIVE,
    POS_NOUN,
    POS_PRONOUN,
    POS_TAGS,
    MarathiNounFST,
)
from typing import Optional


class MarathiMorphologyGUI:
    """Tkinter user interface for the Marathi morphology FST."""

    #####################################################################
    #
    # Class Name    : MarathiMorphologyGUI
    # Description   : Desktop GUI for generation and analysis
    # Author        : Pradhumnya Changdev Kalsait
    # Date          : 16/04/26
    #
    #####################################################################

    def __init__(self, root: tk.Tk):
        """Initializes the GUI window and widgets.

        Args:
            root (tk.Tk): Main Tkinter window.
        """
        self.root = root
        self.fst = MarathiNounFST()

        self.root.title("Marathi Morphology FST GUI")
        self.root.geometry("940x700")
        self.root.minsize(900, 650)

        self._setup_style()
        self._build_layout()
        self._set_default_values()

    def _setup_style(self) -> None:
        """Configures the Tkinter theme and widget styling."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#f5f1e8")
        style.configure("Panel.TFrame", background="#fffdf8")
        style.configure(
            "App.TLabel",
            background="#f5f1e8",
            foreground="#1f2937",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel",
            background="#f5f1e8",
            foreground="#111827",
            font=("Segoe UI Semibold", 20),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#f5f1e8",
            foreground="#4b5563",
            font=("Segoe UI", 10),
        )
        style.configure(
            "App.TButton",
            font=("Segoe UI", 10),
            padding=(12, 8),
        )
        style.configure(
            "Accent.TButton",
            font=("Segoe UI Semibold", 10),
            padding=(12, 8),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#1d4ed8"), ("!active", "#2563eb")],
            foreground=[("active", "white"), ("!active", "white")],
        )

    def _build_layout(self) -> None:
        """Builds the main GUI layout."""
        main_frame = ttk.Frame(self.root, style="App.TFrame", padding=18)
        main_frame.pack(fill="both", expand=True)

        header_frame = ttk.Frame(main_frame, style="App.TFrame")
        header_frame.pack(fill="x", pady=(0, 14))

        title_label = ttk.Label(
            header_frame,
            text="Marathi Morphology FST",
            style="Title.TLabel",
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            header_frame,
            text="Multi-POS generation and analysis for NOUN, PRONOUN, and ADJECTIVE entries",
            style="Subtitle.TLabel",
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))

        body_frame = ttk.Frame(main_frame, style="App.TFrame")
        body_frame.pack(fill="both", expand=True)

        left_frame = ttk.Frame(body_frame, style="Panel.TFrame", padding=16)
        left_frame.pack(side="left", fill="y", padx=(0, 12))

        right_frame = ttk.Frame(body_frame, style="Panel.TFrame", padding=16)
        right_frame.pack(side="right", fill="both", expand=True)

        self._build_controls(left_frame)
        self._build_output_panel(right_frame)

    def _build_controls(self, parent: ttk.Frame) -> None:
        """Creates the input controls used for generation and analysis."""
        ttk.Label(parent, text="Input Controls", style="App.TLabel").pack(
            anchor="w", pady=(0, 10)
        )

        ttk.Label(parent, text="Lemma", style="App.TLabel").pack(anchor="w")
        self.lemma_var = tk.StringVar()
        self.lemma_entry = ttk.Entry(parent, textvariable=self.lemma_var, width=28)
        self.lemma_entry.pack(fill="x", pady=(4, 10))

        ttk.Label(parent, text="Surface Form", style="App.TLabel").pack(anchor="w")
        self.surface_var = tk.StringVar()
        self.surface_entry = ttk.Entry(parent, textvariable=self.surface_var, width=28)
        self.surface_entry.pack(fill="x", pady=(4, 10))

        ttk.Label(parent, text="POS Tag", style="App.TLabel").pack(anchor="w")
        self.pos_var = tk.StringVar()
        self.pos_combo = ttk.Combobox(
            parent,
            textvariable=self.pos_var,
            values=POS_TAGS,
            state="readonly",
            width=26,
        )
        self.pos_combo.pack(fill="x", pady=(4, 10))

        ttk.Label(parent, text="Case", style="App.TLabel").pack(anchor="w")
        self.case_var = tk.StringVar()
        self.case_combo = ttk.Combobox(
            parent,
            textvariable=self.case_var,
            values=CASES,
            state="readonly",
            width=26,
        )
        self.case_combo.pack(fill="x", pady=(4, 10))

        button_frame = ttk.Frame(parent, style="Panel.TFrame")
        button_frame.pack(fill="x", pady=(8, 12))

        generate_button = ttk.Button(
            button_frame,
            text="Generate",
            style="Accent.TButton",
            command=self._generate_form,
        )
        generate_button.pack(fill="x", pady=(0, 8))

        analyze_button = ttk.Button(
            button_frame,
            text="Analyze",
            style="App.TButton",
            command=self._analyze_form,
        )
        analyze_button.pack(fill="x", pady=(0, 8))

        lexicon_button = ttk.Button(
            button_frame,
            text="Show Lexicon",
            style="App.TButton",
            command=self._show_lexicon,
        )
        lexicon_button.pack(fill="x", pady=(0, 8))

        pos_button = ttk.Button(
            button_frame,
            text="Show POS Tags",
            style="App.TButton",
            command=self._show_pos_tags,
        )
        pos_button.pack(fill="x", pady=(0, 8))

        case_button = ttk.Button(
            button_frame,
            text="Show Cases",
            style="App.TButton",
            command=self._show_cases,
        )
        case_button.pack(fill="x", pady=(0, 8))

        demo_button = ttk.Button(
            button_frame,
            text="Run Demo",
            style="App.TButton",
            command=self._run_demo,
        )
        demo_button.pack(fill="x", pady=(0, 8))

        clear_button = ttk.Button(
            button_frame,
            text="Clear Output",
            style="App.TButton",
            command=self._clear_output,
        )
        clear_button.pack(fill="x")

    def _build_output_panel(self, parent: ttk.Frame) -> None:
        """Creates the output display area."""
        ttk.Label(parent, text="Output", style="App.TLabel").pack(
            anchor="w", pady=(0, 10)
        )

        self.output_box = scrolledtext.ScrolledText(
            parent,
            wrap="word",
            height=24,
            font=("Consolas", 11),
            background="#fffdf8",
            foreground="#111827",
            insertbackground="#111827",
            relief="solid",
            borderwidth=1,
            padx=12,
            pady=12,
        )
        self.output_box.pack(fill="both", expand=True)
        self.output_box.configure(state="disabled")

    def _set_default_values(self) -> None:
        """Sets default selections for the input controls."""
        if POS_TAGS:
            self.pos_combo.set(POS_TAGS[0])
        if CASES:
            self.case_combo.set(CASES[0])

    def _write_output(self, text: str) -> None:
        """Writes text to the output panel.

        Args:
            text (str): Text to display in the output panel.
        """
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text + "\n")
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def _clear_output(self) -> None:
        """Clears the output panel."""
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def _get_inputs(self) -> tuple[str, str, Optional[str]]:
        """Collects the current GUI inputs.

        Returns:
            tuple[str, str, Optional[str]]: Lemma, case, and POS filter.
        """
        lemma = self.lemma_var.get().strip()
        case = self.case_var.get().strip().upper()
        pos = self.pos_var.get().strip().upper() or None
        return lemma, case, pos

    def _generate_form(self) -> None:
        """Generates a surface form using the selected lemma, case, and POS."""
        lemma, case, pos = self._get_inputs()
        result = self.fst.generate(lemma, case, pos)
        self._write_output(f"GEN: {result}")

    def _analyze_form(self) -> None:
        """Analyzes a surface form against the selected POS filter."""
        surface_form = self.surface_var.get().strip()
        if not surface_form:
            messagebox.showinfo(
                "Input Needed",
                "Enter a surface form, then click Analyze.",
            )
            return

        pos = self.pos_var.get().strip().upper() or None
        result = self.fst.analyze(surface_form, pos)
        self._write_output(f"ANA: {result}")

    def _show_lexicon(self) -> None:
        """Displays the current lexicon in the output panel."""
        self._clear_output()
        self._write_output("Lexicon by POS:")
        for lemma, entry in self.fst.entries.items():
            self._write_output(
                f"- {lemma} | POS={entry.pos} | class={entry.noun_class} | gender={entry.gender}"
            )

    def _show_pos_tags(self) -> None:
        """Displays supported POS tags."""
        self._clear_output()
        self._write_output("Supported POS tags:")
        for pos in self.fst.list_pos_tags():
            self._write_output(f"- {pos}")

    def _show_cases(self) -> None:
        """Displays supported case labels."""
        self._clear_output()
        self._write_output("Supported cases:")
        for case in self.fst.list_cases():
            self._write_output(f"- {case}")

    def _run_demo(self) -> None:
        """Runs the demo and prints all sample outputs."""
        self._clear_output()
        self._write_output("Demo output:")
        samples = [
            ("घर", "DATIVE", POS_NOUN),
            ("गाव", "GENITIVE", POS_NOUN),
            ("मी", "DATIVE", POS_PRONOUN),
            ("चांगला", "NOMINATIVE", POS_ADJECTIVE),
        ]
        for lemma, case, pos in samples:
            self._write_output(self.fst.generate(lemma, case, pos))


def main() -> None:
    """Launches the Tkinter GUI application."""
    root = tk.Tk()
    MarathiMorphologyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
