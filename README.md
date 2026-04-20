# AIuthor - Execution Docs

AIuthor is an agentic book writing system. To run it, follow these steps:

## 1. Setup
Install requirements:
```bash
pip install -r requirements.txt
```

## 2. API Key
Create a `.env` file in the root directory and add your key:
```text
GOOGLE_API_KEY=your_key_here
PRIMARY_MODEL=Gemine_model
```

## 3. Run
Generate a book with a single command:
```bash
python3 main.py --topic "The Future of AI" --reader "General Public" --length 3 --tonality "Motivational"
```

## 4. System Test Suite
AIuthor Test cases for assingment(single line execution)
python3 test_suite.py [a|b|c|d|all]
```
- **Test A:** 10-chapter personal finance guide (Conversational tone, ~2,500 words/chapter).()
- **Test B:** 5-chapter novella (Storyteller tone, character consistency check).
- **Test C:** Regenerates Chapter 3 of Test A in **Academic**, **Motivational**, and **Witty** tones using existing research.
- **Test D:** Inserts a new chapter between Chapters 4 and 5 of Test A, triggering the **self-healing pipeline** for TOC, callbacks, and glossary.

All test outputs are saved in the `output/` directory.
For deep technical details, see [documentation.md](documentation.md).
