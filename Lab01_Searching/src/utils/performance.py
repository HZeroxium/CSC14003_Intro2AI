import time  # for timing
import tracemalloc  # for memory usage tracking
from utils.graph import Graph


def measure_performance(algorithm, graph: Graph, start: int, goal: int):
    tracemalloc.start()
    start_time = time.time()
    # print("Start time: ", start_time)
    path = algorithm(graph, start, goal)
    end_time = time.time()
    # print("End time: ", end_time)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    time_taken = end_time - start_time
    memory_used = peak / 1024  # Convert to KB

    return path, time_taken, memory_used
