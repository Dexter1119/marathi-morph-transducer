# Marathi Noun Morphology FST

## Project Overview
This project models Marathi morphological case handling for a single part of speech: **NOUN**. It implements a simple **Finite State Transducer (FST)** style analyzer and generator using an **add/delete table** approach inspired by standard NLP laboratory demonstrations.

The system can:
- generate surface forms from noun lemmas and grammatical cases,
- analyze surface forms back into lemma + case,
- display a case study for Marathi noun morphology,
- display the add/delete table used by the transducer.

## Abstract
This project presents a compact finite state transducer model for Marathi morphology. It now covers multiple POS tags, with **NOUN** as the main focus and additional support for **PRONOUN** and **ADJECTIVE** entries. The system demonstrates how Marathi case inflection can be modeled using an explicit add/delete table, a small lexicon, and deterministic generation and analysis rules. The system is designed as a submission-ready NLP lab exercise rather than a full-scale morphological analyzer.

## Scope
This submission focuses on case-based Marathi morphology with a compact multi-POS design. It does not attempt to solve full Marathi morphology or all possible POS tags. The design is intentionally compact and pedagogical so it is easy to present in a lab or assignment.

## Supported POS Tags
- NOUN
- PRONOUN
- ADJECTIVE

## Marathi Noun Cases Used
The following cases are included in the model:

| Case | Function | Typical Marker |
| --- | --- | --- |
| Nominative | Dictionary form | None |
| Dative | Recipient / goal | ला / ला-like forms |
| Instrumental | Means / agent | ने |
| Locative | Location | त |
| Genitive | Possession | चा / ची / चे |
| Ablative | Source / separation | हून |

## Add/Delete Table
The FST uses class-based morphotactics.

### 1. Consonant-final nouns
Examples: घर, गाव, शहर, पुस्तक, भारत

| Case | Delete | Add | Example |
| --- | --- | --- | --- |
| Nominative | Ø | Ø | घर |
| Dative | Ø | ाला | घराला |
| Instrumental | Ø | ाने | घराने |
| Locative | Ø | ात | घरात |
| Genitive | Ø | ाचा / ाची | घराचा |
| Ablative | Ø | ाहून | घराहून |

### 2. A-class nouns
Examples: शाळा

| Case | Delete | Add | Example |
| --- | --- | --- | --- |
| Nominative | Ø | Ø | शाळा |
| Dative | ा | ेला | शाळेला |
| Instrumental | ा | ेने | शाळेने |
| Locative | ा | ेत | शाळेत |
| Genitive | ा | ेचा / ेची | शाळेची |
| Ablative | ा | ेहून | शाळेहून |

### 3. Irregular nouns
Examples: मुलगा, मुलगी, विद्यार्थी

These forms are handled using lexical overrides because Marathi contains lexically irregular noun patterns that do not follow a single productive suffix rule.

| Lemma | Dative | Instrumental | Locative | Genitive | Ablative |
| --- | --- | --- | --- | --- | --- |
| मुलगा | मुलाला | मुलाने | मुलात | मुलाचा | मुलाहून |
| मुलगी | मुलीला | मुलीने | मुलीत | मुलीची | मुलीहून |
| विद्यार्थी | विद्यार्थ्याला | विद्यार्थ्याने | विद्यार्थ्यात | विद्यार्थ्याचा | विद्यार्थ्याहून |

## Algorithm Notes
The transducer is implemented as a deterministic rule system:

1. Read the noun lemma from the lexicon.
2. Identify the noun class:
   - `CONSONANT`
   - `A_CLASS`
   - `IRREGULAR`
3. Select the case rule from the add/delete table.
4. Apply the rule to produce the surface form.
5. For analysis, compare the given surface form against the generated forms and return the matching lemma + case.

### Why this is FST-style
- The model maps lexical input to surface output.
- The mapping is state-like and deterministic.
- The rule set is explicit and finite.
- Exceptions are handled separately with lexical overrides, which is standard in practical morphology systems.

## Input and Output Behavior
### Generation
Input:
- lemma: घर
- case: DATIVE

Output:
- घर + DATIVE -> घराला

### Analysis
Input:
- surface form: शाळेत

Output:
- शाळेत -> Lemma: शाळा, POS: NOUN, Case: LOCATIVE

## Sample Outputs
Example demo results from the script:

```text
घर [NOUN] + DATIVE -> घराला
गाव [NOUN] + GENITIVE -> गावाचा
मी [PRONOUN] + DATIVE -> मला
चांगला [ADJECTIVE] + NOMINATIVE -> चांगला
```

Example analysis results:

```text
घराला -> Lemma: घर, POS: NOUN, Case: DATIVE
मला -> Lemma: मी, POS: PRONOUN, Case: DATIVE
चांगला -> Lemma: चांगला, POS: ADJECTIVE, Case: NOMINATIVE
```

## How to Run
Run the program with Python:

```bash
python marathi_fst_system.py
```

Then choose one of the menu options to:
- study the Marathi noun cases,
- show the add/delete table,
- generate noun forms,
- analyze noun forms,
- view the lexicon,
- run the sample demo.

## Class Structure
The project uses a small class-based design:

| Class | Responsibility |
| --- | --- |
| `MarathiNounFST` | Core finite state transducer logic for generation, analysis, lexicon lookup, and table display |
| `UserInterface` | CLI wrapper for menu-driven interaction with the FST engine |

The main engine stores the lexicon, case rules, and surface-form mappings. The user interface class keeps interaction separate from the morphology logic, which makes the project easier to test and present.

## File Format
The code follows a consistent Python project format:

1. File header at the top of each Python file.
2. Module docstring describing the purpose of the file.
3. Class headers for major classes.
4. Function/method docstrings for important behavior.
5. PEP 8-aligned naming and indentation.

Current project files:

- [marathi_fst_system.py](marathi_fst_system.py) - Core FST engine and CLI menu
- [marathi_fst_gui.py](marathi_fst_gui.py) - Tkinter GUI for the same engine
- [README.md](README.md) - Project report and documentation

## File Structure
- [marathi_fst_system.py](marathi_fst_system.py) - Main FST implementation and CLI menu
- [README.md](README.md) - Project documentation

## Submission Notes
This package is now suitable for submission as a compact Marathi morphology FST demo focused on noun case inflection. The README gives the linguistic background, rule table, algorithm summary, and sample outputs needed for presentation or review.

## References
1. IIIT-H Virtual Labs, Natural Language Processing. Available at: [https://nlp-iiith.vlabs.ac.in/](https://nlp-iiith.vlabs.ac.in/)
2. IIIT-H Virtual Labs reference material on add/delete table based finite state transducers.
3. Marathi morphology lecture and lab notes used for noun case modeling and transducer design.

## Conclusion
This project demonstrates that Marathi noun case morphology can be modeled cleanly with a finite state transducer style approach. The add/delete table makes the morphology easy to explain, the lexicon keeps the system deterministic, and lexical overrides provide a practical way to handle irregular forms. The result is a compact, submission-ready NLP artifact that is easy to demonstrate and extend.
