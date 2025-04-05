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

def save_results_to_excel(all_results):
    """Saves the results to a single Excel file with separate sheets for each TSP instance."""
    # Create a single Excel file for all instances
    filename = "tsp_results_all.xlsx"
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    
    # Get workbook and create formats
    workbook = writer.book
    
    # Format for headers
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1,
        'align': 'center',
    })
    
    # Format for numeric values
    number_format = workbook.add_format({
        'num_format': '0.00',
        'align': 'center',
    })
    
    # Format for percentage values
    percent_format = workbook.add_format({
        'num_format': '0.00%',
        'align': 'center',
    })
    
    # Format for time values
    time_format = workbook.add_format({
        'num_format': '0.0000',
        'align': 'center',
    })
    
    # Format for algorithm names - different algorithms get different colors
    algorithm_formats = {
        'Greedy': workbook.add_format({'bg_color': '#E6F0FF', 'align': 'center'}),
        'sGreedy': workbook.add_format({'bg_color': '#F2E6FF', 'align': 'center'}),
        'pGreedy': workbook.add_format({'bg_color': '#FFE6E6', 'align': 'center'}),
        'rGreedy': workbook.add_format({'bg_color': '#E6FFE6', 'align': 'center'}),
        'optDistCircularIC': workbook.add_format({'bg_color': '#FFF2CC', 'align': 'center'})
    }
    
    # Format for iterations
    iteration_format = workbook.add_format({
        'align': 'center',
        'bold': True
    })
    
    for instance_name, results in all_results.items():
        # Get instance name without extension for the sheet name
        sheet_name = instance_name.split('.')[0]
        
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
                    avg_improvement / 100  # Convert to decimal for percentage formatting
                ])

        df = pd.DataFrame(data, columns=[
            "Algorithm", 
            "Iterations", 
            "Average Time (s)", 
            "Average Initial Cost",
            "Average Final Cost",
            "Improvement"
        ])
        
        # Write data to a sheet named after the instance
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        worksheet = writer.sheets[sheet_name]
        
        # Set column widths
        worksheet.set_column('A:A', 18)  # Algorithm
        worksheet.set_column('B:B', 12)  # Iterations
        worksheet.set_column('C:C', 16)  # Average Time
        worksheet.set_column('D:D', 18)  # Average Initial Cost
        worksheet.set_column('E:E', 18)  # Average Final Cost
        worksheet.set_column('F:F', 14)  # Improvement

        # Set up header row
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Apply conditional formatting to highlight the best results
        worksheet.conditional_format('C2:C100', {'type': '3_color_scale',
                                               'min_color': '#63BE7B',  # Green for low (good) times
                                               'mid_color': '#FFEB84',
                                               'max_color': '#F8696B'})  # Red for high (bad) times
                                           
        worksheet.conditional_format('E2:E100', {'type': '3_color_scale',
                                               'min_color': '#63BE7B',  # Green for low (good) final costs
                                               'mid_color': '#FFEB84',
                                               'max_color': '#F8696B'})  # Red for high (bad) final costs
                                               
        worksheet.conditional_format('F2:F100', {'type': '3_color_scale',
                                               'min_color': '#F8696B',  # Red for low (bad) improvement
                                               'mid_color': '#FFEB84',
                                               'max_color': '#63BE7B'})  # Green for high (good) improvement
        
        # Apply formatting to each row
        for row_num, row in enumerate(df.values, 1):
            algorithm = row[0]
            # Apply algorithm-specific format to the algorithm cell
            worksheet.write(row_num, 0, algorithm, algorithm_formats[algorithm])
            # Apply iteration format
            worksheet.write(row_num, 1, row[1], iteration_format)
            # Apply time format
            worksheet.write(row_num, 2, row[2], time_format)
            # Apply number format to costs
            worksheet.write(row_num, 3, row[3], number_format)
            worksheet.write(row_num, 4, row[4], number_format)
            # Apply percentage format to improvement
            worksheet.write(row_num, 5, row[5], percent_format)
        
        # Add a filter to easily sort and filter data
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
        
        # Freeze the header row
        worksheet.freeze_panes(1, 0)
        
        print(f"Added formatted results for {instance_name} to sheet '{sheet_name}'")
    
    # Close the writer after all sheets have been added
    writer.close()
    print(f"\nAll results saved to {filename}")

# --- Main ---
if __name__ == "__main__":
    filenames = ["eil51.tsp", "berlin52.tsp"]
    iterations_list = [100, 1000, 10000]  # Different numbers of iterations
    num_runs = 10  # Number of times to run each algorithm for each iteration count
    all_results = {}

    for filename in filenames:
        all_results[filename] = run_experiments(filename, iterations_list, num_runs)

    save_results_to_excel(all_results)