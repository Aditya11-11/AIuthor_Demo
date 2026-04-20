import argparse
import sys
from src.memory.schema import BookBrief, TonalityPreset
from src.orchestration.orchestrator import Orchestrator

def main():
    parser = argparse.ArgumentParser(description="AIuthor - Agentic Book Writing System")
    parser.add_argument("--topic", required=True, help="Topic of the book")
    parser.add_argument("--reader", required=True, help="Target reader profile")
    parser.add_argument("--length", default="10 chapters", help="Length description (e.g., '10 chapters', '5 chapters')")
    parser.add_argument("--tonality", default="Conversational", choices=[t.value for t in TonalityPreset], help="Tonality preset")
    parser.add_argument("--genre", default="Non-fiction", help="Genre of the book")
    
    args = parser.parse_args()

    brief = BookBrief(
        topic=args.topic,
        reader_profile=args.reader,
        length=args.length,
        tonality=TonalityPreset(args.tonality),
        genre=args.genre
    )

    print(f"Starting AIuthor for topic: {brief.topic}") 
    print(f"Tonality: {brief.tonality}")
    
    orchestrator = Orchestrator()
    book = orchestrator.run(brief)
    
    print(f"Book generation complete! Saved to output/")

if __name__ == "__main__":
    main()
