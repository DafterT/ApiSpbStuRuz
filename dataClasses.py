"""File with some data classes"""
import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Faculty:
    id: int
    name: str
    abbr: str


@dataclass(frozen=True)
class Group:
    id: int
    name: str
    level: int
    type: str
    kind: int
    spec: str
    year: int


@dataclass(frozen=True)
class Teacher:
    id: int
    oid: int
    full_name: str
    first_name: str
    middle_name: str
    last_name: str
    grade: str
    chair: str


@dataclass(frozen=True, init=False)
class Date:
    year: int
    month: int
    day: int

    def __init__(self, date: str):
        year, month, day = map(int, re.findall(r'\d+', date))
        object.__setattr__(self, "year", year)
        object.__setattr__(self, "month", month)
        object.__setattr__(self, "day", day)


@dataclass(frozen=True)
class Week:
    date_start: Date | str
    date_end: Date | str
    is_odd: bool

    def __post_init__(self):
        object.__setattr__(self, "date_start", Date(self.date_start))
        object.__setattr__(self, "date_end", Date(self.date_end))


@dataclass(frozen=True, init=False)
class Time:
    hour: int
    minute: int

    def __init__(self, time: str):
        hour, minute = map(int, time.split(':'))
        object.__setattr__(self, "hour", hour)
        object.__setattr__(self, "minute", minute)


@dataclass(frozen=True)
class TypeObj:
    id: int
    name: str
    abbr: str


@dataclass(frozen=True)
class Group:
    id: int
    name: str
    level: int
    type: str
    kind: int
    spec: str
    year: int
    faculty: Faculty | dict

    def __post_init__(self):
        object.__setattr__(self, "faculty", Faculty(**self.faculty))


@dataclass(frozen=True)
class Building:
    id: int
    name: str
    abbr: str
    address: str


@dataclass(frozen=True)
class Auditory:
    id: int
    name: str
    building: Building | dict

    def __post_init__(self):
        object.__setattr__(self, "building", Building(**self.building))


@dataclass(frozen=True)
class Lesson:
    subject: str
    subject_short: str
    type: int
    additional_info: str
    time_start: Time | str
    time_end: Time | str
    parity: int
    typeObj: TypeObj | dict
    groups: tuple[Group | dict] = field(default_factory=tuple)
    teachers: tuple[Teacher | dict] = field(default_factory=tuple)
    auditories: tuple[Auditory | dict] = field(default_factory=tuple)
    webinar_url: str = ''
    lms_url: str = ''

    def __post_init__(self):
        object.__setattr__(self, "time_start", Time(self.time_start))
        object.__setattr__(self, "time_end", Time(self.time_end))
        object.__setattr__(self, "typeObj", TypeObj(**self.typeObj))
        object.__setattr__(self, "groups", tuple([Group(**i) for i in self.groups]))
        object.__setattr__(self, "teachers", tuple([Teacher(**i) for i in self.teachers]))
        object.__setattr__(self, "auditories", tuple([Auditory(**i) for i in self.auditories]))


@dataclass(frozen=True)
class Day:
    weekday: int
    date: Date | str
    lessons: tuple[Lesson | dict] = field(default_factory=tuple)

    def __post_init__(self):
        object.__setattr__(self, "date", Date(self.date))
        object.__setattr__(self, "lessons", tuple([Lesson(**i) for i in self.lessons]))


@dataclass(frozen=True)
class Scheduler:
    week: Week | dict
    days: tuple[Day | dict] = field(default_factory=tuple)
    teacher: Teacher | dict = Teacher(0, 0, "Иванов Иван Иванович", "Иванов", "Иван", "Иванович", "", "")

    def __post_init__(self):
        object.__setattr__(self, "week", Week(**self.week))
        object.__setattr__(self, "teacher", Teacher(**self.teacher))
        object.__setattr__(self, "days", tuple([Day(**i) for i in self.days]))
