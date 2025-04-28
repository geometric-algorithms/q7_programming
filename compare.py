import random
import time
import matplotlib.pyplot as plt
from A.A import query as query_a, preprocess as preprocess_a
from B.B import preprocess as preprocess_b, query as query_b

Ns = [100,200,300,400, 500, 1000, 2000,3000,4000,
      5000,6000,7000,8000,9000,10000,20000,30000,40000,50000]

pre_times_a = []
query_times_a = []
pre_times_b = []
query_times_b = []

for N in Ns:
    points = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(N)]
    coords = [random.uniform(-100, 100) for _ in range(4)]
    xmin, xmax = sorted(coords[:2])
    ymin, ymax = sorted(coords[2:])

    start = time.time()
    preprocess_a(points)
    mid = time.time()
    result_a = query_a(xmin, xmax, ymin, ymax)
    end = time.time()

    pre_times_a.append(mid - start)
    query_times_a.append(end - mid)

    start = time.time()
    preprocess_b(points)
    mid = time.time()
    result_b = query_b(xmin, xmax, ymin, ymax)
    end = time.time()

    pre_times_b.append(mid - start)
    query_times_b.append(end - mid)

    if set(result_a) != set(result_b):
        print(f"❌ Results differ for N={N}!")
    else:
        print(f"✅ Results match for N={N}.")


plt.figure(figsize=(10, 6))

plt.plot(Ns, pre_times_a, marker='o', label='Preprocess A', color='blue')
plt.plot(Ns, pre_times_b, marker='o', label='Preprocess B', color='green')

plt.plot(Ns, query_times_a, marker='s', linestyle='--', label='Query A', color='cyan')
plt.plot(Ns, query_times_b, marker='s', linestyle='--', label='Query B', color='lime')

plt.xscale('log') 
plt.yscale('log')   

plt.xlabel('Number of Points (N) [log scale]')
plt.ylabel('Time (seconds) [log scale]')
plt.title('Preprocessing and Query Times vs Number of Points')
plt.grid(True, which="both", linestyle='--', linewidth=0.7)
plt.legend()
plt.tight_layout()
plt.show()
