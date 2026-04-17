# AIuthor - Agentic Book Writing System

AIuthor is an advanced multi-agent system designed to produce publication-ready books from a simple brief. It features grounded research, tonality presets, memory across chapters, and a dedicated humanizer to eliminate "AI tells."

## Architecture

The system uses an **Orchestrator-Worker** pattern:
1. **Planner**: Outlines the book.
2. **Researcher**: Gathers facts (RAG-ready).
3. **Writer**: Drafts chapters using memory and tonality.
4. **Humanizer**: Refines prose to sound human.
5. **Editor**: Polishes for flow and consistency.
6. **Fact-Checker**: Validates claims.
7. **Memory Keeper**: Maintains character bibels and callback indexes.
8. **Assembler**: Generates PDF and DOCX.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --topic "Personal Finance for Beginners" --reader "College Graduates" --tonality "Conversational"
```

## Features

- **Memory across chapters**: Fact registry and callback index ensure continuity.
- **Tonality Presets**: 5 specific tones (Conversational, Academic, Storyteller, Motivational, Witty).
- **Observability**: Detailed traces and cost logs for every run.
```
