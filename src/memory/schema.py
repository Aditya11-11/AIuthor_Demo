from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum

class TonalityPreset(str, Enum):
    CONVERSATIONAL = "Conversational"
    ACADEMIC = "Academic"
    STORYTELLER = "Storyteller"
    MOTIVATIONAL = "Motivational"
    WITTY = "Witty"

class BookBrief(BaseModel):
    topic: str
    reader_profile: str
    length: str
    tonality: TonalityPreset
    genre: str
    additional_requirements: Optional[str] = None

class ChapterOutline(BaseModel):
    chapter_number: int
    title: str
    summary: str
    key_points: List[str]
    estimated_word_count: int

class BookOutline(BaseModel):
    title: str
    front_matter_plan: List[str]
    chapters: List[ChapterOutline]
    back_matter_plan: List[str]

class FactRecord(BaseModel):
    fact: str
    source: Optional[str] = None
    confidence: float
    verified: bool = False

class CharacterRecord(BaseModel):
    name: str
    description: str
    traits: List[str]
    arc: Optional[str] = None

class Callback(BaseModel):
    id: str
    context: str
    content: str
    chapter_source: int
    used_in_chapters: List[int] = []

class TonalityFingerprint(BaseModel):
    chapter_number: int
    lexical_density: float
    sentence_variety_score: float
    metaphor_count: int
    ai_tell_count: int
    dominant_tone: str
    examples: List[str]

class DecisionLogEntry(BaseModel):
    agent_name: str
    decision: str
    rationale: str
    alternatives_considered: List[str]
    timestamp: str

class MemoryState(BaseModel):
    fact_registry: List[FactRecord] = []
    character_bible: List[CharacterRecord] = []
    callback_index: List[Callback] = []
    tonality_fingerprint: List[TonalityFingerprint] = []
    decision_log: List[DecisionLogEntry] = []

class AgentTrace(BaseModel):
    agent_name: str
    timestamp: str
    input: Any
    output: Any
    tokens_used: int
    cost: float
    logs: List[str] = []

class ChapterContent(BaseModel):
    chapter_number: int
    title: str
    content: str
    summary: str
    metadata: Dict[str, Any] = {}

class FullBook(BaseModel):
    brief: BookBrief
    outline: BookOutline
    front_matter: Dict[str, str]
    chapters: List[ChapterContent]
    back_matter: Dict[str, str]
    memory: MemoryState
    traces: List[AgentTrace] = []
