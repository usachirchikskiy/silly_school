from dataclasses import dataclass
from typing import List

from dto.TeacherDto import TeacherDto


@dataclass
class DepartmentDto:
    id: int
    name: str
    photo: str
    description: str
    teachers: List[TeacherDto]