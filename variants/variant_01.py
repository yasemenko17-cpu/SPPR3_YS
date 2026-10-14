def solve(obj):
    """Повертає сумарний sys.getsizeof усіх РІЗНИХ об'єктів, досяжних із obj через list, tuple, set, frozenset, dict."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    print(solve(["alpha", "beta", "gamma"]))
