# Python Queue 1

Read the Abstract Data Types lecture (Queue section) before you start.
https://drive.google.com/file/d/1jXGQdSvuUYjGXl-PUuHMUzKWEBGQoARL/view?usp=sharing

**Rules for this assignment**

- Do **not** use `.append()` or `.pop()` inside the Enqueue and Dequeue functions.
  Move the pointers yourself and store with `Queue[TailPointer] = ...`. The tests check for this.
- Functions **return** their answer — do not print.
- Use `global` for every queue variable a function changes.

---

## Exercise 1

**Problem:**

Build a **linear queue** of names for a ticket line.

Set up the queue:

- `Queue` → a global array of **6** elements, all set to `""` (empty string)
- `HeadPointer` → a global integer, set to `-1`
- `TailPointer` → a global integer, set to `-1`

Then write two functions:

`Enqueue(Name)`

- If the queue is full (`TailPointer` is 5), return `False`
- Otherwise add 1 to `TailPointer`, store `Name` at `Queue[TailPointer]`,
  and return `True`
- If this is the **first** item ever (`HeadPointer` is -1), set `HeadPointer` to 0

`Dequeue()`

- If the queue is empty (`HeadPointer` is -1, or `HeadPointer` is more than
  `TailPointer`), return `""`
- Otherwise return the name at `Queue[HeadPointer]`, and add 1 to `HeadPointer`

**Example:**

    Input:
      print(Enqueue("Bat"))
      print(Enqueue("Saraa"))
      print(Enqueue("Anu"))
      print(Dequeue())
      print(Dequeue())
      print(HeadPointer, TailPointer)

    Output:
      True
      True
      True
      Bat
      Saraa
      2 2

**This is a linear queue.** After 6 names have joined, `Enqueue` returns
`False` — even if some names have already left. That is the problem the
circular queue in Exercise 2 fixes.

    Input:
      Enqueue 6 names, then Dequeue() twice, then:
      print(Enqueue("G"))

    Output:
      False

---

## Exercise 2

**Problem:**

Build a **circular queue** that reuses the free spaces.

Set up the queue:

- `CircularQueue` → a global array of **6** elements, all set to `""`
- `CircularHead` and `CircularTail` → global integers, both set to `-1`
- `NumberItems` → a global integer, set to `0`

Then write three functions:

`CircularEnqueue(Name)`

- If the queue is full (`NumberItems` is 6), return `False`
- If the queue is empty, set `CircularHead` and `CircularTail` to 0
- Otherwise add 1 to `CircularTail` — and if it reaches **6**, set it back to **0**
- Store `Name` at `CircularQueue[CircularTail]`, add 1 to `NumberItems`, return `True`

`CircularDequeue()`

- If the queue is empty (`NumberItems` is 0), return `""`
- Otherwise read the name at `CircularQueue[CircularHead]`
- Add 1 to `CircularHead` — and if it reaches **6**, set it back to **0**
- Take 1 off `NumberItems`
- If the queue is now empty, set `CircularHead` and `CircularTail` back to `-1`
- Return the name

`ShowQueue()`

- Return all the names from the **front** to the **back** of the queue,
  with `", "` between them. Return `""` if the queue is empty.
- Start at `CircularHead` and take `NumberItems` steps — remember to wrap
  back to 0 when you reach the end of the array.
- Do **not** change the queue.

**Example:**

    Input:
      Enqueue A, B, C, D, E, F
      print(CircularEnqueue("X"))
      CircularDequeue()
      CircularDequeue()
      CircularDequeue()
      print(CircularEnqueue("G"))
      print(CircularEnqueue("H"))
      print(CircularTail)
      print(ShowQueue())

    Output:
      False
      True
      True
      1
      D, E, F, G, H

`G` was stored at index 0 and `H` at index 1 — the tail **wrapped around**.
`ShowQueue()` still lists them in queue order: D, E, F, then G, H.

---

## Exercise 3

**Problem:**

`HotPotato(Names, Passes)`

A party game. Everyone stands in a circle and passes a hot potato. After
`Passes` passes, whoever is holding the potato is **out**. Keep going until one
person is left — the **winner**.

Use **your circular queue** from Exercise 2:

1. **Empty the queue first:** set `CircularHead` and `CircularTail` to `-1`
   and `NumberItems` to `0`.
2. Enqueue every name in `Names` (there are at most 6).
3. While more than one person is in the queue:
    - Do `Passes` passes. One pass = dequeue the person at the front and
      enqueue them again at the back.
    - Dequeue the person now at the front — they are out.
4. Return the name of the last person left. If `Names` is empty, return `""`.

**Example:**

    Input:
      print(HotPotato(["Bat", "Saraa", "Anu", "Dorj", "Tuya"], 2))

    Output:
      Dorj

How it works (front of the queue on the left):

    Start:                       Bat Saraa Anu Dorj Tuya
    2 passes -> Anu is out:      Dorj Tuya Bat Saraa
    2 passes -> Bat is out:      Saraa Dorj Tuya
    2 passes -> Tuya is out:     Saraa Dorj
    2 passes -> Saraa is out:    Dorj          <- winner

    Input:                                         Output:
      HotPotato(["Bat", "Saraa", "Anu"], 1)          Anu
      HotPotato(["Bat"], 4)                          Bat

The queue keeps going round and round — that only works because it is **circular**.

---
