# Spectre

**Spectre** is a minimal version control system for a single file (`main.txt`), built on a stack of full snapshots.

It is designed to be simple, local, and predictable — no branches, no merges, no diffs — just a linear history of saved states.

---

## 🧠 Philosophy

- One file (`main.txt`)
- One author
- One branch
- One stack of snapshots
- One pointer (`PTR`) tracking the active snapshot
- Every snapshot holds the entire state, not the difference

---

## 📦 How It Works

Spectre creates a `.vcs_spectre/` folder which contains:

```
.vcs_spectre/
├── stack.json        # List of snapshots
├── PTR               # Pointer to the current snapshot ID
└── main.txt          # Tracked file (in project root)
```

Each snapshot entry contains:

```json
{
  "id": "<uuid4>",
  "date": "<ISO timestamp>",
  "comment": "<your comment>",
  "state": "<contents of main.txt>"
}
```

---

## 🚀 Usage

### 1. Initialize a new repo

```bash
python spectre.py init
```

- Fails if `main.txt` already exists
- Creates an empty `main.txt` and saves it as the first snapshot

---

### 2. Save a snapshot

```bash
python spectre.py save
```

- Prompts for a comment
- Appends the full state of `main.txt` to the stack
- Updates `PTR` to the new snapshot

---

### 3. View history

```bash
python spectre.py log
```

- Shows all snapshot IDs, dates, and comments
- Highlights the current `PTR`

---

### 4. Switch to a previous snapshot

```bash
python spectre.py switch <snapshot_id>
```

- Overwrites `main.txt` with the snapshot’s state
- Updates `PTR`

---

## 🧪 Example

```bash
python spectre.py init
# => Initialized empty Spectre repository.

echo "hello world" > main.txt
python spectre.py save
# => Comment for this snapshot: initial greeting

python spectre.py log
# => [snapshot_id] [timestamp] - initial greeting ← PTR
```

---

## 🛡 Requirements

- Python 3.8+
- Works well in Unix-like systems (tested in WSL2, Ubuntu 22.04)

---

## ✨ Roadmap Ideas

- `spectre show <id>` to preview snapshot contents without switching
- `spectre diff <id1> <id2>` to show differences
- Export/import snapshot stack
- Named snapshots (aliases)
- Lock `PTR` for safe mode

---

## 🧑‍💻 Author

Luis Vásquez

---

