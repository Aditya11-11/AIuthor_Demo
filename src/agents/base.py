from abc import ABC, abstractmethod
from typing import Any, Dict
from src.memory.schema import AgentTrace
import datetime

class BaseAgent(ABC):
    def __init__(self, name: str, model_name: str):
        self.name = name
        self.model_name = model_name

    @abstractmethod
    def execute(self, input_data: Any, context: Dict[str, Any]) -> Any:
        pass

    def create_trace(self, input_data: Any, output_data: Any, tokens: int, cost: float, logs: list) -> AgentTrace:
        return AgentTrace(
            agent_name=self.name,
            timestamp=datetime.datetime.now().isoformat(),
            input=input_data,
            output=output_data,
            tokens_used=tokens,
            cost=cost,
            logs=logs
        )
