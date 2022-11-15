from dataclasses import dataclass

@dataclass
class NewsDto:
    id: int
    datetime_posted: str
    name: str
    photo: str
    description: str