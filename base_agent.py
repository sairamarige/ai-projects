"""
base_agent.py
=============
Every agent in this project inherits from `Agent`. Subclasses implement
`process(state)` — the actual work — instead of `run(state)`.

`run(state)` (defined once, here) wraps `process`:
  1. checks `required_keys` are already present on shared state (this is
     the "agents check their own preconditions" idea — an agent won't
     silently crash on data an earlier stage was supposed to produce)
  2. logs entry/exit instead of using print()
  3. leaves error handling to the Supervisor, which is what actually
     calls `run` and can catch exceptions per-agent
"""

import logging


class Agent:
    """Abstract base class for all agents."""

    # Attributes on `state` that must exist and be non-empty before this
    # agent can do useful work. Override per subclass. Empty by default
    # for agents that generate the first piece of state (e.g. InputAgent).
    required_keys: list[str] = []

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, state):
        """Subclasses must override this with their actual logic."""
        raise NotImplementedError(f"{self.__class__.__name__} must implement process()")

    def is_ready(self, state) -> bool:
        """Precondition check: do we have what we need to run?"""
        for key in self.required_keys:
            value = getattr(state, key, None)
            if value in (None, [], {}, ""):
                self.logger.warning(f"Skipped — required state '{key}' is missing/empty.")
                return False
        return True

    def run(self, state):
        if not self.is_ready(state):
            return state
        self.logger.info("Running...")
        state = self.process(state)
        self.logger.info("Done.")
        return state
