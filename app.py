import streamlit as st
import sys
import os

# Ensure the root directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.memory.schema import BookBrief, TonalityPreset
from src.orchestration.orchestrator import Orchestrator

st.set_page_config(page_title="AIuthor Dashboard", page_icon="📚", layout="wide")

def main():
    st.title("📚 AIuthor - Agentic Book Writing System")
    st.markdown("Generate a complete book using multi-agent orchestration.")
    
    with st.sidebar:
        st.header("Book Configuration")
        topic = st.text_input("Topic of the book", "Artificial Intelligence")
        reader = st.text_input("Target reader profile", "General Audience")
        length = st.text_input("Length description", "3 chapters")
        
        tonality_options = [t.value for t in TonalityPreset]
        tonality = st.selectbox("Tonality preset", tonality_options)
        
        genre = st.text_input("Genre of the book", "Non-fiction")
        
        generate_btn = st.button("Generate Book", type="primary")

    if generate_btn:
        st.info(f"Starting AIuthor for topic: {topic}")
        
        brief = BookBrief(
            topic=topic,
            reader_profile=reader,
            length=length,
            tonality=TonalityPreset(tonality),
            genre=genre
        )
        
        try:
            orchestrator = Orchestrator()
            with st.spinner("Generating book... This entails planning, researching, writing, and editing. It may take a while."):
                book = orchestrator.run(brief)
            
            st.success("Book generation complete! Saved to output/")
            
            st.subheader("Generated Book Outline")
            st.json(book.outline.model_dump())

            st.subheader("Chapters Summary")
            for chapter in book.chapters:
                with st.expander(f"Chapter {chapter.chapter_number}: {chapter.title}"):
                    st.markdown(f"**Summary:** {chapter.summary}")
                    st.markdown("**Content Preview (first 500 chars):**")
                    st.text(chapter.content[:500] + "...")
                        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)
    else:
        st.info("👈 Configure the book in the sidebar and click **Generate Book** to start.")
        
        st.markdown("""
        ### Features:
        - Multi-agent architecture for planning, researching, writing, and editing
        - RAG-powered research
        - Automated PDF and DOCX generation
        """)

if __name__ == "__main__":
    main()
