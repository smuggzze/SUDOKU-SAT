import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file with the results.
df = pd.read_csv('benchmark_results.csv')

# Filter the data for each solver and outcome.
# For brute force:
bf_solved = df[(df['solver'] == 'brute') & (df['outcome'] == 'solved')]
bf_dnf    = df[(df['solver'] == 'brute') & (df['outcome'] == 'DNF')]
# For SAT:
sat_solved = df[(df['solver'] == 'sat') & (df['outcome'] == 'solved')]
sat_dnf    = df[(df['solver'] == 'sat') & (df['outcome'] == 'DNF')]

plt.figure(figsize=(10, 6))

# Plot brute force results:
plt.scatter(bf_solved['removals'], bf_solved['time_ms'], 
            color='blue', marker='o', label='Brute Solved')
plt.scatter(bf_dnf['removals'], bf_dnf['time_ms'], 
            color='red', marker='o', label='Brute DNF')

# Plot SAT results:
plt.scatter(sat_solved['removals'], sat_solved['time_ms'], 
            color='green', marker='^', label='SAT Solved')
if not sat_dnf.empty:
    plt.scatter(sat_dnf['removals'], sat_dnf['time_ms'], 
                color='orange', marker='^', label='SAT DNF')

plt.xlabel('Number of Removals (Empty Cells)')
plt.ylabel('Time (ms)')
plt.title('Solver Benchmark: Time vs. Number of Removals')
plt.legend()
plt.grid(True)
plt.show()
