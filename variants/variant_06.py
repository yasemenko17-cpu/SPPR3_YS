def solve(func, limit):
    """Виконує func() під tracemalloc і повертає limit найбільших пар (номер рядка, байти) у файлі, де визначено func."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "tests")
    import workloads
    print(solve(workloads.workload_6a, 2))
