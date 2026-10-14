def solve(text):
    """Підсумовує карту адресного простору (вміст /proc/<pid>/maps): розміри областей за категоріями."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    with open("/proc/self/maps", encoding="utf-8") as handle:
        print(solve(handle.read()))
