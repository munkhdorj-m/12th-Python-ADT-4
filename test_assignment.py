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
                "Move the pointers yourself and store with Queue[TailPointer] = ..."
            )


def empty_the_queue(q):
    items = []
    for x in range(q.NumberItems):
        items.append(q.Dequeue())
    return items


def test1_initial_queue(q):
    assert q.Queue == [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    assert q.HeadPointer == -1
    assert q.TailPointer == -1
    assert q.NumberItems == 0


def test1_enqueue(q):
    assert q.Enqueue(15) == True
    assert q.HeadPointer == 0
    assert q.TailPointer == 0
    assert q.NumberItems == 1
    assert q.Queue[0] == 15
    assert q.Enqueue(27) == True
    assert q.TailPointer == 1
    assert q.NumberItems == 2


def test1_enqueue_when_full(q):
    for x in range(10):
        assert q.Enqueue(x) == True
    assert q.Enqueue(99) == False
    assert q.NumberItems == 10
    assert q.Queue == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test1_dequeue(q):
    q.Enqueue(10)
    q.Enqueue(20)
    q.Enqueue(30)
    assert q.Dequeue() == 10
    assert q.HeadPointer == 1
    assert q.NumberItems == 2
    assert q.Dequeue() == 20
    assert q.Dequeue() == 30


def test1_dequeue_when_empty(q):
    assert q.Dequeue() == -999
    q.Enqueue(-1)
    assert q.Dequeue() == -1
    assert q.NumberItems == 0
    assert q.HeadPointer == -1
    assert q.TailPointer == -1
    assert q.Dequeue() == -999


def test1_wraps_around(q):
    for x in range(10):
        q.Enqueue(x)
    q.Dequeue()
    q.Dequeue()
    q.Dequeue()
    assert q.Enqueue(10) == True
    assert q.TailPointer == 0
    assert q.Queue[0] == 10
    assert q.Enqueue(11) == True
    assert q.Enqueue(12) == True
    assert q.TailPointer == 2
    assert q.Enqueue(13) == False
    assert empty_the_queue(q) == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def test1_uses_pointers(q):
    check_no_list_methods(q.Enqueue)
    check_no_list_methods(q.Dequeue)
    for x in range(25):
        q.Enqueue(x)
        q.Dequeue()
    assert len(q.Queue) == 10


@pytest.mark.parametrize("content, expected_count, expected_items", [
    ["5\n10\n15\n", 3, [5, 10, 15]],
    ["7\n\n-3\n\n", 2, [7, -3]],
    ["42", 1, [42]],
    ["", 0, []],
])
def test2_load_queue(q, tmp_path, content, expected_count, expected_items):
    path = tmp_path / "numbers.txt"
    path.write_text(content)
    assert q.LoadQueue(path) == expected_count
    assert q.NumberItems == expected_count
    assert empty_the_queue(q) == expected_items


def test2_load_when_full(q, tmp_path, capsys):
    path = tmp_path / "numbers.txt"
    path.write_text("1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n")
    assert q.LoadQueue(path) == 10
    assert capsys.readouterr().out.count("Queue full") == 1
    assert empty_the_queue(q) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test2_adds_to_back(q, tmp_path):
    q.Enqueue(100)
    path = tmp_path / "numbers.txt"
    path.write_text("1\n2\n3\n")
    assert q.LoadQueue(path) == 3
    assert empty_the_queue(q) == [100, 1, 2, 3]


@pytest.mark.parametrize("items, expected_removed, expected_items", [
    [[5, -2, 7, -1, 3], 2, [5, 7, 3]],
    [[1, 2, 3], 0, [1, 2, 3]],
    [[-5, 0, -6], 2, [0]],
    [[], 0, []],
])
def test3_remove_negatives(q, items, expected_removed, expected_items):
    for item in items:
        q.Enqueue(item)
    assert q.RemoveNegatives() == expected_removed
    assert q.NumberItems == len(expected_items)
    assert empty_the_queue(q) == expected_items


def test3_after_wrap_around(q):
    for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        q.Enqueue(x)
    for x in range(6):
        q.Dequeue()
    for x in [-11, 12, -13, 14]:
        q.Enqueue(x)
    assert q.RemoveNegatives() == 2
    assert empty_the_queue(q) == [7, 8, 9, 10, 12, 14]


def test3_all_negative(q):
    for x in [-1, -2, -3]:
        q.Enqueue(x)
    assert q.RemoveNegatives() == 3
    assert q.NumberItems == 0
    assert q.HeadPointer == -1
    assert q.TailPointer == -1
    assert q.Dequeue() == -999
