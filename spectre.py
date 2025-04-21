#!/usr/bin/env python3
# spectre.py

import os
import sys
import uuid
import json
from datetime import datetime, timezone, timedelta
from logger import Logger

REPO_DIR = ".vcs_spectre"
SNAPSHOT_FILE = os.path.join(REPO_DIR, "tree.json")
CURRENT_FILE = os.path.join(REPO_DIR, "CURRENT")
TRACKED_FILE = "main.txt"

def create_snapshot(state: str, comment: str, parent_id: str = None) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "date": datetime.now(timezone(timedelta(hours=-5))).strftime("%d %b %Y %I:%M:%S %p"),
        "comment": comment,
        "state": state,
        "parent": parent_id
    }

def ensure_repo():
    if not os.path.isdir(REPO_DIR):
        Logger.error("Spectre repository not initialized.")
        sys.exit(1)

def write_tree(tree):
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(tree, f, indent=2)

def read_tree():
    if not os.path.exists(SNAPSHOT_FILE):
        return []
    with open(SNAPSHOT_FILE) as f:
        return json.load(f)

def read_current():
    if not os.path.exists(CURRENT_FILE):
        return None
    with open(CURRENT_FILE) as f:
        return f.read().strip()

def write_current(snapshot_id):
    with open(CURRENT_FILE, "w") as f:
        f.write(snapshot_id)

def init():
    if os.path.exists(REPO_DIR):
        Logger.error("Spectre repository already exists.")
        return
    if os.path.exists(TRACKED_FILE):
        Logger.error("main.txt already exists. Cannot initialize.")
        return

    os.makedirs(REPO_DIR)
    with open(TRACKED_FILE, "w") as f:
        f.write("")

    root = create_snapshot("", "Initial empty state", parent_id=None)
    write_tree([root])
    write_current(root["id"])
    Logger.info("Initialized empty Spectre repository.")

def save():
    ensure_repo()
    comment = input("Comment for this snapshot: ")
    with open(TRACKED_FILE, "r") as f:
        state = f.read()

    parent_id = read_current()
    new_snapshot = create_snapshot(state, comment, parent_id=parent_id)

    tree = read_tree()
    tree.append(new_snapshot)
    write_tree(tree)
    write_current(new_snapshot["id"])
    Logger.info(f"Saved snapshot {new_snapshot['id']}")

def log():
    ensure_repo()
    tree = read_tree()
    current_id = read_current()

    snapshot_map = {s["id"]: s for s in tree}
    children_map = {}
    for snap in tree:
        children_map.setdefault(snap.get("parent"), []).append(snap)

    def render(node_id, levels=0, parent_connector=''):
        node = snapshot_map[node_id]
        is_current = node_id == current_id
        children = children_map.get(node_id, [])
        prefix = ('|' * (levels - 1) + parent_connector) if parent_connector != '' else ('|' * levels)
        Logger.snapshot(node, is_current=is_current, prefix=prefix)
        if len(children) == 0:
            return
        elif len(children) == 1:
            Logger.plain('|' * (levels - 1) + '↓')
            render(children[0]["id"], levels)
        elif len(children) > 1:
            for i, child in enumerate(children):
                connector = "├─" if i < len(children) - 1 else "└─"
                render(child["id"], levels + 1, parent_connector=connector)

    for root in children_map.get(None, []):
        render(root["id"])

def switch(target_id):
    ensure_repo()
    tree = read_tree()
    match = next((s for s in tree if s["id"] == target_id), None)
    if not match:
        Logger.error("No snapshot with that ID.")
        return
    with open(TRACKED_FILE, "w") as f:
        f.write(match["state"])
    write_current(match["id"])
    Logger.info(f"Switched to snapshot {target_id}")

def main():
    if len(sys.argv) < 2:
        Logger.plain("Usage: spectre [init | save | log | switch <id>]")
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
            Logger.plain("Usage: spectre switch <id>")
            return
        switch(sys.argv[2])
    else:
        Logger.error("Unknown command")

if __name__ == "__main__":
    main()
