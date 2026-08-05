"""
student_pipeline.py
====================
Level 1: Student Report Generator, rebuilt on the shared Agent base class.
"""

import logging
from dataclasses import dataclass, field

import config
from base_agent import Agent
from data_loader import load_students

logger = logging.getLogger("StudentReport")


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------
@dataclass
class StudentSharedState:
    students: list = field(default_factory=list)
    errors: list = field(default_factory=list)

    def add_error(self, name, message):
        self.errors.append(f"{name}: {message}")


# ---------------------------------------------------------------------------
# Pure helper (kept standalone so it's easy to unit test)
# ---------------------------------------------------------------------------
def grade_for(percentage: float) -> str:
    for minimum, grade in config.GRADE_BOUNDARIES:
        if percentage >= minimum:
            return grade
    return "F"


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------
class InputAgent(Agent):
    """First agent in the pipeline — nothing is required beforehand."""

    def process(self, state: StudentSharedState):
        state.students = load_students(config.STUDENTS_CSV)
        return state


class ValidationAgent(Agent):
    required_keys = ["students"]

    def process(self, state: StudentSharedState):
        valid = []
        for student in state.students:
            bad = [m for m in student.marks.values()
                   if not (config.MARK_MIN <= m <= config.MARK_MAX)]
            if bad:
                state.add_error(student.name, f"invalid marks found: {bad}")
            else:
                valid.append(student)
        state.students = valid
        return state


class MarksAgent(Agent):
    required_keys = ["students"]

    def process(self, state: StudentSharedState):
        for student in state.students:
            student.total = sum(student.marks.values())
            student.max_total = len(student.marks) * 100
        return state


class PercentageAgent(Agent):
    required_keys = ["students"]

    def process(self, state: StudentSharedState):
        for student in state.students:
            student.percentage = round(student.total / student.max_total * 100, 2)
        return state


class GradeAgent(Agent):
    required_keys = ["students"]

    def process(self, state: StudentSharedState):
        for student in state.students:
            student.grade = grade_for(student.percentage)
        return state


class StudentReportAgent(Agent):
    required_keys = ["students"]

    def process(self, state: StudentSharedState):
        logger.info("=" * 50)
        logger.info("STUDENT REPORT CARD SUMMARY")
        logger.info("=" * 50)
        for student in state.students:
            logger.info(
                f"{student.name}: {student.total}/{student.max_total} "
                f"({student.percentage}%) -> Grade {student.grade}"
            )
        for err in state.errors:
            logger.info(f"REJECTED - {err}")

        if state.students:
            avg = round(sum(s.percentage for s in state.students) / len(state.students), 2)
            logger.info(f"Class Average: {avg}%")
        return state


# ---------------------------------------------------------------------------
# Pipeline builder
# ---------------------------------------------------------------------------
def build_student_pipeline():
    from supervisor import Supervisor
    return Supervisor(
        agents=[
            InputAgent(),
            ValidationAgent(),
            MarksAgent(),
            PercentageAgent(),
            GradeAgent(),
            StudentReportAgent(),
        ],
        state_factory=StudentSharedState,
        name="Student Report",
    )
