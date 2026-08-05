"""
main.py
=======
Entry point. Simulates: User -> RouterAgent -> (Student | Employee | Shopping)

Run from the project root so the relative CSV paths in config.py resolve:
    cd multi_agent_project
    python3 main.py
"""

import config
from router_agent import RouterAgent


def main():
    config.configure_logging()
    router = RouterAgent()

    # Stand-ins for real user requests (chat input, API calls, form submits...)
    user_requests = [
        "Generate the student report card",
        "Run payroll and calculate employee bonuses",
        "Process my shopping cart and give me an invoice",
    ]

    for request in user_requests:
        print(f"\nUSER: {request}")
        router.dispatch(request)


if __name__ == "__main__":
    main()
