# Task Tracker CLI

A simple **command line interface (CLI) application** to track and manage your tasks.  
This project helps you practice working with the filesystem, handling user inputs, and building a functional CLI app without external libraries.

---

## Features

- Add, update, and delete tasks
- Mark tasks as **todo**, **in-progress**, or **done**
- List tasks by status or all at once
- Tasks are stored in a local **JSON file**
- Graceful handling of errors and edge cases

---

## Requirements

- Any programming language (e.g., Python, JavaScript, etc.)
- Native filesystem module (no external libraries/frameworks)
- JSON file stored in the current directory
- JSON file is auto-created if it does not exist
- Uses **positional arguments** in the CLI

---

## Task Properties

Each task will be stored in the JSON file with the following properties:

- **id**: Unique identifier for the task  
- **description**: Short description of the task  
- **status**: `todo`, `in-progress`, or `done`  
- **createdAt**: Date/time the task was created  
- **updatedAt**: Date/time the task was last updated  

---

## Example Usage

```bash
# Adding a new task
task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)

# Updating and deleting tasks
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1

# Marking a task as in progress or done
task-cli mark-in-progress 1
task-cli mark-done 1

# Listing all tasks
task-cli list

# Listing tasks by status
task-cli list done
task-cli list todo
task-cli list in-progress
```