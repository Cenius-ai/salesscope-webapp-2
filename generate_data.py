#!/usr/bin/env python3
"""Generate exactly 1000 realistic sales records across 2 years, 5 regions, 10 products."""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

REGIONS = [
    "North America",
    "Europe",
    "Asia Pacific",
    "Latin America",
    "Middle East & Africa",
]

PRODUCTS = [
    "Enterprise Suite",
    "Cloud Storage Pro",
    "DataSync Basic",
    "Analytics Plus",
    "Security Shield",
    "API Gateway",
    "Mobile Connect",
    "IoT Platform",
    "AI Insights",
    "Workflow Automator",
]

PRODUCT_CATEGORY = {
    "Enterprise Suite": "Software",
    "Cloud Storage Pro": "Cloud Services",
    "DataSync Basic": "Cloud Services",
    "Analytics Plus": "Analytics",
    "Security Shield": "Security",
    "API Gateway": "Integration",
    "Mobile Connect": "Integration",
    "IoT Platform": "Cloud Services",
    "AI Insights": "Analytics",
    "Workflow Automator": "Software",
}

# Base price per unit (USD) and cost per unit (to derive profit)
PRODUCT_ECONOMICS = {
    "Enterprise Suite":   (1250.0, 500.0),
    "Cloud Storage Pro":  (480.0,  160.0),
    "DataSync Basic":     (195.0,  55.0),
    "Analytics Plus":     (890.0,  320.0),
    "Security Shield":    (750.0,  260.0),
    "API Gateway":        (320.0,  90.0),
    "Mobile Connect":     (210.0,  60.0),
    "IoT Platform":       (640.0,  210.0),
    "AI Insights":        (1100.0, 400.0),
    "Workflow Automator": (560.0,  180.0),
}

REGION_MULTIPLIERS = {
    "North America": 1.4,
    "Europe": 1.2,
    "Asia Pacific": 1.0,
    "Latin America": 0.7,
    "Middle East & Africa": 0.5,
}

TARGET_ROWS = 1000
START_DATE = date(2023, 1, 1)
END_DATE = date(2024, 12, 31)

# Resolved once at module load; the base dir is the canonical project root.
_BASE_DIR = Path(__file__).resolve().parent
_OUTPUT_DIR = (_BASE_DIR / "data").resolve()
_OUTPUT_FILENAME = "sales_data.csv"


def _safe_output_path() -> Path:
    """Return the resolved output path, validated to stay within the data directory."""
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = (_OUTPUT_DIR / _OUTPUT_FILENAME).resolve()
    if not target.is_relative_to(_OUTPUT_DIR):
        raise ValueError(
            f"Output path {target} escapes the expected data directory {_OUTPUT_DIR}"
        )
    return target


def seasonal_factor(d: date) -> float:
    quarter = (d.month - 1) // 3 + 1
    if quarter == 4:
        return 1.35
    elif quarter == 1:
        return 0.75
    elif quarter == 2:
        return 1.05
    else:
        return 1.10


def weekday_factor(d: date) -> float:
    return 1.2 if d.weekday() < 5 else 0.35


def generate() -> None:
    rows: list[dict[str, object]] = []
    order_id = 1000

    total_days = (END_DATE - START_DATE).days + 1
    # We need TARGET_ROWS rows across total_days days
    # Generate a weighted distribution so each day gets at least 1, some get more
    weights = [weekday_factor(START_DATE + timedelta(days=i)) for i in range(total_days)]
    weight_sum = sum(weights)

    # Assign row counts per day proportionally, then adjust to hit exactly TARGET_ROWS
    raw_counts = [max(1, round(TARGET_ROWS * w / weight_sum)) for w in weights]
    diff = TARGET_ROWS - sum(raw_counts)
    # Adjust: add/subtract from highest-weight days
    indices_by_weight = sorted(range(total_days), key=lambda i: weights[i], reverse=True)
    i = 0
    while diff > 0:
        raw_counts[indices_by_weight[i % total_days]] += 1
        diff -= 1
        i += 1
    while diff < 0:
        idx = indices_by_weight[i % total_days]
        if raw_counts[idx] > 1:
            raw_counts[idx] -= 1
            diff += 1
        i += 1

    for day_idx in range(total_days):
        current = START_DATE + timedelta(days=day_idx)
        day_seed = current.toordinal()
        rng = random.Random(day_seed)
        num_records = raw_counts[day_idx]

        for _ in range(num_records):
            region = rng.choice(REGIONS)
            product = rng.choice(PRODUCTS)
            category = PRODUCT_CATEGORY[product]

            base_price, base_cost = PRODUCT_ECONOMICS[product]
            region_mult = REGION_MULTIPLIERS[region]
            season = seasonal_factor(current)
            wday = weekday_factor(current)

            price_noise = rng.uniform(0.85, 1.15)
            effective_price = round(base_price * price_noise, 2)

            units_factor = region_mult * season * wday * rng.uniform(0.5, 1.5)
            quantity = max(1, round(units_factor * rng.randint(2, 20)))

            sales_amount = round(effective_price * quantity, 2)
            cost_total = round(base_cost * price_noise * quantity, 2)
            profit = round(sales_amount - cost_total, 2)

            rows.append({
                "OrderID": order_id,
                "Date": current.isoformat(),
                "Region": region,
                "Product": product,
                "Category": category,
                "SalesAmount": sales_amount,
                "Quantity": quantity,
                "Profit": profit,
            })
            order_id += 1

    # Safety: trim or warn if we drifted
    if len(rows) != TARGET_ROWS:
        print(f"WARNING: generated {len(rows)} rows, expected {TARGET_ROWS} — trimming")
        rows = rows[:TARGET_ROWS]

    output_path = _safe_output_path()
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["OrderID", "Date", "Region", "Product", "Category", "SalesAmount", "Quantity", "Profit"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} sales records → {output_path}")


if __name__ == "__main__":
    generate()
