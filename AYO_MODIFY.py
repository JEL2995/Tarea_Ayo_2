import multiprocessing as mp
import random
import time
import matplotlib.pyplot as plt


def estimate_pi(seed: int, samples: int = 1_000_000) -> float:
    """
    Monte Carlo: fraction of random points that
    fall inside the unit quarter circle.
    """
    rng = random.Random(seed)

    inside = sum(
        rng.random()**2 + rng.random()**2 <= 1.0
        for _ in range(samples)
    )

    return 4 * inside / samples


if __name__ == '__main__':

    seeds = list(range(8))

    # 1. Sequential Looping
    t0 = time.perf_counter()

    seq_results = [estimate_pi(s) for s in seeds]

    t_seq = time.perf_counter() - t0

    print(f'Sequential wall-clock: {t_seq:.3f}s')

    # 2. Parallel Pool Execution
    processes_list = [1, 2, 4, 8]

    times = []
    speedups = []

    for n in processes_list:

        t0 = time.perf_counter()

        with mp.Pool(processes=n) as pool:
            par_results = pool.map(estimate_pi, seeds)

        t_par = time.perf_counter() - t0

        speedup = t_seq / t_par

        times.append(t_par)
        speedups.append(speedup)

        print(f'\nProcesses: {n}')
        print(f'Parallel wall-clock: {t_par:.3f}s')
        print(f'Speedup: {speedup:.2f}x')

    # 3. Plot Speedup
    plt.plot(processes_list, speedups, marker='o',
             label='Actual Speedup')

    plt.plot(processes_list, processes_list, '--',
             label='Ideal Speedup')

    plt.xlabel('Number of Processes')
    plt.ylabel('Speedup')
    plt.title('Parallel Speedup - Monte Carlo Pi')
    plt.xticks(processes_list)
    plt.legend()
    plt.grid(True)
    plt.show()