
import csv
from datetime import date, timedelta

providers = [
    ("AWS", "us-east-1", 120.50),
    ("Azure", "Central India", 95.75),
    ("GCP", "asia-south1", 85.25)
]

today = date.today()

with open("historical_costs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "date", "provider", "region",
        "currency", "daily_cost_usd"
    ])

    for day in range(44, -1, -1):
        current_date = today - timedelta(days=day)

        for provider, region, base_cost in providers:
            daily_cost = round(
                base_cost + (day % 7) * 2.35,
                2
            )

            writer.writerow([
                current_date.isoformat(),
                provider,
                region,
                "USD",
                daily_cost
            ])

print("Historical cost dataset created!")
print("Total records:", 45 * 3)
print("Unique days:", 45)