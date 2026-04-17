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

All generated files will be in the `output/` directory.
For deep technical details, see [documentation.md](documentation.md).
