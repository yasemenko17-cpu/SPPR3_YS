def solve(fields, count):
    """Будує два класи (зі __dict__ і зі __slots__ за іменами fields) і вимірює пам'ять на екземпляр через tracemalloc."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    print(solve(["x", "y", "z"], 2000))
