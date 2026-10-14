"""Готує дані свого варіанта для ручного запуску.

Використання:  python build_dataset.py <номер варіанта 1..30> <каталог>
Для задач 3, 5 і 10 у каталозі створюється файл з даними картки (status.txt, maps.txt, records.txt).
Скрипт друкує номер задачі й виклик solve(...), який відтворює картку.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
import cases  # noqa: E402

TEXTS = {
    3: [cases.STATUS_A, cases.STATUS_B, cases.STATUS_C],
    5: [cases.MAPS_A, cases.MAPS_B, cases.MAPS_C],
    10: [cases.FILE_A, cases.FILE_B, cases.FILE_C],
}
FILES = {3: "status.txt", 5: "maps.txt", 10: "records.txt"}
CALLS = {
    1: ["solve(['alpha', 'beta', 'gamma'])",
        "solve({'a': shared, 'b': shared, 'c': (shared, 'x')})  # shared = [1000, 2000, 3000]",
        "solve(node)  # node = {'name': 'ab', 'next': node}"],
    2: ["solve(['x', 'y', 'z'], 2000)", "solve(['id', 'name', 'price', 'qty', 'unit', 'tag'], 1000)",
        "solve(['f0', 'f1', ..., 'f9'], 500)"],
    3: ["solve(open('status.txt').read(), ['Pid', 'VmRSS', 'Name'])",
        "solve(open('status.txt').read(), ['State', 'Threads', 'voluntary_ctxt_switches', 'VmSwap'])",
        "solve(open('status.txt').read(), ['Name', 'Groups', 'VmData', 'VmLib', 'Cpus_allowed_list'])"],
    4: ["solve(48)", "solve(64)", "solve(96)"],
    5: ["solve(open('maps.txt').read())"] * 3,
    6: ["solve(workloads.workload_6a, 2)", "solve(workloads.workload_6b, 2)", "solve(workloads.workload_6c, 10)"],
    7: ["solve(workloads.leaky_list, 40, 20000)", "solve(workloads.leaky_cache, 100, 5000)",
        "solve(workloads.leaky_default, 50, 50000)"],
    8: ["solve(workloads.peak_a)", "solve(workloads.peak_b, 100000)", "solve(workloads.peak_c, 5, 100000)"],
    9: ["solve(200000, lambda x: x * x)", "solve(300000, lambda x: x % 1000)", "solve(500000, lambda x: len(str(x)))"],
    10: ["solve('records.txt', 100, 2)", "solve('records.txt', 0, 3)", "solve('records.txt', -100, 5)"],
}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    number = int(sys.argv[1])
    if not 1 <= number <= 30:
        print("Номер варіанта має бути від 1 до 30")
        return 1
    task, index = (number - 1) // 3 + 1, (number - 1) % 3
    print(f"Задача {task}, файл variants/variant_{task:02d}.py")
    if task in TEXTS:
        target = Path(sys.argv[2]).resolve()
        target.mkdir(parents=True, exist_ok=True)
        (target / FILES[task]).write_text(TEXTS[task][index], encoding="utf-8")
        print(f"Дані записано: {target / FILES[task]}")
    if task in (6, 7, 8):
        print("Перед викликом: sys.path.insert(0, 'tests'); import workloads")
    print("Виклик: " + CALLS[task][index])
    return 0


if __name__ == "__main__":
    sys.exit(main())
