"""Тридцять наборів даних з карток: по три для кожної з десяти задач.

Кожна функція s<NN><A|B|C> перевіряє розв'язок m на даних відповідного варіанта. Очікувані значення задачі 3, 5, 9 і 10
пораховано вручну з умови картки; для задач із вимірюваннями перевіряються властивості й співвідношення.
"""
import os
import sys
import tracemalloc
from pathlib import Path

import pytest

import workloads as w

HERE = Path(w.__file__).resolve()
SOURCE = HERE.read_text(encoding="utf-8").splitlines()
MIB = 1024 * 1024


def line_of(marker):
    """Номер рядка workloads.py, що містить коментар `# @marker`."""
    hits = [i for i, text in enumerate(SOURCE, 1) if text.rstrip().endswith("# @" + marker)]
    assert len(hits) == 1, marker
    return hits[0]


def size(obj):
    return sys.getsizeof(obj)


# ------------------------------------------------------------------ задача 1: повний розмір
def s01a(m):
    obj = ["alpha", "beta", "gamma"]
    assert m.solve(obj) == size(obj) + size("alpha") + size("beta") + size("gamma")


def s01b(m):
    shared = [1000, 2000, 3000]
    tup = (shared, "x")
    obj = {"a": shared, "b": shared, "c": tup}
    expected = (size(obj) + size("a") + size("b") + size("c") + size(shared)
                + size(1000) + size(2000) + size(3000) + size(tup) + size("x"))
    assert m.solve(obj) == expected


def s01c(m):
    node = {"name": "ab", "next": None}
    node["next"] = node
    assert m.solve(node) == size(node) + size("name") + size("ab") + size("next")


# ------------------------------------------------------------------ задача 2: __dict__ проти __slots__
def check_layout(m, fields, count):
    result = m.solve(list(fields), count)
    dict_class, slots_class = result["dict_class"], result["slots_class"]
    assert tuple(slots_class.__slots__) == tuple(fields)
    inst = slots_class()
    assert not hasattr(inst, "__dict__")
    for name in fields:
        setattr(inst, name, 1)
    with pytest.raises(AttributeError):
        inst.not_declared = 1
    plain = dict_class()
    plain.extra = 1
    assert "extra" in vars(plain)
    n = len(fields)
    assert 8 * n <= result["per_slots"] <= 8 * n + 96
    assert result["per_dict"] >= 1.2 * result["per_slots"]
    assert result["saving"] == pytest.approx(result["per_dict"] - result["per_slots"])
    assert not tracemalloc.is_tracing()


def s02a(m):
    check_layout(m, ("x", "y", "z"), 2000)


def s02b(m):
    check_layout(m, ("id", "name", "price", "qty", "unit", "tag"), 1000)


def s02c(m):
    check_layout(m, tuple(f"f{i}" for i in range(10)), 500)


# ------------------------------------------------------------------ задача 3: /proc/self/status
STATUS_A = (
    "Name:\tpython3\n"
    "State:\tS (sleeping)\n"
    "Pid:\t4242\n"
    "VmPeak:\t  120000 kB\n"
    "VmSize:\t  118000 kB\n"
    "VmRSS:\t   30000 kB\n"
    "Threads:\t3\n"
)
STATUS_B = (
    "Name:\tworker\n"
    "State:\tR (running)\n"
    "Threads:\t12\n"
    "VmSwap:\t       0 kB\n"
    "voluntary_ctxt_switches:\t128\n"
    "nonvoluntary_ctxt_switches:\t9\n"
)
STATUS_C = (
    "Name:\ta:b\n"
    "Groups:\t4 24 27\n"
    "Cpus_allowed_list:\t0-3\n"
    "VmData:\t    2048 kB\n"
    "VmStk:\t     132 kB\n"
)


def s03a(m):
    assert m.solve(STATUS_A, ["Pid", "VmRSS", "Name"]) == {"Pid": 4242, "VmRSS": 30_720_000, "Name": "python3"}


def s03b(m):
    keys = ["State", "Threads", "voluntary_ctxt_switches", "VmSwap"]
    assert m.solve(STATUS_B, keys) == {"State": "R (running)", "Threads": 12, "voluntary_ctxt_switches": 128, "VmSwap": 0}


def s03c(m):
    keys = ["Name", "Groups", "VmData", "VmLib", "Cpus_allowed_list"]
    assert m.solve(STATUS_C, keys) == {"Name": "a:b", "Groups": "4 24 27", "VmData": 2_097_152, "Cpus_allowed_list": "0-3"}


# ------------------------------------------------------------------ задача 4: ріст VmRSS
def check_rss(m, mib):
    result = m.solve(mib)
    data = mib * MIB
    assert set(result) == {"before", "during", "after", "hwm"}
    assert all(isinstance(v, int) and v % 1024 == 0 and v > 0 for v in result.values())
    assert result["during"] - result["before"] >= 0.9 * data
    assert result["during"] - result["before"] <= data + 24 * MIB
    assert result["hwm"] >= result["during"]
    assert result["during"] - result["after"] >= 0.8 * data


def s04a(m):
    check_rss(m, 48)


def s04b(m):
    check_rss(m, 64)


def s04c(m):
    check_rss(m, 96)


# ------------------------------------------------------------------ задача 5: /proc/self/maps
MAPS_A = (
    "00400000-00452000 r-xp 00000000 08:01 1234                               /usr/bin/python3\n"
    "00651000-00652000 r--p 00051000 08:01 1234                               /usr/bin/python3\n"
    "00652000-00653000 rw-p 00052000 08:01 1234                               /usr/bin/python3\n"
    "01e3a000-01e5b000 rw-p 00000000 00:00 0                                  [heap]\n"
    "7ffd5c0a0000-7ffd5c0c1000 rw-p 00000000 00:00 0                          [stack]\n"
)
MAPS_B = (
    "7f1000000000-7f1000200000 rw-p 00000000 00:00 0 \n"
    "7f1000200000-7f1000400000 rw-p 00000000 00:00 0 \n"
    "7f1000600000-7f1000601000 r--p 00000000 08:01 77                         /usr/lib/libc.so.6\n"
    "7f1000601000-7f1000780000 r-xp 00001000 08:01 77                         /usr/lib/libc.so.6\n"
    "7f1000800000-7f1000810000 r--p 00000000 08:01 88                         /usr/lib/libm.so.6\n"
    "7ffe00100000-7ffe00102000 r-xp 00000000 00:00 0                          [vdso]\n"
)
MAPS_C = (
    "55d0c0000000-55d0c0004000 r-xp 00000000 fd:00 5                          /opt/my app/tool\n"
    "55d0c0004000-55d0c0005000 rw-p 00004000 fd:00 5                          /opt/my app/tool\n"
    "55d0c1000000-55d0c1100000 rw-p 00000000 00:00 0                          [heap]\n"
    "7f2000000000-7f2000010000 rwxp 00000000 00:00 0 \n"
    "7f2000010000-7f2000011000 ---p 00000000 00:00 0 \n"
    "7f2000100000-7f2000102000 r--s 00000000 00:2b 99                         /tmp/data.bin (deleted)\n"
    "7ffc00000000-7ffc00021000 rw-p 00000000 00:00 0                          [stack]\n"
    "ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0                  [vsyscall]\n"
)


def s05a(m):
    assert m.solve(MAPS_A) == {"regions": 5, "total": 614_400, "heap": 135_168, "stack": 135_168, "anon": 0,
                               "executable": 335_872, "files": [("/usr/bin/python3", 344_064)]}


def s05b(m):
    assert m.solve(MAPS_B) == {"regions": 6, "total": 5_840_896, "heap": 0, "stack": 0, "anon": 4_194_304,
                               "executable": 1_576_960,
                               "files": [("/usr/lib/libc.so.6", 1_572_864), ("/usr/lib/libm.so.6", 65_536)]}


def s05c(m):
    assert m.solve(MAPS_C) == {"regions": 8, "total": 1_286_144, "heap": 1_048_576, "stack": 135_168, "anon": 69_632,
                               "executable": 86_016,
                               "files": [("/opt/my app/tool", 20_480), ("/tmp/data.bin (deleted)", 8192)]}


# ------------------------------------------------------------------ задача 6: найбільші виділення
def within(value, wanted, slack=300):
    return wanted <= value <= wanted + slack


def s06a(m):
    got = m.solve(w.workload_6a, 2)
    assert [line for line, _ in got] == [line_of("6A-big"), line_of("6A-middle")]
    assert within(got[0][1], 800_000) and within(got[1][1], 200_000)
    assert not tracemalloc.is_tracing()


def s06b(m):
    got = m.solve(w.workload_6b, 2)
    assert [line for line, _ in got] == [line_of("6B-rows"), line_of("6B-index")]
    assert got[0][1] >= 2000 * 500  # усі 2000 буферів на одному рядку складаються
    assert 10_000 <= got[1][1] <= 80_000
    assert line_of("6B-temp") not in [line for line, _ in got]  # тимчасовий буфер уже звільнено


def s06c(m):
    got = m.solve(w.workload_6c, 10)
    assert [line for line, _ in got] == [line_of("6C-words")]
    assert 60_000 <= got[0][1] <= 250_000


# ------------------------------------------------------------------ задача 7: витоки
def leaks(m, func, rounds, minimum):
    w.reset_leaks()
    result = m.solve(func, rounds, minimum)
    assert len(w.CALLS) == rounds + 1  # прогрів + rounds викликів
    assert not tracemalloc.is_tracing()
    return result


def s07a(m):
    assert leaks(m, w.leaky_list, 40, 20_000) == [line_of("7A-leak")]


def s07b(m):
    assert leaks(m, w.leaky_cache, 100, 5_000) == [line_of("7B-leak")]


def s07c(m):
    assert leaks(m, w.leaky_default, 50, 50_000) == [line_of("7C-leak")]


# ------------------------------------------------------------------ задача 8: поточна й пікова пам'ять
def s08a(m):
    r = m.solve(w.peak_a)
    assert len(r["result"]) == MIB
    assert MIB <= r["current"] <= MIB + 2048
    assert 5 * MIB <= r["peak"] <= 5 * MIB + 4096
    assert not tracemalloc.is_tracing()


def s08b(m):
    r = m.solve(w.peak_b, 100_000)
    assert r["result"] == 4_999_950_000
    assert r["current"] < 2048
    assert r["peak"] >= 8 * 100_000
    assert r["peak"] >= r["current"]


def s08c(m):
    r = m.solve(w.peak_c, 5, 100_000)
    assert len(r["result"]) == 5 and all(len(x) == 100_000 for x in r["result"])
    assert 500_000 <= r["current"] <= 500_000 + 2048
    assert r["peak"] >= r["current"]


# ------------------------------------------------------------------ задача 9: список проти генератора
def check_lists(m, n, transform, total):
    calls = [0]  # лічильник без росту пам'яті: список викликів спотворив би виміри

    def counted(x):
        calls[0] += 1
        return transform(x)

    r = m.solve(n, counted)
    assert r["total"] == total
    assert calls[0] == 2 * n  # по одному проходу для списку і для генератора
    assert r["list_peak"] >= 8 * n
    assert r["gen_peak"] <= 16 * 1024
    assert r["list_peak"] >= 50 * r["gen_peak"]
    assert not tracemalloc.is_tracing()


def s09a(m):
    n = 200_000
    check_lists(m, n, lambda x: x * x, (n - 1) * n * (2 * n - 1) // 6)


def s09b(m):
    check_lists(m, 300_000, lambda x: x % 1000, 149_850_000)


def s09c(m):
    check_lists(m, 500_000, lambda x: len(str(x)), 2_888_890)


# ------------------------------------------------------------------ задача 10: потоковий розбір
FILE_A = "# замовлення\nalpha;250\nbeta;99\ngamma;100\ndelta;1000\n\nepsilon;40\n"
FILE_B = "x;5\ny;abc\nz\nw;-7\n q ; 12 \nv;3;4\nu;+8\n"
FILE_C = "Яблуко;30\nГруша;30\nАнанас;30\nСлива;-50\nДуля;-150\n"


def run_file(m, tmp_path, text, threshold, k):
    path = tmp_path / "records.txt"
    path.write_text(text, encoding="utf-8")
    before = len(os.listdir("/proc/self/fd"))
    result = m.solve(str(path), threshold, k)
    assert len(os.listdir("/proc/self/fd")) == before  # файл закрито
    return result


def s10a(m, tmp_path):
    assert run_file(m, tmp_path, FILE_A, 100, 2) == {
        "count": 3, "total": 1350, "bad": 0, "top": [(1000, "delta"), (250, "alpha")]}


def s10b(m, tmp_path):
    assert run_file(m, tmp_path, FILE_B, 0, 3) == {
        "count": 3, "total": 25, "bad": 3, "top": [(12, "q"), (8, "u"), (5, "x")]}


def s10c(m, tmp_path):
    assert run_file(m, tmp_path, FILE_C, -100, 5) == {
        "count": 4, "total": 40, "bad": 0,
        "top": [(30, "Ананас"), (30, "Груша"), (30, "Яблуко"), (-50, "Слива")]}


SETS = [(1, "A", s01a), (1, "B", s01b), (1, "C", s01c),
        (2, "A", s02a), (2, "B", s02b), (2, "C", s02c),
        (3, "A", s03a), (3, "B", s03b), (3, "C", s03c),
        (4, "A", s04a), (4, "B", s04b), (4, "C", s04c),
        (5, "A", s05a), (5, "B", s05b), (5, "C", s05c),
        (6, "A", s06a), (6, "B", s06b), (6, "C", s06c),
        (7, "A", s07a), (7, "B", s07b), (7, "C", s07c),
        (8, "A", s08a), (8, "B", s08b), (8, "C", s08c),
        (9, "A", s09a), (9, "B", s09b), (9, "C", s09c),
        (10, "A", s10a), (10, "B", s10b), (10, "C", s10c)]
