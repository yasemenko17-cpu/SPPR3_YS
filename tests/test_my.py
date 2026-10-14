from conftest import load
import pytest

solve = load(8).solve  # 8 — номер вашої задачі

def test_empty_workload():
    res = solve(lambda: 42)
    assert res["result"] == 42
    assert res["current"] <= 2048

def test_exception_propagation():
    def bad_func():
        raise ValueError("test error")
    
    with pytest.raises(ValueError, match="test error"):
        solve(bad_func)

def test_peak_memory_tracking():
    def memory_func():
        arr = [0] * 50000
        return len(arr)
    
    res = solve(memory_func)
    assert res["result"] == 50000
    assert res["peak"] >= res["current"]