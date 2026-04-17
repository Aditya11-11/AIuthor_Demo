from src.memory.schema import FullBook, ChapterContent, MemoryState
import os

class AssemblerAgent:
    def __init__(self):
        pass

    def assemble(self, book: FullBook) -> str:
        # This will be replaced by actual PDF/DOCX generation
        print(f"[Assembler] Assembling book: {book.outline.title}")
        output_path = os.path.join("output", f"{book.outline.title.replace(' ', '_')}.txt")
        
        with open(output_path, "w") as f:
            f.write(f"# {book.outline.title}\n\n")
            f.write("## Front Matter\n")
            for k, v in book.front_matter.items():
                f.write(f"### {k.capitalize()}\n{v}\n\n")
            
            f.write("## Chapters\n")
            for ch in book.chapters:
                f.write(f"### Chapter {ch.chapter_number}: {ch.title}\n{ch.content}\n\n")
                
            f.write("## Back Matter\n")
            for k, v in book.back_matter.items():
                f.write(f"### {k.capitalize()}\n{v}\n\n")
                
        return output_path
