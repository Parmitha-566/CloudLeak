
import csv
import json
import argparse
from pathlib import Path

ALLOWED_TYPES = {
    "EC2", "RDS", "S3",
    "Kubernetes", "Lambda", "LoadBalancer"
}

REQUIRED_COLUMNS = {
    "resource_id", "resource_type", "cpu_cores",
    "memory_gb", "cpu_utilization_pct",
    "memory_utilization_pct", "monthly_cost_usd", "region"
}


def load_and_validate(filename):

    resources = []
    seen_ids = set()

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty.")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        for line, row in enumerate(reader, start=2):
            try:
                resource_id = row["resource_id"].strip()
                resource_type = row["resource_type"].strip()
                region = row["region"].strip()

                if not resource_id or not region:
                    raise ValueError("Resource ID and region are required.")

                if resource_id in seen_ids:
                    raise ValueError("Duplicate resource ID.")

                if resource_type not in ALLOWED_TYPES:
                    raise ValueError("Invalid resource type.")

                cpu = int(row["cpu_cores"])
                memory = float(row["memory_gb"])
                cpu_util = float(row["cpu_utilization_pct"])
                memory_util = float(row["memory_utilization_pct"])
                cost = float(row["monthly_cost_usd"])

                if cpu < 0 or memory < 0 or cost < 0:
                    raise ValueError("Negative resource values are invalid.")

                if not 0 <= cpu_util <= 100:
                    raise ValueError("Invalid CPU utilization.")

                if not 0 <= memory_util <= 100:
                    raise ValueError("Invalid memory utilization.")

                seen_ids.add(resource_id)

                resources.append({
                    "resource_id": resource_id,
                    "resource_type": resource_type,
                    "cpu_cores": cpu,
                    "memory_gb": memory,
                    "cpu_utilization_pct": cpu_util,
                    "memory_utilization_pct": memory_util,
                    "average_utilization_pct": round(
                        (cpu_util + memory_util) / 2, 2
                    ),
                    "monthly_cost_usd": round(cost, 2),
                    "region": region
                })

            except (ValueError, TypeError) as error:
                raise ValueError(f"Line {line}: {error}") from error

    if not resources:
        raise ValueError("No resource records found.")

    return resources


def filter_resources(resources, resource_type=None,
                     min_utilization=None, max_utilization=None):

    filtered = resources

    if resource_type:
        filtered = [
            r for r in filtered
            if r["resource_type"].lower() == resource_type.lower()
        ]

    if min_utilization is not None:
        filtered = [
            r for r in filtered
            if r["average_utilization_pct"] >= min_utilization
        ]

    if max_utilization is not None:
        filtered = [
            r for r in filtered
            if r["average_utilization_pct"] <= max_utilization
        ]

    return filtered


def main():

    parser = argparse.ArgumentParser(
        description="Cloud Leak Resource Data Module"
    )

    parser.add_argument("--type", dest="resource_type")
    parser.add_argument("--min-utilization", type=float)
    parser.add_argument("--max-utilization", type=float)
    parser.add_argument("--input", default="sample_billing.csv")
    parser.add_argument("--output", default="member2_input.json")

    args = parser.parse_args()

    for value in (args.min_utilization, args.max_utilization):
        if value is not None and not 0 <= value <= 100:
            parser.error("Utilization must be between 0 and 100.")

    if (args.min_utilization is not None
            and args.max_utilization is not None
            and args.min_utilization > args.max_utilization):
        parser.error("Minimum utilization cannot exceed maximum.")

    resources = load_and_validate(args.input)

    filtered = filter_resources(
        resources,
        args.resource_type,
        args.min_utilization,
        args.max_utilization
    )

    output = {
        "metadata": {
            "total_records_loaded": len(resources),
            "records_after_filter": len(filtered),
            "currency": "USD",
            "utilization_definition":
                "Average of CPU and memory utilization"
        },
        "resources": filtered
    }

    Path(args.output).write_text(
        json.dumps(output, indent=4),
        encoding="utf-8"
    )

    print("Cloud Leak Data Module")
    print("----------------------")
    print("Validation successful!")
    print("Records loaded:", len(resources))
    print("Records after filtering:", len(filtered))
    print("JSON output created:", args.output)


if __name__ == "__main__":
    main()