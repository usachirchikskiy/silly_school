from dataclasses import dataclass


@dataclass
class AdministrationDto:
    id: int
    name: str
    photo: str
    profession: str