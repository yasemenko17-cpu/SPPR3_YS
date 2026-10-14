"""Навантаження для задач 6-8: функції з відомими виділеннями пам'яті.

Коментарі виду `# @мітка` позначають рядки, номери яких повертають розв'язки; тести шукають їх за міткою.
"""
import itertools

# ------------------------------------------------------------- задача 6: де виділено пам'ять


def workload_6a():
    big = bytearray(800_000)  # @6A-big
    middle = bytearray(200_000)  # @6A-middle
    small = bytearray(50_000)  # @6A-small
    return big, middle, small


def workload_6b():
    rows = []
    for i in range(2000):
        rows.append(bytes(500))  # @6B-rows
    temp = bytearray(3_000_000)  # @6B-temp
    del temp
    index = {i: i for i in range(500)}  # @6B-index
    return rows, index


def workload_6c():
    words = [str(i) * 20 for i in range(1000)]  # @6C-words
    return words


# ------------------------------------------------------------- задача 7: витоки між знімками
LEAK_STORE = []
REGISTRY = {}
COUNTER = itertools.count()
CALLS = []


def reset_leaks():
    LEAK_STORE.clear()
    REGISTRY.clear()
    CALLS.clear()
    leaky_default.__defaults__[1].clear()


def leaky_list():
    CALLS.append(1)
    scratch = bytearray(200_000)  # @7A-scratch
    LEAK_STORE.append(bytes(1000))  # @7A-leak
    return len(scratch)


def leaky_cache():
    CALLS.append(1)
    key = next(COUNTER)
    REGISTRY[key] = str(key) * 200  # @7B-leak
    return len(REGISTRY)


def leaky_default(item=None, history=[]):
    CALLS.append(1)
    history.append(bytearray(2000))  # @7C-leak
    return len(history)


def leaky_two():
    CALLS.append(1)
    LEAK_STORE.append(bytes(3000))  # @7D-big
    REGISTRY[next(COUNTER)] = bytes(1000)  # @7D-small
    return len(LEAK_STORE)


def clean_workload():
    CALLS.append(1)
    temp = bytearray(500_000)  # @7E-temp
    return len(temp)


class Node:
    pass


def cyclic_garbage():
    CALLS.append(1)
    a = Node()
    b = Node()
    a.other = b
    b.other = a
    a.payload = bytearray(100_000)  # @7F-cycle
    return 0


# ------------------------------------------------------------- задача 8: поточна й пікова пам'ять
def peak_a():
    kept = bytes(1024 * 1024)  # @8A-kept
    temp = bytearray(4 * 1024 * 1024)  # @8A-temp
    del temp  # тимчасовий буфер зникає, але пік його пам'ятає
    return kept


def peak_b(n):
    data = [i for i in range(n)]
    return sum(data)


def peak_c(parts, size):
    return [bytes(size) for _ in range(parts)]
