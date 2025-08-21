import argparse
import json
from collections import defaultdict
from datetime import datetime

from tabulate import tabulate

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Script for argument parsing")
    parser.add_argument("--input", type=str, nargs="+", required=True, help="Path to input file")
    parser.add_argument("--report", type=str, default="average", help="Report type")
    parser.add_argument("--date", type=str, help="Report type")
    return parser.parse_args(argv)

def get_stats_from_file(stats, file_name, date=None):
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entry_date = datetime.strptime(entry["@timestamp"], "%Y-%m-%dT%H:%M:%S%z").date()
                if(date is not None and date != entry_date):
                    continue
                key = entry["url"]
                stats[key]["count"] += 1
                stats[key]["total_responce_time"] += entry["response_time"]
            except json.JSONDecodeError:
                print(f"Skipping malformed line: {line}")
            except KeyError:
                print(f"Missing expected field in line: {line}")

def form_report_average(input_files, date=None):
    date = None if date is None else datetime.strptime(date, "%Y-%d-%m").date()
    stats = defaultdict(lambda: {"count": 0, "total_responce_time": 0})

    for file_name in input_files:
        get_stats_from_file(stats, file_name, date)

    table_data=[]
    for key, data in stats.items():
        avg = data["total_responce_time"] / data["count"]
        table_data.append([key, data["count"], f"{avg:.3f}"])
    return table_data

def main(argv=None):
    args = parse_args(argv)
    print(f"Input: {args.input}")
    print(f"Report: {args.report}")
    print(f"Date: {args.date}")

    table_data = form_report_average(args.input, args.date)
    headers = ["handler", "total", "avg_response_time"]
    print(tabulate(table_data, headers=headers))

if __name__ == "__main__":
    main()
