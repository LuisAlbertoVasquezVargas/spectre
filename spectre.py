#!/usr/bin/env python3

import os
import sys
import uuid
import json
from datetime import datetime, timezone

REPO_DIR = ".vcs_spectre"
STACK_FILE = os.path.join(REPO_DIR, "stack.json")
PTR_FILE = os.path.join(REPO_DIR, "PTR")
TRACKED_FILE = "main.txt"

def ensure_repo():
    if not os.path.isdir(REPO_DIR):
        print("Spectre repository not initialized.")
        sys.exit(1)

def write_stack(stack):
    with open(STACK_FILE, "w") as f:
        json.dump(stack, f, indent=2)

def read_stack():
    if not os.path.exists(STACK_FILE):
        return []
    with open(STACK_FILE) as f:
        return json.load(f)

def read_ptr():
    if not os.path.exists(PTR_FILE):
        return None
    with open(PTR_FILE) as f:
        return f.read().strip()

def write_ptr(snapshot_id):
    with open(PTR_FILE, "w") as f:
        f.write(snapshot_id)

def init():
    if os.path.exists(REPO_DIR):
        print("Spectre repository already exists.")
        return
    if os.path.exists(TRACKED_FILE):
        print("main.txt already exists. Cannot initialize.")
        return

    os.makedirs(REPO_DIR)
    with open(TRACKED_FILE, "w") as f:
        f.write("")

    first_snapshot = {"id": str(uuid.uuid4()), "date": datetime.now(timezone.utc).isoformat(), "comment": "Initial empty state", "state": ""}
    write_stack([first_snapshot])
    write_ptr(first_snapshot["id"])
    print("Initialized empty Spectre repository.")

def save():
    ensure_repo()
    comment = input("Comment for this snapshot: ")
    with open(TRACKED_FILE, "r") as f:
        state = f.read()

    new_snapshot = {"id": str(uuid.uuid4()), "date": datetime.now(timezone.utc).isoformat(), "comment": comment, "state": state}

    stack = read_stack()
    stack.append(new_snapshot)
    write_stack(stack)
    write_ptr(new_snapshot["id"])
    print(f"Saved snapshot {new_snapshot['id']}")

def log():
    ensure_repo()
    stack = read_stack()
    current = read_ptr()
    for snap in stack:
        marker = " ← PTR" if snap["id"] == current else ""
        print(f"{snap['id']} [{snap['date']}] - {snap['comment']}{marker}")

def switch(target_id):
    ensure_repo()
    stack = read_stack()
    match = next((s for s in stack if s["id"] == target_id), None)
    if not match:
        print("No snapshot with that ID.")
        return
    with open(TRACKED_FILE, "w") as f:
        f.write(match["state"])
    write_ptr(match["id"])
    print(f"Switched to snapshot {target_id}")

def main():
    if len(sys.argv) < 2:
        print("Usage: spectre [init | save | log | switch <id>]")
        return

    cmd = sys.argv[1]
    if cmd == "init":
        init()
    elif cmd == "save":
        save()
    elif cmd == "log":
        log()
    elif cmd == "switch":
        if len(sys.argv) < 3:
            print("Usage: spectre switch <id>")
            return
        switch(sys.argv[2])
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
