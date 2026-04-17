# AIuthor Architecture Specification

## 1. Orchestration Topology
Orchestrator-Worker pattern.

```mermaid
graph TD
    A[User Brief] --> B[Orchestrator]
    B --> C[Planner Agent]
    D[Chapter Unit] --> E[Researcher]
    E --> F[Writer]
    F --> G[Humanizer]
    G --> H[Editor]
    H --> I[Fact-Checker]
    I --> J[Memory Keeper]
    J --> B
    B --> K[Assembler]
```

## 2. Model Routing Strategy
All components now use Gemini via `google.genai` SDK.
- Generation: `gemini-2.0-flash`
- Embeddings: `text-embedding-004`

## 3. Self-Healing
Repair logic for chapter insertion handles TOC and Glossary regeneration.
