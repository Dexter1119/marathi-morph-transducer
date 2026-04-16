#####################################################################
#
# File Name    : marathi_fst_system.py
# Description  : Marathi morphology FST model with multiple POS tags
# Author       : Pradhumnya Changdev Kalsait
# Date         : 16/04/26
#
#####################################################################

"""Marathi morphology using a finite state transducer style model.

This project now supports multiple POS tags in a compact FST-style setup.
It demonstrates Marathi case morphology with an add/delete table and a small
lexicon of regular and irregular patterns for nouns, pronouns, and adjectives.

The implementation is intentionally pedagogical. It is suitable for an NLP
assignment or lab submission that needs a clear FST-style rule system rather
than a full industrial morphological analyzer.
"""

from dataclasses import dataclass, field
import sys
from typing import Dict, List, Optional


CASE_NOMINATIVE = "NOMINATIVE"
CASE_DATIVE = "DATIVE"
CASE_INSTRUMENTAL = "INSTRUMENTAL"
CASE_LOCATIVE = "LOCATIVE"
CASE_GENITIVE = "GENITIVE"
CASE_ABLATIVE = "ABLATIVE"

CASES = [
    CASE_NOMINATIVE,
    CASE_DATIVE,
    CASE_INSTRUMENTAL,
    CASE_LOCATIVE,
    CASE_GENITIVE,
    CASE_ABLATIVE,
]

POS_NOUN = "NOUN"
POS_PRONOUN = "PRONOUN"
POS_ADJECTIVE = "ADJECTIVE"

POS_TAGS = [POS_NOUN, POS_PRONOUN, POS_ADJECTIVE]


@dataclass(frozen=True)
class CaseRule:
    """Stores one add/delete rule for a morphological case."""

    case: str
    delete: str
    add: str
    description: str


@dataclass
class LexemeEntry:
    """Represents a lexeme with POS, class, and surface overrides."""

    lemma: str
    pos: str
    gender: str
    noun_class: str
    overrides: Dict[str, str] = field(default_factory=dict)


class MarathiNounFST:
    """Finite-state style model for Marathi morphology."""

    #####################################################################
    #
    # Class Name    : MarathiNounFST
    # Description   : Handles Marathi noun, pronoun, and adjective mapping
    # Author        : Pradhumnya Changdev Kalsait
    # Date          : 16/04/26
    #
    #####################################################################

    def __init__(self):
        """Initializes the lexicon and the case rules used by the FST."""
        self.entries: Dict[str, LexemeEntry] = {
            "घर": LexemeEntry("घर", POS_NOUN, "neuter", "CONSONANT"),
            "गाव": LexemeEntry("गाव", POS_NOUN, "masculine", "CONSONANT"),
            "शहर": LexemeEntry("शहर", POS_NOUN, "neuter", "CONSONANT"),
            "पुस्तक": LexemeEntry("पुस्तक", POS_NOUN, "neuter", "CONSONANT"),
            "भारत": LexemeEntry("भारत", POS_NOUN, "masculine", "CONSONANT"),
            "शाळा": LexemeEntry("शाळा", POS_NOUN, "feminine", "A_CLASS"),
            "विद्यार्थी": LexemeEntry(
                "विद्यार्थी",
                POS_NOUN,
                "masculine",
                "IRREGULAR",
                overrides={
                    CASE_DATIVE: "विद्यार्थ्याला",
                    CASE_INSTRUMENTAL: "विद्यार्थ्याने",
                    CASE_LOCATIVE: "विद्यार्थ्यात",
                    CASE_GENITIVE: "विद्यार्थ्याचा",
                    CASE_ABLATIVE: "विद्यार्थ्याहून",
                },
            ),
            "मुलगा": LexemeEntry(
                "मुलगा",
                POS_NOUN,
                "masculine",
                "IRREGULAR",
                overrides={
                    CASE_DATIVE: "मुलाला",
                    CASE_INSTRUMENTAL: "मुलाने",
                    CASE_LOCATIVE: "मुलात",
                    CASE_GENITIVE: "मुलाचा",
                    CASE_ABLATIVE: "मुलाहून",
                },
            ),
            "मुलगी": LexemeEntry(
                "मुलगी",
                POS_NOUN,
                "feminine",
                "IRREGULAR",
                overrides={
                    CASE_DATIVE: "मुलीला",
                    CASE_INSTRUMENTAL: "मुलीने",
                    CASE_LOCATIVE: "मुलीत",
                    CASE_GENITIVE: "मुलीची",
                    CASE_ABLATIVE: "मुलीहून",
                },
            ),
            "मी": LexemeEntry(
                "मी",
                POS_PRONOUN,
                "neutral",
                "IRREGULAR",
                overrides={
                    CASE_NOMINATIVE: "मी",
                    CASE_DATIVE: "मला",
                    CASE_INSTRUMENTAL: "माझ्याने",
                    CASE_LOCATIVE: "माझ्यात",
                    CASE_GENITIVE: "माझा",
                    CASE_ABLATIVE: "माझ्याहून",
                },
            ),
            "तो": LexemeEntry(
                "तो",
                POS_PRONOUN,
                "masculine",
                "IRREGULAR",
                overrides={
                    CASE_NOMINATIVE: "तो",
                    CASE_DATIVE: "त्याला",
                    CASE_INSTRUMENTAL: "त्याने",
                    CASE_LOCATIVE: "त्यात",
                    CASE_GENITIVE: "त्याचा",
                    CASE_ABLATIVE: "त्याहून",
                },
            ),
            "ती": LexemeEntry(
                "ती",
                POS_PRONOUN,
                "feminine",
                "IRREGULAR",
                overrides={
                    CASE_NOMINATIVE: "ती",
                    CASE_DATIVE: "तिला",
                    CASE_INSTRUMENTAL: "तिने",
                    CASE_LOCATIVE: "तिच्यात",
                    CASE_GENITIVE: "तिचा",
                    CASE_ABLATIVE: "तिच्याहून",
                },
            ),
            "चांगला": LexemeEntry("चांगला", POS_ADJECTIVE, "neutral", "INVARIANT"),
            "मोठा": LexemeEntry("मोठा", POS_ADJECTIVE, "neutral", "INVARIANT"),
        }

        self.rules: Dict[str, Dict[str, CaseRule]] = {
            "CONSONANT": {
                CASE_NOMINATIVE: CaseRule(CASE_NOMINATIVE, "", "", "Base dictionary form"),
                CASE_DATIVE: CaseRule(CASE_DATIVE, "", "ाला", "Add the dative marker"),
                CASE_INSTRUMENTAL: CaseRule(CASE_INSTRUMENTAL, "", "ाने", "Add the instrumental marker"),
                CASE_LOCATIVE: CaseRule(CASE_LOCATIVE, "", "ात", "Add the locative marker"),
                CASE_GENITIVE: CaseRule(CASE_GENITIVE, "", "ाचा", "Add the genitive marker"),
                CASE_ABLATIVE: CaseRule(CASE_ABLATIVE, "", "ाहून", "Add the ablative marker"),
            },
            "A_CLASS": {
                CASE_NOMINATIVE: CaseRule(CASE_NOMINATIVE, "", "", "Base dictionary form"),
                CASE_DATIVE: CaseRule(CASE_DATIVE, "ा", "ेला", "Delete final 'ा' and insert 'े'"),
                CASE_INSTRUMENTAL: CaseRule(CASE_INSTRUMENTAL, "ा", "ेने", "Delete final 'ा' and insert 'े'"),
                CASE_LOCATIVE: CaseRule(CASE_LOCATIVE, "ा", "ेत", "Delete final 'ा' and insert 'े'"),
                CASE_GENITIVE: CaseRule(CASE_GENITIVE, "ा", "ेची", "Delete final 'ा' and insert 'े'"),
                CASE_ABLATIVE: CaseRule(CASE_ABLATIVE, "ा", "ेहून", "Delete final 'ा' and insert 'े'"),
            },
            "IRREGULAR": {},
            "INVARIANT": {
                CASE_NOMINATIVE: CaseRule(CASE_NOMINATIVE, "", "", "Lexeme form"),
                CASE_DATIVE: CaseRule(CASE_DATIVE, "", "", "Adjective is kept invariant in this demo"),
                CASE_INSTRUMENTAL: CaseRule(CASE_INSTRUMENTAL, "", "", "Adjective is kept invariant in this demo"),
                CASE_LOCATIVE: CaseRule(CASE_LOCATIVE, "", "", "Adjective is kept invariant in this demo"),
                CASE_GENITIVE: CaseRule(CASE_GENITIVE, "", "", "Adjective is kept invariant in this demo"),
                CASE_ABLATIVE: CaseRule(CASE_ABLATIVE, "", "", "Adjective is kept invariant in this demo"),
            },
        }

    def validate_word(self, lemma: str) -> bool:
        """Checks whether a lemma exists in the lexicon.

        Args:
            lemma (str): Input lemma to validate.

        Returns:
            bool: True if the lemma exists, otherwise False.
        """
        return lemma in self.entries

    def get_entry(self, lemma: str) -> Optional[LexemeEntry]:
        """Returns the lexeme entry for a lemma if it exists.

        Args:
            lemma (str): Input lemma.

        Returns:
            Optional[LexemeEntry]: Matching entry or None.
        """
        return self.entries.get(lemma)

    def list_cases(self) -> List[str]:
        """Returns the supported case inventory.

        Returns:
            List[str]: Available case labels.
        """
        return CASES[:]

    def list_pos_tags(self) -> List[str]:
        """Returns the supported POS tags.

        Returns:
            List[str]: Available POS labels.
        """
        return POS_TAGS[:]

    def _genitive_suffix(self, entry: LexemeEntry) -> str:
        """Builds the genitive suffix for a lexeme entry.

        Args:
            entry (LexemeEntry): Lexeme metadata.

        Returns:
            str: Genitive suffix.
        """
        if entry.noun_class == "A_CLASS":
            return "ेची" if entry.gender == "feminine" else "ेचा"
        return "ाची" if entry.gender == "feminine" else "ाचा"

    def _default_surface(self, entry: LexemeEntry, case: str) -> Optional[str]:
        """Generates a surface form for a lemma-case pair.

        Args:
            entry (LexemeEntry): Lexeme metadata.
            case (str): Target grammatical case.

        Returns:
            Optional[str]: Surface form if a rule is available.
        """
        if entry.pos == POS_ADJECTIVE and entry.noun_class == "INVARIANT":
            return entry.lemma

        if entry.noun_class == "IRREGULAR":
            if case == CASE_NOMINATIVE:
                return entry.lemma
            return entry.overrides.get(case)

        if entry.noun_class == "A_CLASS":
            stem = entry.lemma[:-1] if entry.lemma.endswith("ा") else entry.lemma
            vowel = "े"
            if case == CASE_NOMINATIVE:
                return entry.lemma
            if case == CASE_DATIVE:
                return stem + vowel + "ला"
            if case == CASE_INSTRUMENTAL:
                return stem + vowel + "ने"
            if case == CASE_LOCATIVE:
                return stem + vowel + "त"
            if case == CASE_GENITIVE:
                return stem + self._genitive_suffix(entry)
            if case == CASE_ABLATIVE:
                return stem + vowel + "हून"
            return None

        if case == CASE_NOMINATIVE:
            return entry.lemma
        if case == CASE_DATIVE:
            return entry.lemma + "ाला"
        if case == CASE_INSTRUMENTAL:
            return entry.lemma + "ाने"
        if case == CASE_LOCATIVE:
            return entry.lemma + "ात"
        if case == CASE_GENITIVE:
            return entry.lemma + self._genitive_suffix(entry)
        if case == CASE_ABLATIVE:
            return entry.lemma + "ाहून"
        return None

    def generate(self, lemma: str, case: str, pos: Optional[str] = None) -> str:
        """Generates a surface form from a lemma and a case.

        Args:
            lemma (str): Input lemma.
            case (str): Target grammatical case.
            pos (Optional[str]): Optional POS filter.

        Returns:
            str: Generated surface form or error message.
        """
        if not self.validate_word(lemma):
            return f"[ERROR] '{lemma}' is not in the lexicon"

        if case not in CASES:
            return "[ERROR] Invalid case"

        entry = self.entries[lemma]
        if pos is not None and entry.pos != pos:
            return f"[ERROR] '{lemma}' is tagged as {entry.pos}, not {pos}"

        surface = self._default_surface(entry, case)

        if surface is None:
            return f"[ERROR] No rule available for '{lemma}' in case '{case}'"

        return f"{lemma} [{entry.pos}] + {case} -> {surface}"

    def analyze(self, surface_form: str, pos: Optional[str] = None) -> str:
        """Analyzes a surface form and returns its lemma and case.

        Args:
            surface_form (str): Observed word form.
            pos (Optional[str]): Optional POS filter.

        Returns:
            str: Analysis result or failure message.
        """
        for lemma, entry in self.entries.items():
            if pos is not None and entry.pos != pos:
                continue
            for case in CASES:
                generated = self._default_surface(entry, case)
                if generated == surface_form:
                    return f"{surface_form} -> Lemma: {lemma}, POS: {entry.pos}, Case: {case}"

        return f"{surface_form} -> No matching analysis found"

    def show_lexicon(self) -> None:
        """Prints the lexicon entries grouped by POS metadata."""
        print("\nLexicon by POS:")
        for lemma, entry in self.entries.items():
            print(f"- {lemma} | POS={entry.pos} | class={entry.noun_class} | gender={entry.gender}")

    def show_pos_inventory(self) -> None:
        """Prints the supported POS tags."""
        print("\nSupported POS tags:")
        for pos in POS_TAGS:
            print("-", pos)

    def show_case_study(self) -> None:
        """Prints the Marathi case study summary used by the project."""
        print("\nMarathi noun cases used in this project:")
        print("- Nominative: dictionary form / citation form")
        print("- Dative: recipient or goal, often marked with ला / ला-like forms")
        print("- Instrumental: means or agent, often marked with ने")
        print("- Locative: location, often marked with त")
        print("- Genitive: possession, often marked with चा / ची / चे")
        print("- Ablative: source or separation, often marked with हून")
        print("\nThe transducer below supports NOUN, PRONOUN, and ADJECTIVE entries.")

    def show_add_delete_table(self) -> None:
        """Prints the add/delete table for supported morphological classes."""
        print("\nAdd/Delete table for Marathi FST:")
        for noun_class, rules in self.rules.items():
            if not rules:
                continue
            print(f"\nClass: {noun_class}")
            print("Case | Delete | Add | Description")
            print("-" * 52)
            for case in CASES:
                rule = rules.get(case)
                if rule is None:
                    continue
                delete = rule.delete if rule.delete else "Ø"
                add = rule.add if rule.add else "Ø"
                print(f"{case} | {delete} | {add} | {rule.description}")
        print("\nIrregular nouns are handled through lexical overrides, which is a common way to model exceptions in FST-based systems.")

    def show_fst_summary(self) -> None:
        """Prints a compact finite-state summary of the model."""
        print("\nFinite-state model summary:")
        print("q0 -> q1 : read lemma and POS")
        print("q1 -> q2 : apply case-specific add/delete rule")
        print("q2 -> qf : output surface form")
        print("\nThis is a deterministic, rule-based transducer for multiple Marathi POS tags.")

    def demo(self) -> None:
        """Runs a small built-in demo of generation examples."""
        print("\nDemo: Marathi morphology generation")
        samples = [
            ("घर", CASE_DATIVE, POS_NOUN),
            ("गाव", CASE_GENITIVE, POS_NOUN),
            ("शाळा", CASE_LOCATIVE, POS_NOUN),
            ("विद्यार्थी", CASE_INSTRUMENTAL, POS_NOUN),
            ("मी", CASE_DATIVE, POS_PRONOUN),
            ("तो", CASE_GENITIVE, POS_PRONOUN),
            ("चांगला", CASE_NOMINATIVE, POS_ADJECTIVE),
        ]
        for lemma, case, pos in samples:
            print(self.generate(lemma, case, pos))


class UserInterface:
    """CLI for interacting with the Marathi morphology FST."""

    def __init__(self):
        """Initializes the CLI with the morphology engine."""
        self.fst = MarathiNounFST()

    def menu(self) -> None:
        """Displays the interactive command-line menu."""
        while True:
            print("\n====================================")
            print(" Marathi Morphology FST Model ")
            print("====================================")
            print("1. Study Marathi noun cases")
            print("2. Show add/delete table")
            print("3. Generate form")
            print("4. Analyze form")
            print("5. Show lexicon")
            print("6. Show POS tags")
            print("7. Run demo")
            print("8. Show FST summary")
            print("9. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.fst.show_case_study()
            elif choice == "2":
                self.fst.show_add_delete_table()
            elif choice == "3":
                self.generate_ui()
            elif choice == "4":
                self.analyze_ui()
            elif choice == "5":
                self.fst.show_lexicon()
            elif choice == "6":
                self.fst.show_pos_inventory()
            elif choice == "7":
                self.fst.demo()
            elif choice == "8":
                self.fst.show_fst_summary()
            elif choice == "9":
                print("Exiting...")
                sys.exit(0)
            else:
                print("[ERROR] Invalid choice")

    def generate_ui(self) -> None:
        """Collects input and prints the generated surface form."""
        lemma = input("Enter lemma: ").strip()
        print("Available POS tags:")
        for pos in POS_TAGS:
            print("-", pos)
        pos = input("Enter POS (blank to auto-detect): ").strip().upper()
        pos = pos if pos else None
        print("Available cases:")
        for case in CASES:
            print("-", case)
        case = input("Enter case: ").strip().upper()
        result = self.fst.generate(lemma, case, pos)
        print("Result:", result)

    def analyze_ui(self) -> None:
        """Collects input and prints the morphological analysis."""
        surface_form = input("Enter surface form: ").strip()
        print("Available POS tags:")
        for pos in POS_TAGS:
            print("-", pos)
        pos = input("Enter POS filter (blank for all): ").strip().upper()
        pos = pos if pos else None
        result = self.fst.analyze(surface_form, pos)
        print("Result:", result)


if __name__ == "__main__":
    UserInterface().menu()
