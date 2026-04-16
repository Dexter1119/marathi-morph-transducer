# 🚀 Marathi Morphological FST Engine

### *Finite State Transducer for Marathi Case Morphology*

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![NLP](https://img.shields.io/badge/Domain-NLP-green.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)
![License](https://img.shields.io/badge/License-Academic-orange.svg)

---

## 📌 Project Overview

This project implements a **Finite State Transducer (FST)** to model **Marathi morphological case inflection** for multiple POS tags, with a primary focus on **NOUN morphology**.

It demonstrates how **rule-based NLP systems** can effectively handle **morphologically rich Indian languages** using a structured **add/delete table approach**.

---

## ✨ Key Features

✔ Morphological **generation** (lemma → inflected form)
✔ Morphological **analysis** (word → lemma + case)
✔ Support for **multiple POS tags**
✔ **Add/Delete Table-based FST implementation**
✔ Handles **regular + irregular nouns**
✔ CLI-based interactive system
✔ GUI support (Tkinter)

---

## 🧠 Abstract

This project presents a compact yet effective **Finite State Transducer model** for Marathi morphology. It focuses on **noun case inflection**, while also supporting **pronouns and adjectives**.

The system uses:

* A **lexicon**
* A **rule-based morphotactic model**
* A **deterministic mapping system**

This makes it ideal for:

* NLP lab assignments
* Academic demonstrations
* Morphological analysis research

---

## 📚 Supported POS Tags

* 🟢 NOUN (Primary)
* 🔵 PRONOUN
* 🟣 ADJECTIVE

---

## 🔷 Marathi Morphological Cases

| Case               | Function   | Example   |
| ------------------ | ---------- | --------- |
| Nominative (कर्ता) | Subject    | गाव       |
| Accusative (कर्म)  | Object     | गावाला    |
| Instrumental (करण) | By/With    | गावाने    |
| Dative (सम्प्रदान) | To/For     | गावाला    |
| Ablative (अपादान)  | From       | गावापासून |
| Genitive (सम्बंध)  | Possession | गावाचा    |
| Locative (अधिकरण)  | In/At      | गावात     |
| Vocative (संबोधन)  | Addressing | अरे गाव   |

---

## ⚙️ Add/Delete Table (Core FST Logic)

### 🔹 Consonant-final nouns

Examples: घर, गाव, शहर

| Case         | Delete | Add  | Example |
| ------------ | ------ | ---- | ------- |
| Dative       | Ø      | ाला  | घराला   |
| Instrumental | Ø      | ाने  | घराने   |
| Locative     | Ø      | ात   | घरात    |
| Genitive     | Ø      | ाचा  | घराचा   |
| Ablative     | Ø      | ाहून | घराहून  |

---

### 🔹 A-class nouns

Example: शाळा

| Case         | Delete | Add | Example |
| ------------ | ------ | --- | ------- |
| Dative       | ा      | ेला | शाळेला  |
| Instrumental | ा      | ेने | शाळेने  |
| Locative     | ा      | ेत  | शाळेत   |
| Genitive     | ा      | ेची | शाळेची  |

---

### 🔹 Irregular nouns

Handled via **lexical overrides**

| Lemma      | Dative         | Instrumental   | Genitive       |
| ---------- | -------------- | -------------- | -------------- |
| मुलगा      | मुलाला         | मुलाने         | मुलाचा         |
| मुलगी      | मुलीला         | मुलीने         | मुलीची         |
| विद्यार्थी | विद्यार्थ्याला | विद्यार्थ्याने | विद्यार्थ्याचा |

---

## ⚙️ Algorithm (FST Workflow)

```text
1. Input lemma
2. Identify noun class
3. Select case rule
4. Apply Add/Delete operation
5. Output inflected form
```

### Reverse Analysis:

```text
1. Input word
2. Match suffix patterns
3. Extract root
4. Return lemma + case
```

---

## 🔁 Input / Output Examples

### ▶ Generation

```text
Input:
lemma = गाव
case = GENITIVE

Output:
गाव + GENITIVE → गावाचा
```

---

### ▶ Analysis

```text
Input:
शाळेत

Output:
Lemma: शाळा
POS: NOUN
Case: LOCATIVE
```

---

## 🧪 Sample Outputs

```text
घर [NOUN] + DATIVE → घराला
गाव [NOUN] + GENITIVE → गावाचा
मी [PRONOUN] + DATIVE → मला
चांगला [ADJECTIVE] + NOMINATIVE → चांगला
```

---

## 🖥️ How to Run

```bash
python marathi_fst_system.py
```

### Menu Options:

* Generate word
* Analyze word
* Show vocabulary
* View case rules
* Run demo

---

## 🏗️ Project Structure

```
📁 Project
│── marathi_fst_system.py   # Core FST engine + CLI
│── marathi_fst_gui.py      # GUI interface (Tkinter)
│── README.md               # Documentation
```

---

## 🧩 System Architecture

```
Lexicon → FST Rules → Add/Delete Table → Output
```

---

## 🧠 Why This is FST?

✔ Finite rule system
✔ Deterministic transitions
✔ Input → Output mapping
✔ State-like behavior

---

## 🎯 Applications

* NLP preprocessing
* Morphological analyzers
* Machine Translation
* Information Retrieval
* Language learning tools

---

## 📊 Scope

This is a **compact educational model**, not a full industrial morphological analyzer.

✔ Covers major case inflections
❌ Does not cover full grammar complexity

---

## 📌 References

*  (Project Base Document)
* IIIT-H NLP Virtual Labs
* Marathi Morphology Research Papers

---

## 🎓 Conclusion

This project proves that **Marathi morphology can be effectively modeled using FST principles**.

The combination of:

* Add/Delete rules
* Lexicon-based control
* Deterministic transitions

makes it:
✔ Simple
✔ Explainable
✔ Extendable

---

## 👨‍💻 Author

**Pradhumnya Changdev Kalsait**
Computer Engineering (BE)
NLP | AI Enthusiast

---

## ⭐ Future Enhancements

* 🔹 Plural handling
* 🔹 Gender agreement
* 🔹 Deep learning hybrid model
* 🔹 Web-based UI
* 🔹 Large-scale corpus integration

---

✨ *If you found this project useful, consider starring the repository!*
