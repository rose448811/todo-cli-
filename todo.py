


















#!/usr/bin/env python3
"""
Simple Todo List CLI Tool
Usage: python todo.py [command] [options]
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

TODO_FILE = Path.home() / ".todo.json"

def load_todos():
    if TODO_FILE.exists():
        try:
            with open(TODO_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def add_task(task):
    todos = load_todos()
    todos.append({
        "id": len(todos) + 1,
        "task": task,
        "done": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    })
    save_todos(todos)
    print(f"✓ Added: {task}")

def list_tasks(show_all=False):
    todos = load_todos()
    if not todos:
        print("No tasks yet! 🎉")
        return

    print("\n📋 Your Todo List\n" + "─" * 50)
    
    for todo in todos:
        if todo["done"] and not show_all:
            continue
            
        status = "✅" if todo["done"] else "⬜"
        task_text = f"\033[9m{todo['task']}\033[0m" if todo["done"] else todo["task"]
        
        print(f"{todo['id']:2d}. {status} {task_text}")
    
    pending = sum(1 for t in todos if not t["done"])
    print(f"\n📊 {pending} pending | {len(todos) - pending} completed")

def complete_task(task_id):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == task_id:
            if todo["done"]:
                print(f"Task #{task_id} is already completed.")
                return
            todo["done"] = True
            todo["completed_at"] = datetime.now().isoformat()
            save_todos(todos)
            print(f"✅ Completed: {todo['task']}")
            return
    print(f"❌ Task #{task_id} not found.")

def delete_task(task_id):
    todos = load_todos()
    original_len = len(todos)
    todos = [t for t in todos if t["id"] != task_id]
    
    if len(todos) < original_len:
        # Re-number remaining tasks
        for i, todo in enumerate(todos):
            todo["id"] = i + 1
        save_todos(todos)
        print(f"🗑️  Deleted task #{task_id}")
    else:
        print(f"❌ Task #{task_id} not found.")

def clear_all():
    if TODO_FILE.exists():
        confirm = input("⚠️  Delete ALL tasks? This cannot be undone. (y/N): ")
        if confirm.lower() == 'y':
            os.remove(TODO_FILE)
            print("🧹 All tasks cleared.")
        else:
            print("Cancelled.")
    else:
        print("No tasks to clear.")

def main():
    parser = argparse.ArgumentParser(description="Simple Todo List CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", nargs="+", help="Task description")

    # List tasks
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("-a", "--all", action="store_true", help="Show completed tasks too")

    # Complete task
    complete_parser = subparsers.add_parser("done", help="Mark a task as done")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # Delete task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Clear all
    subparsers.add_parser("clear", help="Delete all tasks")

    args = parser.parse_args()

    if not args.command:
        list_tasks()
        return

    if args.command == "add":
        task_text = " ".join(args.task)
        add_task(task_text)
    elif args.command == "list":
        list_tasks(show_all=args.all)
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "clear":
        clear_all()

if __name__ == "__main__":
    main()
