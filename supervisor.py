"""
supervisor.py
=============
One generic Supervisor used by all three pipelines. It:
  - builds the initial shared state (via `state_factory`)
  - runs each agent in order
  - wraps every agent call in try/except so one agent failing doesn't
    take down the whole pipeline — it's logged and execution continues
"""

import logging


class Supervisor:
    def __init__(self, agents, state_factory, name="Pipeline"):
        self.agents = agents
        self.state_factory = state_factory
        self.name = name
        self.logger = logging.getLogger(f"Supervisor:{name}")

    def run(self):
        state = self.state_factory()
        self.logger.info(f"Starting pipeline ({len(self.agents)} agents).")

        for agent in self.agents:
            try:
                state = agent.run(state)
            except Exception as exc:
                self.logger.error(
                    f"{agent.__class__.__name__} raised {type(exc).__name__}: {exc}. "
                    "Continuing with next agent."
                )

        self.logger.info("Pipeline finished.")
        return state
