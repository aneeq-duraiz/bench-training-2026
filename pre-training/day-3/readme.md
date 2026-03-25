# Task Tracker CLI

A command-line task manager that persists tasks to `tasks.json`.

## Usage

```bash
python3 task_tracker.py add "<title>"
python3 task_tracker.py done <id>
python3 task_tracker.py delete <id>
python3 task_tracker.py list
python3 task_tracker.py list --filter todo
python3 task_tracker.py list --filter done
```

## Examples

```
$ python3 task_tracker.py add "go to gym"
[added] #2: go to gym

$ python3 task_tracker.py list
ID  STATUS  CREATED AT           TITLE
---------------------------------------
1   done    2026-03-25 18:12:46  make lunch
2   todo    2026-03-25 18:16:41  go to gym
```

## Design: Why a Class Instead of Just Functions?

The `TaskManager` class holds the task list as `self.tasks`, meaning it is loaded once and shared across every method call (`add_task`, `complete_task`, `list_tasks`, `delete_task`). With plain functions you would have to pass that list as an argument to every single function, or store it in a global variable, both of which make the code harder to follow and test.

In short: the class bundles the state and behaviours on one place, which is exactly the problem classes are designed to solve.
