import tracemalloc

def solve(func, *args):
    """
    Викликає func(*args) та повертає словник з результатами та статистикою пам'яті:
    {"result", "current", "peak"}
    """
    was_tracing = tracemalloc.is_tracing()
    if not was_tracing:
        tracemalloc.start()
    
    tracemalloc.reset_peak()
    start_current, _ = tracemalloc.get_traced_memory()
    
    try:
        result = func(*args)
    finally:
        end_current, peak = tracemalloc.get_traced_memory()
        current_diff = end_current - start_current
        if not was_tracing:
            tracemalloc.stop()
            
    return {
        "result": result,
        "current": current_diff,
        "peak": peak
    }

if __name__ == "__main__":
    # Імпортуємо навантаження з теки tests
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests')))
    from workloads import peak_b
    
    print(solve(peak_b, 100000))