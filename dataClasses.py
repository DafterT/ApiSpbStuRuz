"""File with some data classes"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Faculties:
    id: int
    name: str
    abbr: str
