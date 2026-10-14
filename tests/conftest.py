"""Допоміжний завантажувач: підключає файл задачі з теки variants/ (або з VARIANT_DIR)."""
import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VARIANT_DIR = Path(os.environ.get("VARIANT_DIR", ROOT.parent / "variants"))


def load(number):
    """Повертає модуль задачі з номером number (1..10)."""
    path = VARIANT_DIR / f"variant_{number:02d}.py"
    if not path.exists():
        raise FileNotFoundError(f"Не знайдено файл задачі {number:02d} у {VARIANT_DIR}")
    spec = importlib.util.spec_from_file_location(f"variant_{number:02d}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def open_fds():
    """Список відкритих дескрипторів поточного процесу (Linux, /proc/self/fd)."""
    return sorted(int(name) for name in os.listdir("/proc/self/fd"))
