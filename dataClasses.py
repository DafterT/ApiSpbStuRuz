"""File with some data classes"""
from dataclasses import dataclass


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
