def solve(text, keys):
    """Розбирає вміст /proc/<pid>/status; повертає словник значень полів із keys (keys=None: усіх)."""
    raise NotImplementedError  # TODO: реалізуйте розв'язок за карткою


if __name__ == "__main__":
    with open("/proc/self/status", encoding="utf-8") as handle:
        print(solve(handle.read(), ["Name", "Pid", "VmRSS"]))
