def solve(func, rounds, min_growth):
    """Шукає рядки файла func, де пам'ять росте між знімками до і після rounds викликів; повертає номери рядків."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "tests")
    import workloads
    print(solve(workloads.leaky_list, 40, 20_000))
