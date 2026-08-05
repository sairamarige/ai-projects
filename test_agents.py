"""
tests/test_agents.py
======================
Unit tests for the pure functions each pipeline relies on, plus the
RouterAgent's routing decisions. Run with:

    cd multi_agent_project
    pytest
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from employee_pipeline import tax_rate
from router_agent import RouterAgent
from student_pipeline import grade_for


# ---------------------------------------------------------------------------
# student_pipeline.grade_for
# ---------------------------------------------------------------------------
def test_grade_for_top_boundary():
    assert grade_for(95) == "A+"
    assert grade_for(90) == "A+"


def test_grade_for_just_below_a_plus():
    assert grade_for(89.9) == "A"


def test_grade_for_mid_range():
    assert grade_for(75) == "A"
    assert grade_for(60) == "B"
    assert grade_for(40) == "C"


def test_grade_for_failing():
    assert grade_for(0) == "F"
    assert grade_for(39.9) == "F"


# ---------------------------------------------------------------------------
# employee_pipeline.tax_rate
# ---------------------------------------------------------------------------
def test_tax_rate_top_slab():
    assert tax_rate(90000) == 0.20


def test_tax_rate_middle_slab():
    assert tax_rate(60000) == 0.12


def test_tax_rate_bottom_slab():
    assert tax_rate(20000) == 0.05


# ---------------------------------------------------------------------------
# router_agent.RouterAgent
# ---------------------------------------------------------------------------
def test_router_routes_student_request():
    assert RouterAgent().route("show me the student report card") == "student"


def test_router_routes_employee_request():
    assert RouterAgent().route("run payroll for this month") == "employee"


def test_router_routes_shopping_request():
    assert RouterAgent().route("checkout my shopping cart") == "shopping"


def test_router_defaults_when_no_keyword_matches():
    assert RouterAgent().route("completely unrelated gibberish") == "student"
