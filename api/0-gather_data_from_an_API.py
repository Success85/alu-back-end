#!/usr/bin/python3
"""
0-gather_data_from_an_API.py

For a given employee ID, prints:
Employee EMPLOYEE_NAME is done with tasks(DONE/TOTAL):
\t TASK_TITLE
...
"""

import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://jsonplaceholder.typicode.com"


def fetch_json(url):
    """
    Fetch JSON from the given URL using urllib and return the parsed object.
    """
    req = Request(url, headers={"User-Agent": "python-urllib/3"})
    with urlopen(req) as resp:
        return json.load(resp)


def main():
    """
    Entry point for CLI usage.
    Expects exactly one integer argument: employee ID.
    """
    if len(sys.argv) != 2:
        return

    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        return

    try:
        user = fetch_json("{}/users/{}".format(BASE_URL, emp_id))
        todos = fetch_json("{}/todos?userId={}".format(BASE_URL, emp_id))
    except (HTTPError, URLError, ValueError):
        return

    name = user.get("name", "")
    done_titles = [
        t.get("title", "")
        for t in todos
        if t.get("completed") is True
    ]
    total = len(todos)
    done = len(done_titles)

    # Exact header format (wrapped to satisfy E501)
    print(
        "Employee {} is done with tasks({}/{}):"
        .format(name, done, total)
    )

    # Each completed task: tab + space + title
    for title in done_titles:
        print("\t {}".format(title))


if __name__ == "__main__":
    main()
