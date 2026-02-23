#!/usr/bin/python3
"""
Module 3-dictionary_of_list_of_dictionaries
Exports all tasks for **all** users to ``todo_all_employees.json``
in the format required by the checker.
"""
import json
import requests


def main():
    """Fetch all users and todos, then build the required structure."""
    base = "https://jsonplaceholder.typicode.com"
    users = requests.get(f"{base}/users").json()
    todos = requests.get(f"{base}/todos").json()

    # Group todos by userId
    by_user = {}
    for t in todos:
        by_user.setdefault(t.get("userId"), []).append(t)

    # Build payload
    data = {}
    for u in users:
        uid = u.get("id")
        username = u.get("username")
        tasks = by_user.get(uid, [])
        data[str(uid)] = [
            {
                "username": username,
                "task": t.get("title"),
                "completed": t.get("completed")
            } for t in tasks
        ]

    with open("todo_all_employees.json", "w", encoding="utf-8") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
