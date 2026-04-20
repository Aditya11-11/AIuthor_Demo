import os
import sys
from src.orchestration.orchestrator import Orchestrator
from src.memory.schema import BookBrief, TonalityPreset, FullBook, ChapterContent, ChapterOutline, FactRecord

def run_test_a():
    print("\n=== RUNNING TEST A: 5-chapter personal finance guide ===")
    brief = BookBrief(
        topic="Beginner's Guide to Personal Finance",
        reader_profile="Young adults and students new to financial planning",
        length="10 chapters",
        tonality=TonalityPreset.CONVERSATIONAL,
        genre="Non-fiction"
    )
    orchestrator = Orchestrator()
    book = orchestrator.run(brief)
    print(f"Test A Complete. Book Title: {book.outline.title}")
    return book

def run_test_b():
    print("\n=== RUNNING TEST B: 5-chapter novella ===")
    brief = BookBrief(
        topic="The Silent Key: A Cyberpunk Mystery",
        reader_profile="Fans of noir and high-tech dystopias",
        length="5 chapters",
        tonality=TonalityPreset.STORYTELLER,
        genre="Novella"
    )
    orchestrator = Orchestrator()
    book = orchestrator.run(brief)
    print(f"Test B Complete. Book Title: {book.outline.title}")
    return book

def run_test_c(book_a: FullBook):
    print("\n=== RUNNING TEST C: Regenerate Test A Chapter 3 in 3 Tones ===")
    orchestrator = Orchestrator()
    ch3_outline = book_a.outline.chapters[2]
    ch3_content = book_a.chapters[2]
    research_raw = ch3_content.metadata.get("research", [])
    research = [FactRecord(**f) for f in research_raw]
    
    tones = ["Academic", "Motivational", "Witty"]
    for tone in tones:
        print(f"Generating version for tone: {tone}")
        # Writer
        draft = orchestrator.llm.call_llm(orchestrator.writer.execute(ch3_outline, research, book_a.memory, tone))
        # Humanize
        humanized = orchestrator.llm.call_llm(orchestrator.humanizer.execute(draft, tone))
        # Edit
        edited = orchestrator.llm.call_llm(orchestrator.editor.execute(humanized, 3))
        
        filename = f"output/test_c_ch3_{tone.lower()}.txt"
        os.makedirs("output", exist_ok=True)
        with open(filename, "w") as f:
            f.write(edited)
        print(f"Saved to {filename}")

def run_test_d(book_a: FullBook):
    print("\n=== RUNNING TEST D: Insert chapter and verify self-healing ===")
    orchestrator = Orchestrator()
    new_ch_outline = ChapterOutline(
        chapter_number=5,
        title="Hidden Costs of Credit",
        summary="Deep dive into interest rates and credit scores.",
        key_points=["APR explained", "Compound interest", "Credit score maintenance"],
        estimated_word_count=2000
    )
    
    book_a.outline.chapters.insert(4, new_ch_outline)
    for i in range(5, len(book_a.outline.chapters)):
        book_a.outline.chapters[i].chapter_number = i + 1
        
    print(f"Generating content for new Chapter 5...")
    research_json = orchestrator.llm.call_llm(orchestrator.researcher.execute(new_ch_outline))
    research_data = orchestrator.parse_json(research_json, default=[])
    research = [FactRecord(**f) for f in research_data] if isinstance(research_data, list) else []
    
    print(f"Writing content for new Chapter 5...")
    draft = orchestrator.llm.call_llm(orchestrator.writer.execute(new_ch_outline, research, book_a.memory, book_a.brief.tonality.value))
    humanized = orchestrator.llm.call_llm(orchestrator.humanizer.execute(draft, book_a.brief.tonality.value))
    edited = orchestrator.llm.call_llm(orchestrator.editor.execute(humanized, 5))
    
    book_a.chapters.insert(4, ChapterContent(
        chapter_number=5,
        title=new_ch_outline.title,
        content=edited,
        summary=new_ch_outline.summary,
        metadata={"research": [f.model_dump() for f in research]}
    ) )
    
    repaired_book = orchestrator.repair_pipeline(book_a, 4)
    print("Test D Complete. Self-healing complete.")
    
    for i, ch in enumerate(repaired_book.chapters):
        print(f"Chapter {ch.chapter_number}: {ch.title}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python test_suite.py [a|b|c|d|all]")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    
    if cmd == "a":
        run_test_a()
    elif cmd == "b":
        run_test_b()
    elif cmd == "c":
        book_a = run_test_a()
        run_test_c(book_a)
    elif cmd == "d":
        book_a = run_test_a()
        run_test_d(book_a)
    elif cmd == "all":
        book_a = run_test_a()
        run_test_b()
        run_test_c(book_a)
        run_test_d(book_a)
