"""
employee_pipeline.py
======================
Level 2: Employee Salary Management, rebuilt on the shared Agent base class.
"""

import logging
from dataclasses import dataclass, field

import config
from base_agent import Agent
from data_loader import load_employees

logger = logging.getLogger("Payroll")


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------
@dataclass
class EmployeeSharedState:
    employees: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Pure helper (kept standalone so it's easy to unit test)
# ---------------------------------------------------------------------------
def tax_rate(gross: float) -> float:
    for threshold, rate in config.TAX_SLABS:
        if gross > threshold:
            return rate
    return config.TAX_SLABS[-1][1]


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------
class EmployeeAgent(Agent):
    def process(self, state: EmployeeSharedState):
        state.employees = load_employees(config.EMPLOYEES_CSV)
        return state


class AllowanceAgent(Agent):
    required_keys = ["employees"]

    def process(self, state: EmployeeSharedState):
        for emp in state.employees:
            emp.hra = round(emp.basic * config.HRA_RATE, 2)
            emp.travel_allowance = config.TRAVEL_ALLOWANCE
        return state


class SalaryAgent(Agent):
    required_keys = ["employees"]

    def process(self, state: EmployeeSharedState):
        for emp in state.employees:
            emp.gross = round(emp.basic + emp.hra + emp.travel_allowance, 2)
        return state


class TaxAgent(Agent):
    required_keys = ["employees"]

    def process(self, state: EmployeeSharedState):
        for emp in state.employees:
            emp.tax_rate = tax_rate(emp.gross)
            emp.tax = round(emp.gross * emp.tax_rate, 2)
        return state


class BonusAgent(Agent):
    required_keys = ["employees"]

    def process(self, state: EmployeeSharedState):
        for emp in state.employees:
            base_bonus = emp.basic * config.BONUS_RATING_PCT.get(emp.rating, 0)
            loyalty_bonus = config.LOYALTY_BONUS_PER_YEAR * emp.years
            emp.bonus = round(base_bonus + loyalty_bonus, 2)
        return state


class PayrollReportAgent(Agent):
    required_keys = ["employees"]

    def process(self, state: EmployeeSharedState):
        logger.info("=" * 55)
        logger.info("PAYROLL REPORT")
        logger.info("=" * 55)
        total_payout = 0
        for emp in state.employees:
            emp.net = round(emp.gross - emp.tax + emp.bonus, 2)
            total_payout += emp.net
            logger.info(
                f"{emp.name}: gross ₹{emp.gross}, tax ₹{emp.tax} "
                f"({int(emp.tax_rate*100)}%), bonus ₹{emp.bonus} -> net ₹{emp.net}"
            )
        logger.info(f"Total Payroll Payout: ₹{round(total_payout, 2)}")
        return state


# ---------------------------------------------------------------------------
# Pipeline builder
# ---------------------------------------------------------------------------
def build_employee_pipeline():
    from supervisor import Supervisor
    return Supervisor(
        agents=[
            EmployeeAgent(),
            AllowanceAgent(),
            SalaryAgent(),
            TaxAgent(),
            BonusAgent(),
            PayrollReportAgent(),
        ],
        state_factory=EmployeeSharedState,
        name="Employee Payroll",
    )
