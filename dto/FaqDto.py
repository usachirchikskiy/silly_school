from dataclasses import dataclass

@dataclass
class FaqDto:
    id: int
    question: str
    answer: str