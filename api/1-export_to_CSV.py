#!/usr/bin/python3
"""
Module 1-export_to_CSV
Exports all tasks for a given user to a CSV file: ``USER_ID.csv``.
Format:
"USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"
"""
import csv
import requests
import sys


def main():
    """Fetch data and write CSV rows with all tasks for the user."""
    if len(sys.argv) < 2:
        sys.exit(0)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        sys.exit(0)

    base = "https://jsonplaceholder.typicode.com"
    user = requests.get(f"{base}/users/{user_id}").json()
    todos = requests.get(f"{base}/todos", params={"userId": user_id}).json()

    username = user.get("username")
    filename = f"{user_id}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for t in todos:
            writer.writerow([
                str(user_id),
                username,
                str(t.get("completed")),
                t.get("title")
            ])


if __name__ == "__main__":
    main()
