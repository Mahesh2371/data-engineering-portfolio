# Python Programming FAQ

## What is a list comprehension?
A list comprehension provides a concise way to create lists. It consists of brackets containing an expression followed by a for clause.
Example: `squares = [x**2 for x in range(10)]`

## What is the difference between a list and a tuple?
Lists are mutable, meaning you can change their content after creation. Tuples are immutable; once created, their values cannot be modified. Tuples are generally faster and are used for fixed data.

## What is a decorator in Python?
A decorator is a function that takes another function and extends its behavior without explicitly modifying it. Decorators are applied using the `@` syntax above a function definition.

## What is the GIL?
The Global Interpreter Lock (GIL) is a mutex in CPython that allows only one thread to execute Python bytecode at a time. It simplifies memory management but limits true multi-threading for CPU-bound tasks.

## How does Python manage memory?
Python uses reference counting combined with a cyclic garbage collector. When an object's reference count drops to zero, it is immediately deallocated.

## What is a generator?
A generator is a function that yields values one at a time using the `yield` keyword. It is memory-efficient because it does not store all values in memory at once.

## What is the difference between `==` and `is`?
`==` checks for value equality. `is` checks whether two variables point to the same object in memory.

## What are *args and **kwargs?
`*args` allows a function to accept any number of positional arguments as a tuple. `**kwargs` allows a function to accept any number of keyword arguments as a dictionary.

## How do you handle exceptions in Python?
Use `try`, `except`, `else`, and `finally` blocks. The `except` block catches specific exceptions. The `finally` block always runs regardless of whether an exception occurred.

## What is a virtual environment?
A virtual environment is an isolated Python environment that allows you to manage project-specific dependencies separately from the global Python installation. Use `python -m venv` to create one.
