"""File with some data classes"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Faculty:
    id: int
    name: str
    abbr: str
