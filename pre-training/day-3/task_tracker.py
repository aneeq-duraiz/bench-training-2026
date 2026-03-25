import json
import sys
import os
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


class Task:
    def __init__(self, id, title, status="todo", created_at=None):
        self.id = id
        self.title = title
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            status=data.get("status", "todo"),
            created_at=data.get("created_at"),
        )


class TaskManager:
    def __init__(self):
        self.tasks = []
        self._load()

    # ------------------------------------------------------------------ data persistence

    def _load(self):
        if not os.path.exists(TASKS_FILE):
            self.tasks = []
            return
        try:
            with open(TASKS_FILE, "r") as f:
                raw = json.load(f)
            if not isinstance(raw, list):
                raise ValueError("Expected a JSON array at the top level.")
            self.tasks = [Task.from_dict(item) for item in raw]
        except (json.JSONDecodeError, ValueError, KeyError) as exc:
            print(f"[error] tasks.json is corrupt or invalid ({exc}). Starting with an empty task list.")
            self.tasks = []

    def _save(self):
        with open(TASKS_FILE, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    # ------------------------------------------------------------------ helpers

    def _next_id(self):
        return max((t.id for t in self.tasks), default=0) + 1

    def _find(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    # ------------------------------------------------------------------ main features

    def add_task(self, title):
        task = Task(id=self._next_id(), title=title)
        self.tasks.append(task)
        self._save()
        print(f"[added] #{task.id}: {task.title}")
        return task

    def complete_task(self, task_id):
        task = self._find(task_id)
        if task is None:
            print(f"[error] No task with id {task_id}.")
            return
        if task.status == "done":
            print(f"[info] Task #{task_id} is already marked as done.")
            return
        task.status = "done"
        self._save()
        print(f"[done] #{task.id}: {task.title}")

    def list_tasks(self, filter=None):
        tasks = self.tasks
        if filter == "done":
            tasks = [t for t in tasks if t.status == "done"]
        elif filter == "todo":
            tasks = [t for t in tasks if t.status == "todo"]
        elif filter is not None:
            print(f"[error] Unknown filter '{filter}'. Use 'todo' or 'done'.")
            return

        if not tasks:
            print("No tasks found.")
            return

        col_id    = max(len(str(t.id)) for t in tasks)
        col_title = max(len(t.title)   for t in tasks)

        header = f"{'ID':<{col_id}}  {'STATUS':<6}  {'CREATED AT':<19}  TITLE"
        print(header)
        print("-" * len(header))
        for t in tasks:
            status_marker = "done" if t.status == "done" else "todo"
            created = t.created_at[:19].replace("T", " ")
            print(f"{t.id:<{col_id}}  {status_marker:<6}  {created:<19}  {t.title}")

    def delete_task(self, task_id):
        task = self._find(task_id)
        if task is None:
            print(f"[error] No task with id {task_id}.")
            return
        self.tasks.remove(task)
        self._save()
        print(f"[deleted] #{task.id}: {task.title}")


# -------------------------------------------------------------------- CLI entry

def _usage():
    print(
        "Usage:\n"
        "  python task_tracker.py add '<title>'\n"
        "  python task_tracker.py done <id>\n"
        "  python task_tracker.py delete <id>\n"
        "  python task_tracker.py list [--filter todo|done]"
    )


def main():
    args = sys.argv[1:]

    if not args:
        _usage()
        sys.exit(1)

    manager = TaskManager()
    command = args[0]

    if command == "add":
        if len(args) < 2 or not args[1].strip():
            print("[error] Please provide a title: python task_tracker.py add '<title>'")
            sys.exit(1)
        manager.add_task(args[1].strip())

    elif command == "done":
        if len(args) < 2:
            print("[error] Please provide a task id: python task_tracker.py done <id>")
            sys.exit(1)
        try:
            task_id = int(args[1])
        except ValueError:
            print(f"[error] Task id must be an integer, got '{args[1]}'.")
            sys.exit(1)
        manager.complete_task(task_id)

    elif command == "delete":
        if len(args) < 2:
            print("[error] Please provide a task id: python task_tracker.py delete <id>")
            sys.exit(1)
        try:
            task_id = int(args[1])
        except ValueError:
            print(f"[error] Task id must be an integer, got '{args[1]}'.")
            sys.exit(1)
        manager.delete_task(task_id)

    elif command == "list":
        filter_value = None
        if "--filter" in args:
            idx = args.index("--filter")
            if idx + 1 >= len(args):
                print("[error] --filter requires a value: 'todo' or 'done'.")
                sys.exit(1)
            filter_value = args[idx + 1]
        manager.list_tasks(filter=filter_value)

    else:
        print(f"[error] Unknown command '{command}'.")
        _usage()
        sys.exit(1)


if __name__ == "__main__":
    main()

