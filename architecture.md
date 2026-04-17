# AIuthor Architecture Specification

## 1. Data Flow
`Orchestrator` -> `Agents` -> `Memory State` -> `Assembler`

## 2. RAG System
`ChromaDB` storing semantic chunks embedded via Gemini `text-embedding-004`.

## 3. Self-Healing
Downstream repair logic for Table of Contents and Glossary ensures integrity after manual chapter insertion.
