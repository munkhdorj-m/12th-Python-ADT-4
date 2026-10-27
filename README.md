# Python Queue 2

Read the Abstract Data Types lecture (Queue section) before you start.
https://drive.google.com/file/d/1jXGQdSvuUYjGXl-PUuHMUzKWEBGQoARL/view?usp=sharing

**Rules for this assignment**

- Do **not** use `.append()` or `.pop()` inside `Enqueue()` and `Dequeue()`.
  Move the pointers yourself and store with `Queue[TailPointer] = ...`. The tests check for this.
- Functions **return** their answer. Only print when the exercise says so.
- Use `global Queue, HeadPointer, TailPointer, NumberItems` in every function that changes them.

## Exercise 1

**Problem:**

Build a **circular queue** of integers.

Set up the queue:

- `Queue` → a global array of **10** elements, all set to `-1`
- `HeadPointer` and `TailPointer` → global integers, both set to `-1`
- `NumberItems` → a global integer, set to `0`

Then write two functions:

`Enqueue(Data)`

- If the queue is full (`NumberItems` is 10), return `False`
- If the queue is empty, set `HeadPointer` and `TailPointer` to 0
- Otherwise add 1 to `TailPointer` — and if it reaches **10**, set it back to **0**
- Store `Data` at `Queue[TailPointer]`, add 1 to `NumberItems`, and return `True`

`Dequeue()`

- If the queue is empty (`NumberItems` is 0), return **`-999`**
- Otherwise read the item at `Queue[HeadPointer]`
- Add 1 to `HeadPointer` — and if it reaches **10**, set it back to **0**
- Take 1 off `NumberItems`
- If the queue is now empty, set `HeadPointer` and `TailPointer` back to `-1`
- Return the item

**Why -999 and not -1?** This queue can hold negative numbers, so `-1` could be
a real item. The rogue value must be something that can never be real data.

**Example:**

    Input:
      Enqueue(10)
      Enqueue(20)
      Enqueue(30)
      print(Dequeue())
      print(Dequeue())
      print(NumberItems, HeadPointer, TailPointer)
      print(Dequeue())
      print(Dequeue())

    Output:
      10
      20
      1 2 2
      30
      -999

---

## Exercise 2

**Problem:**

`LoadQueue(Filename)`

The file has one whole number on each line. Read the file and **enqueue** each
number, as an **integer**, at the back of the queue. Skip any blank lines.

- If `Enqueue()` returns `False`, print `Queue full` **once** and stop.
- Return how many numbers were added.
- Do **not** empty the queue first — the numbers go after anything already in it.

**Example:**

    Example File Content (numbers.txt):
        5
        10
        15

    Example Input:
        print(LoadQueue("numbers.txt"))
        print(Dequeue())

    Program Output:
        3
        5

    Example File Content (numbers.txt):
        1
        2
        ...
        12

    Program Output:
        Queue full
        10

Only the first 10 numbers fit.

---

## Exercise 3

**Problem:**

`RemoveNegatives()`

Remove every **negative** number from the queue, but keep the other numbers
in the **same order**. Return how many numbers were removed.

Use only `Enqueue()` and `Dequeue()`:

1. Store how many items are in the queue **before** you start.
2. Repeat that many times:
    - Dequeue the item at the front.
    - If it is **not** negative, enqueue it again at the back.

`0` is not negative — keep it.

**Example:**

    Queue before (front → back):   5  -2  7  -1  3

    Input:
      print(RemoveNegatives())

    Output:
      2

    Queue after (front → back):    5  7  3

*Hint:* why store the count first? `NumberItems` changes while you are
dequeuing and enqueuing. If your loop checks `NumberItems` every time, it
will stop at the wrong moment.

---
