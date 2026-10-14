def solve(func, *args):
    """Викликає func(*args); повертає {"result", "current", "peak"}: результат, приріст пам'яті й пік за час виклику."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "tests")
    import workloads
    print(solve(workloads.peak_b, 100_000))
