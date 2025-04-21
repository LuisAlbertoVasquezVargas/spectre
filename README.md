# Spectre

**Spectre** is a minimal version control system **VCS** for a single file (`main.txt`), built on a traceable tree of full snapshots.

It is designed to be simple, local, and predictable — no branches (yet), no merges, no diffs — just a growing tree of saved states where each snapshot knows its parent.

---

## 🧠 Assumptions

- One file (`main.txt`)
- One author
- One tree of snapshots
- One pointer (`CURRENT`) tracking the active snapshot
- Every snapshot holds the entire state, not the difference
- Traceability enabled through `parent` linkage

---

## 📦 How It Works

Spectre creates a `.vcs_spectre/` folder which contains:

```
.vcs_spectre/
├── tree.json         # Flat list of all snapshots (with parent relationships)
├── CURRENT           # Points to the current snapshot ID
└── main.txt          # Tracked file (in project root)
```

Each snapshot entry contains:

```json
{
  "id": "<uuid4>",
  "date": "20 Apr 2025 06:45:11 PM",
  "comment": "your description",
  "state": "<contents of main.txt>",
  "parent": "<id of parent snapshot, or null for root>"
}
```

---

## 🚀 Usage

### 1. Initialize a new repo

```bash
spectre init
```

- Fails if `main.txt` already exists
- Creates an empty `main.txt` and saves it as the root snapshot

### 2. Save a snapshot

```bash
spectre save
```

- Prompts for a comment
- Creates a new snapshot as a child of the current one
- Updates `CURRENT` to the new snapshot

### 3. View history

```bash
spectre log
```

- Shows all snapshot IDs, dates, and comments
- Highlights the current `CURRENT` snapshot

### 4. Switch to a previous snapshot

```bash
spectre switch <snapshot_id>
```

- Overwrites `main.txt` with the selected snapshot’s state
- Sets `CURRENT` to that snapshot

---

## 🧪 Example

```bash
spectre init
# => Initialized empty Spectre repository.

echo "hello world" > main.txt
spectre save
# => Comment for this snapshot: initial greeting

spectre log
# => [snapshot_id] [timestamp] - initial greeting ← CURRENT
```

---

## 🛠 CLI Setup (for global use)

Run this after cloning the project:

```bash
chmod +x ~/projects/spectre/spectre.py
mkdir -p ~/bin
ln -s ~/projects/spectre/spectre.py ~/bin/spectre
export PATH="$HOME/bin:$PATH"   # Needed only per terminal session
```

You can now run `spectre` like a real CLI tool from any directory.

To confirm:

```bash
which spectre
# Should show: /home/youruser/bin/spectre
```

---

## 🛡 Requirements

- Python 3.12
- Tested in WSL2 (Ubuntu 22.04)

---

## ✨ Roadmap Ideas

- `spectre show <id>` to preview snapshot contents without switching
- `spectre diff <id1> <id2>` to show differences
- Export/import snapshot tree
- Named snapshots (aliases)
- Lock `CURRENT` for safe mode
- Visual `spectre graph` to show parent → child lineage

---

## 🧑‍💻 Author

Luis Vásquez

