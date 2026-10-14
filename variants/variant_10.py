def solve(path, threshold, k):
    """Один потоковий прохід по файлу «ім'я;значення»: лічильники й k найбільших записів без завантаження файла в пам'ять."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    import sys
    print(solve(sys.argv[1] if len(sys.argv) > 1 else "records.txt", 0, 3))
