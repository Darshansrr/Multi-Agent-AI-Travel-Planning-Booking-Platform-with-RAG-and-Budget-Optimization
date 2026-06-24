# tools/budget_tool.py

import re


def analyze_budget(flight_results: str, hotel_results: str) -> str:
    """
    Basic budget analysis from flight and hotel results.
    """

    prices = re.findall(r"\d+(?:\.\d+)?", flight_results + hotel_results)

    if not prices:
        return "Unable to estimate budget from available data."

    prices = [float(p) for p in prices]

    total_cost = sum(prices)
    cheapest = min(prices)
    expensive = max(prices)

    return f"""
Estimated Total Cost: {total_cost:.2f}

Cheapest Option:
{cheapest:.2f}

Luxury Option:
{expensive:.2f}

Budget Saving Suggestions:
- Book flights earlier
- Choose budget hotels
- Travel on weekdays
- Avoid peak season dates
"""