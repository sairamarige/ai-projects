"""
models.py
=========
Dataclasses for the records each pipeline works with. Fields with defaults
are the ones later agents fill in as the record moves through the pipeline
(e.g. `Student.grade` starts empty and is set by GradeAgent).
"""

from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    marks: dict
    total: int = 0
    max_total: int = 0
    percentage: float = 0.0
    grade: str = ""


@dataclass
class Employee:
    name: str
    basic: float
    years: int
    rating: str
    hra: float = 0.0
    travel_allowance: float = 0.0
    gross: float = 0.0
    tax_rate: float = 0.0
    tax: float = 0.0
    bonus: float = 0.0
    net: float = 0.0


@dataclass
class CartItem:
    item: str
    price: float
    qty: int
    subtotal: float = 0.0
    discount: float = 0.0
