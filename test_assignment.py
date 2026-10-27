import ast
import importlib
import inspect
import textwrap

import pytest

import assignment


@pytest.fixture
def q():
    return importlib.reload(assignment)


def calls_in(function):
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.append(node.func.id)
            if isinstance(node.func, ast.Attribute):
                names.append("." + node.func.attr)
    return names


def check_no_list_methods(function):
    for name in calls_in(function):
        if name in [".append", ".pop", ".insert", ".remove", ".extend", ".clear"]:
            pytest.fail(
                function.__name__ + "() uses " + name + "(). "
                "Move the pointers yourself and store with Queue[pointer] = ..."
            )


def test1_initial_queue(q):
    assert q.Queue == ["", "", "", "", "", ""]
    assert q.HeadPointer == -1
    assert q.TailPointer == -1


def test1_enqueue(q):
    assert q.Enqueue("Bat") == True
    assert q.HeadPointer == 0
    assert q.TailPointer == 0
    assert q.Queue[0] == "Bat"
    assert q.Enqueue("Saraa") == True
    assert q.HeadPointer == 0
    assert q.TailPointer == 1
    assert q.Queue[1] == "Saraa"


def test1_enqueue_when_full(q):
    for name in ["A", "B", "C", "D", "E", "F"]:
        assert q.Enqueue(name) == True
    assert q.Enqueue("G") == False
    assert q.TailPointer == 5
    assert q.Queue == ["A", "B", "C", "D", "E", "F"]


def test1_dequeue(q):
    q.Enqueue("Bat")
    q.Enqueue("Saraa")
    q.Enqueue("Anu")
    assert q.Dequeue() == "Bat"
    assert q.HeadPointer == 1
    assert q.Dequeue() == "Saraa"
    assert q.Dequeue() == "Anu"


def test1_dequeue_when_empty(q):
    assert q.Dequeue() == ""
    q.Enqueue("Bat")
    q.Dequeue()
    assert q.Dequeue() == ""


def test1_linear_queue_problem(q):
    for name in ["A", "B", "C", "D", "E", "F"]:
        q.Enqueue(name)
    q.Dequeue()
    q.Dequeue()
    assert q.Enqueue("G") == False
    assert q.Dequeue() == "C"


def test1_uses_pointers(q):
    check_no_list_methods(q.Enqueue)
    check_no_list_methods(q.Dequeue)
    for x in range(8):
        q.Enqueue("P" + str(x))
    for x in range(8):
        q.Dequeue()
    assert len(q.Queue) == 6


def test2_initial_queue(q):
    assert q.CircularQueue == ["", "", "", "", "", ""]
    assert q.CircularHead == -1
    assert q.CircularTail == -1
    assert q.NumberItems == 0


def test2_enqueue_and_dequeue(q):
    assert q.CircularEnqueue("Bat") == True
    assert q.CircularHead == 0
    assert q.CircularTail == 0
    assert q.NumberItems == 1
    assert q.CircularEnqueue("Saraa") == True
    assert q.CircularEnqueue("Anu") == True
    assert q.NumberItems == 3
    assert q.CircularDequeue() == "Bat"
    assert q.CircularHead == 1
    assert q.NumberItems == 2
    assert q.CircularDequeue() == "Saraa"


def test2_wraps_around(q):
    for name in ["A", "B", "C", "D", "E", "F"]:
        assert q.CircularEnqueue(name) == True
    assert q.CircularEnqueue("X") == False
    assert q.CircularDequeue() == "A"
    assert q.CircularDequeue() == "B"
    assert q.CircularEnqueue("G") == True
    assert q.CircularTail == 0
    assert q.CircularQueue[0] == "G"
    assert q.CircularEnqueue("H") == True
    assert q.CircularTail == 1
    assert q.CircularEnqueue("I") == False
    assert q.NumberItems == 6
    result = []
    for x in range(6):
        result.append(q.CircularDequeue())
    assert result == ["C", "D", "E", "F", "G", "H"]


def test2_empty_resets_pointers(q):
    assert q.CircularDequeue() == ""
    q.CircularEnqueue("Bat")
    q.CircularEnqueue("Saraa")
    q.CircularDequeue()
    q.CircularDequeue()
    assert q.NumberItems == 0
    assert q.CircularHead == -1
    assert q.CircularTail == -1
    assert q.CircularDequeue() == ""


def test2_show_queue(q):
    assert q.ShowQueue() == ""
    q.CircularEnqueue("Bat")
    assert q.ShowQueue() == "Bat"
    q.CircularEnqueue("Saraa")
    q.CircularEnqueue("Anu")
    assert q.ShowQueue() == "Bat, Saraa, Anu"
    assert q.NumberItems == 3
    assert q.CircularHead == 0


def test2_show_queue_after_wrap(q):
    for name in ["A", "B", "C", "D", "E", "F"]:
        q.CircularEnqueue(name)
    q.CircularDequeue()
    q.CircularDequeue()
    q.CircularDequeue()
    q.CircularEnqueue("G")
    q.CircularEnqueue("H")
    assert q.ShowQueue() == "D, E, F, G, H"
    assert q.CircularDequeue() == "D"


def test2_uses_pointers(q):
    check_no_list_methods(q.CircularEnqueue)
    check_no_list_methods(q.CircularDequeue)
    for x in range(20):
        q.CircularEnqueue("P" + str(x))
        q.CircularDequeue()
    assert len(q.CircularQueue) == 6


@pytest.mark.parametrize("names, passes, expected", [
    [["Bat", "Saraa", "Anu", "Dorj", "Tuya"], 2, "Dorj"],
    [["Bat", "Saraa", "Anu", "Dorj", "Tuya"], 1, "Anu"],
    [["Bat", "Saraa", "Anu", "Dorj", "Tuya"], 0, "Tuya"],
    [["Bat", "Saraa", "Anu", "Dorj", "Tuya", "Bold"], 3, "Tuya"],
    [["Bat", "Saraa"], 7, "Bat"],
    [["Bat"], 4, "Bat"],
    [[], 2, ""],
])
def test3_hot_potato(q, names, passes, expected):
    assert q.HotPotato(names, passes) == expected


def test3_starts_with_empty_queue(q):
    q.CircularEnqueue("Old1")
    q.CircularEnqueue("Old2")
    assert q.HotPotato(["Bat", "Saraa", "Anu", "Dorj", "Tuya"], 2) == "Dorj"
    assert q.HotPotato(["Bat", "Saraa", "Anu", "Dorj", "Tuya"], 1) == "Anu"


def test3_uses_circular_queue(q):
    names = calls_in(q.HotPotato)
    assert "CircularEnqueue" in names, "HotPotato() must call CircularEnqueue()."
    assert "CircularDequeue" in names, "HotPotato() must call CircularDequeue()."
    assert q.HotPotato(["Bat", "Saraa", "Anu"], 1) == "Anu"
