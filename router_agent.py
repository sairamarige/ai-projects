"""
router_agent.py
================
A RouterAgent that looks at a user's request and decides which pipeline
handles it — the "User -> Router -> Student/Employee/Shopping" pattern
(a keyword-matching stand-in for an LLM-based intent router).
"""

import logging

from employee_pipeline import build_employee_pipeline
from shopping_pipeline import build_shopping_pipeline
from student_pipeline import build_student_pipeline

logger = logging.getLogger("RouterAgent")


class RouterAgent:
    ROUTES = {
        "student": ["student", "report card", "marks", "grade"],
        "employee": ["employee", "salary", "payroll", "bonus"],
        "shopping": ["shopping", "cart", "invoice", "order", "buy", "checkout"],
    }

    PIPELINE_BUILDERS = {
        "student": build_student_pipeline,
        "employee": build_employee_pipeline,
        "shopping": build_shopping_pipeline,
    }

    def route(self, user_request: str) -> str:
        """Pick a route name based on keywords in the request."""
        text = user_request.lower()
        for route_name, keywords in self.ROUTES.items():
            if any(keyword in text for keyword in keywords):
                logger.info(f"Routed '{user_request}' -> '{route_name}'")
                return route_name
        logger.warning(f"No route matched '{user_request}', defaulting to 'student'")
        return "student"

    def dispatch(self, user_request: str):
        """Route the request and run the matching pipeline."""
        route_name = self.route(user_request)
        build_pipeline = self.PIPELINE_BUILDERS[route_name]
        supervisor = build_pipeline()
        return supervisor.run()
