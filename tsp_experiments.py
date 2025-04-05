import time
import random
import math
import numpy as np
import pandas as pd
from algorithms import Greedy, sGreedy, pGreedy, rGreedy, optDistCircularIC

# --- TSP Data Loading ---
def load_tsp_data(filename):
    """Loads TSP data from a .tsp file and converts to id,x,y format."""
    coords = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        start_coords = False
        for line in lines:
            if line.startswith("NODE_COORD_SECTION"):
                start_coords = True
                continue
            if line.startswith("EOF"):
                break
            if start_coords:
                parts = line.strip().split()
                # Format expected by algorithms: (id, x, y)
                coords.append((int(parts[0])-1, float(parts[1]), float(parts[2])))
    return coords

# --- Main Experiment ---
def run_experiments(filename, iterations_list, num_runs):
    """Runs experiments for different algorithms and iterations."""
    cities = load_tsp_data(filename)
    print(f"Running experiments for {filename}...")

    results = {}
    algorithms = {
        "Greedy": Greedy,
        "sGreedy": sGreedy,
        "pGreedy": pGreedy,
        "rGreedy": rGreedy,
        "optDistCircularIC": optDistCircularIC 
    }

    for alg_name, alg_func in algorithms.items():
        print(f"Testing {alg_name}...")
        results[alg_name] = {}
        
        for iterations in iterations_list:
            results[alg_name][iterations] = []
            
            for _ in range(num_runs):
                # Create a shuffled copy for this run
                cities_copy = cities.copy()
                random.shuffle(cities_copy)
                
                # Measure time
                start_time = time.time()
                initial_cost, final_cost, _ = alg_func(cities_copy, iterations)
                end_time = time.time()
                
                # Store results (time, initial_cost, final_cost)
                results[alg_name][iterations].append((end_time - start_time, initial_cost, final_cost))
    
    # --- Print Results ---
    for algorithm, iterations_data in results.items():
        print(f"\n{algorithm}:")
        for iterations, runs in iterations_data.items():
            times = [run[0] for run in runs]
            initial_costs = [run[1] for run in runs]
            final_costs = [run[2] for run in runs]
            
            avg_time = np.mean(times)
            avg_initial_cost = np.mean(initial_costs)
            avg_final_cost = np.mean(final_costs)
            avg_improvement = (1 - avg_final_cost/avg_initial_cost) * 100 if avg_initial_cost > 0 else 0
            
            print(f"  Iterations: {iterations}")
            print(f"    Average Time: {avg_time:.4f} seconds")
            print(f"    Average Initial Cost: {avg_initial_cost:.2f}")
            print(f"    Average Final Cost: {avg_final_cost:.2f}")
            print(f"    Average Improvement: {avg_improvement:.2f}%")
    
    return results

def save_results_to_excel(all_results, filename="tsp_custom_results.xlsx"):
    """Saves the results to an Excel file."""
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    for instance_name, results in all_results.items():
        data = []
        for algorithm, iterations_data in results.items():
            for iterations, runs in iterations_data.items():
                times = [run[0] for run in runs]
                initial_costs = [run[1] for run in runs]
                final_costs = [run[2] for run in runs]
                
                avg_time = np.mean(times)
                avg_initial_cost = np.mean(initial_costs)
                avg_final_cost = np.mean(final_costs)
                avg_improvement = (1 - avg_final_cost/avg_initial_cost) * 100 if avg_initial_cost > 0 else 0
                
                data.append([
                    algorithm, 
                    iterations, 
                    avg_time, 
                    avg_initial_cost, 
                    avg_final_cost,
                    avg_improvement
                ])

        df = pd.DataFrame(data, columns=[
            "Algorithm", 
            "Iterations", 
            "Average Time (s)", 
            "Average Initial Cost",
            "Average Final Cost",
            "Improvement (%)"
        ])
        df.to_excel(writer, sheet_name=instance_name, index=False)

    writer.close()
    print(f"\nResults saved to {filename}")

# --- Main ---
if __name__ == "__main__":
    filenames = ["eil51.tsp", "berlin52.tsp"]
    iterations_list = [100, 1000, 10000]  # Different numbers of iterations
    num_runs = 10  # Number of times to run each algorithm for each iteration count
    all_results = {}

    for filename in filenames:
        all_results[filename] = run_experiments(filename, iterations_list, num_runs)

    save_results_to_excel(all_results)