import os
import json
from typing import List, Dict, Any
from src.memory.schema import BookBrief, FullBook, MemoryState, BookOutline, ChapterContent, FactRecord, DecisionLogEntry, TonalityFingerprint
from src.agents.unified_agent import *
from src.assembler.pdf_gen import PDFGenerator
from src.assembler.docx_gen import DOCXGenerator
from src.utils.rag import RAGSystem
from src.evals.scorers import EvalScorer
from src.utils.llm import LLMInterface
from src.config import PRIMARY_MODEL
import re

def clean_json(text: str) -> str:
    """Strip markdown code blocks and whitespace."""
    if not text:
        return ""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    # Remove any leading/trailing characters that are not { or [
    match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

class Orchestrator:
    def __init__(self):
        self.llm = LLMInterface()
        self.planner = PlannerAgent(PRIMARY_MODEL)
        self.researcher = ResearcherAgent(PRIMARY_MODEL)
        self.writer = WriterAgent(PRIMARY_MODEL)
        self.humanizer = HumanizerAgent(PRIMARY_MODEL)
        self.editor = EditorAgent(PRIMARY_MODEL)
        self.fact_checker = FactCheckerAgent(PRIMARY_MODEL)
        self.memory_keeper = MemoryKeeperAgent(PRIMARY_MODEL)
        self.front_matter_agent = FrontMatterAgent(PRIMARY_MODEL)
        self.back_matter_agent = BackMatterAgent(PRIMARY_MODEL)
        self.rag = RAGSystem()
        self.evals = EvalScorer()
        self.pdf_gen = PDFGenerator()
        self.docx_gen = DOCXGenerator()

    def parse_json(self, raw_text: str, default: Any = None) -> Any:
        """Robust JSON parsing with cleaning and fallbacks."""
        cleaned = clean_json(raw_text)
        if not cleaned:
            return default
        try:
            return json.loads(cleaned)
        except Exception as e:
            print(f"[Orchestrator] JSON parsing error: {e}")
            print(f"Raw text provided: {raw_text[:200]}...")
            return default

    def run(self, brief: BookBrief) -> FullBook:
        #  Planning
        print(f"[Planner] Planning book: {brief.topic}")
        outline_raw = self.llm.call_llm(self.planner.execute(brief), PRIMARY_MODEL, json_mode=True)
        outline_data = self.parse_json(outline_raw)
        
        if not outline_data:
            print(f"[Orchestrator] Critical Error: Failed to generate book outline.")
            raise ValueError("Failed to generate book outline.")
            
        try:
            outline = BookOutline(**outline_data)
        except Exception as e:
            print(f"[Orchestrator] Error validating outline: {e}")
            raise
        
        book = FullBook(
            brief=brief,
            outline=outline,
            front_matter={},
            chapters=[],
            back_matter={},
            memory=MemoryState()
        )
        
        for ch_outline in outline.chapters:
            # Decision Log: Start chapter
            book.memory.decision_log.append(DecisionLogEntry(
                agent_name="Orchestrator",
                decision=f"Generating Chapter {ch_outline.chapter_number}",
                rationale="Continuing sequential generation",
                alternatives_considered=[],
                timestamp=str(os.path.getmtime(__file__)) # placeholder
            ))
            
            # Research with RAG
            rag_context = self.rag.query(ch_outline.title + " " + " ".join(ch_outline.key_points))
            research_json = self.llm.call_llm(self.researcher.execute(ch_outline, context=str(rag_context)))
            research_data = self.parse_json(research_json, default=[])
            research = [FactRecord(**f) for f in research_data] if isinstance(research_data, list) else []
            
            # Write Draft
            draft = self.llm.call_llm(self.writer.execute(ch_outline, research, book.memory, brief.tonality.value))
            
            # Humanize
            humanized = self.llm.call_llm(self.humanizer.execute(draft, brief.tonality.value))
            
            # Edit
            edited = self.llm.call_llm(self.editor.execute(humanized, ch_outline.chapter_number))
            
            # Fact Check
            fact_check_report = self.llm.call_llm(self.fact_checker.execute(edited, research))
            # In a real system, we would handle failures here. For now, we log it.
            print(f"[{self.fact_checker.name}] Report: {fact_check_report}")
            
            # Update Memory
            memory_update_json = self.llm.call_llm(self.memory_keeper.execute(edited, book.memory, ch_outline.chapter_number))
            memory_update_data = self.parse_json(memory_update_json)
            if memory_update_data:
                try:
                    book.memory = MemoryState(**memory_update_data)
                except Exception as e:
                    print(f"[Orchestrator] Memory validation failed: {e}")
            else:
                print(f"[Orchestrator] Skipping memory update due to parsing failure.")
            
            # Tonality Fingerprint (Simulated scoring for now)
            book.memory.tonality_fingerprint.append(TonalityFingerprint(
                chapter_number=ch_outline.chapter_number,
                lexical_density=0.45,
                sentence_variety_score=0.8,
                metaphor_count=3,
                ai_tell_count=0,
                dominant_tone=brief.tonality.value,
                examples=["Example humanized sentence..."]
            ))
            
            # Store Chapter
            book.chapters.append(ChapterContent(
                chapter_number=ch_outline.chapter_number,
                title=ch_outline.title,
                content=edited,
                summary=ch_outline.summary,
                metadata={"research": [f.model_dump() for f in research]}
            ))
            
        #  Matter Generation
        front_raw = self.llm.call_llm(self.front_matter_agent.execute(brief, outline))
        book.front_matter = self.parse_json(front_raw, default={"title": outline.title, "note": "Generated with default front matter due to parsing error."})
        
        back_raw = self.llm.call_llm(self.back_matter_agent.execute(brief, outline, book.memory))
        book.back_matter = self.parse_json(back_raw, default={"appendix": "Included.", "note": "Generated with default back matter due to parsing error."})
        
        #  Evals Run
        # Final tonality check on a sample of chapters
        if book.chapters:
            sample_prose = book.chapters[0].content
            fidelity = self.evals.check_tonality_fidelity(sample_prose, brief.tonality.value, self.llm)
            print(f"[Evals] Tonality Fidelity ({brief.tonality.value}): {fidelity}")

        eval_results = self.evals.check_structural_completeness(book.model_dump())
        print(f"[Evals] Structural Completeness: {eval_results}")

        #  Assemble and Save
        print(f"[Assembler] Generating PDF and DOCX...")
        self.pdf_gen.generate(book)
        self.docx_gen.generate(book)
        
        #  Final Traces Collection
        book.traces = self.llm.get_logs()["traces"]
        
        return book

    def repair_pipeline(self, book: FullBook, inserted_chapter_index: int) -> FullBook:
        """Test D: Self-healing repair logic for chapter insertion."""
        print(f"[Orchestrator] Triggering self-healing repair for chapter insertion at index {inserted_chapter_index}")
        
        #  Update Chapter Numbers for all subsequent chapters
        for i in range(inserted_chapter_index + 1, len(book.chapters)):
            book.chapters[i].chapter_number = i + 1
            
        #  Re-run Memory Keeper for the new chapter and all subsequent ones to fix continuity
        for i in range(inserted_chapter_index, len(book.chapters)):
            ch = book.chapters[i]
            memory_update_json = self.llm.call_llm(self.memory_keeper.execute(ch.content, book.memory, ch.chapter_number))
            try:
                book.memory = MemoryState(**json.loads(memory_update_json))
            except Exception:
                pass
                
        #  Regenerate Back Matter (Glossary/Index) to include new terms
        new_back_json = self.llm.call_llm(self.back_matter_agent.execute(book.brief, book.outline, book.memory))
        book.back_matter = json.loads(new_back_json)
        
        return book
