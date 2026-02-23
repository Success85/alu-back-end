#!/usr/bin/python3
"""
Module 2-export_to_JSON
Exports all tasks for a given user to JSON file: ``USER_ID.json``.
Format:
{
  "USER_ID": [
    {"task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS,
     "username": "USERNAME"},
    ...
  ]
}
"""
import json
import requests
import sys


def main():
    """Fetch data and dump a JSON mapping for the user."""
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
    payload = {
        str(user_id): [
            {
                "task": t.get("title"),
                "completed": t.get("completed"),
                "username": username
            }
            for t in todos
        ]
    }

    filename = f"{user_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f)


if __name__ == "__main__":
    main()
