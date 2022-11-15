from dataclasses import dataclass

@dataclass
class TeacherDto:
    id: int
    photo: str
    name: str
    timetable: str
    department_id: str