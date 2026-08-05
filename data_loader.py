"""
data_loader.py
===============
Reads input records from CSV files. This is the "dynamic data" piece —
swap these functions for a DB query, an API call, or a form submission
and nothing else in the pipeline needs to change, since every agent
downstream only ever deals with Student / Employee / CartItem objects.
"""

import ast
import csv
import logging

from models import CartItem, Employee, Student

logger = logging.getLogger("DataLoader")


def load_students(path) -> list[Student]:
    students = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            marks = ast.literal_eval(row["marks"])  # "{'Math': 88, ...}" -> dict
            students.append(Student(name=row["name"], marks=marks))
    logger.info(f"Loaded {len(students)} students from {path}")
    return students


def load_employees(path) -> list[Employee]:
    employees = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            employees.append(Employee(
                name=row["name"],
                basic=float(row["basic"]),
                years=int(row["years"]),
                rating=row["rating"],
            ))
    logger.info(f"Loaded {len(employees)} employees from {path}")
    return employees


def load_products(path) -> list[CartItem]:
    items = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            items.append(CartItem(
                item=row["item"],
                price=float(row["price"]),
                qty=int(row["qty"]),
            ))
    logger.info(f"Loaded {len(items)} cart items from {path}")
    return items
