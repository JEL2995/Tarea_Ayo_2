
import math
import random
import time
import statistics
import matplotlib.pyplot as plt



cities = {
    "A": (0, 0),
    "B": (0, 3),
    "E": (2, 5),
    "D": (4, 3),
    "C": (4, 0)
}


def tour_length(route):
    return sum(
        math.dist(
            cities[route[i]],
            cities[route[(i + 1) % len(route)]]
        )
        for i in range(len(route))
    )

def random_successor(route, rng):
    new_route = route.copy()

    i, j = sorted(rng.sample(range(len(route)), 2))

    new_route[i:j + 1] = reversed(new_route[i:j + 1])

    return new_route


def simulated_annealing(initial_route, cooling_rate, seed):

    rng = random.Random(seed)

    current = initial_route.copy()
    current_distance = tour_length(current)

    best = current.copy()
    best_distance = current_distance

    temperature = 100.0
    min_temperature = 0.01

    iterations = 0

    current_costs = [current_distance]
    best_costs = [best_distance]
    temperatures = [temperature]

    start_time = time.perf_counter()

    while temperature > min_temperature:

        next_route = random_successor(current, rng)
        next_distance = tour_length(next_route)

        delta = next_distance - current_distance

        if delta <= 0 or rng.random() < math.exp(-delta / temperature):
            current = next_route
            current_distance = next_distance

        if current_distance < best_distance:
            best = current.copy()
            best_distance = current_distance

        temperature *= cooling_rate

        iterations += 1

        current_costs.append(current_distance)
        best_costs.append(best_distance)
        temperatures.append(temperature)

    execution_time = time.perf_counter() - start_time

    return {
        "route": best,
        "distance": best_distance,
        "iterations": iterations,
        "time": execution_time,
        "current_costs": current_costs,
        "best_costs": best_costs,
        "temperatures": temperatures
    }



if __name__ == "__main__":

    initial_route = ["A", "D", "E", "B", "C"]

    cooling_schedules = {
        "Fast Cooling": 0.90,
        "Medium Cooling": 0.95,
        "Slow Cooling": 0.99
    }

    colors = {
        "Fast Cooling": "red",
        "Medium Cooling": "blue",
        "Slow Cooling": "green"
    }

    num_trials = 30

    results = {}

    print("=== SIMULATED ANNEALING ===")
    print("Initial Route:", initial_route)
    print("Initial Cost:", round(tour_length(initial_route), 2))


    for name, rate in cooling_schedules.items():

        trials = []

        for test in range(num_trials):

            result = simulated_annealing(
                initial_route,
                rate,
                seed=42 + test
            )

            trials.append(result)

        representative = trials[0]

        avg_cost = statistics.mean(
            r["distance"] for r in trials
        )

        avg_time = statistics.mean(
            r["time"] for r in trials
        )

        results[name] = {
            "trials": trials,
            "representative": representative,
            "avg_cost": avg_cost,
            "avg_time": avg_time
        }

        print(f"\n--- {name} ---")
        print("Cooling Rate:", rate)
        print("Iterations:", representative["iterations"])
        print("Final Route:", representative["route"])
        print("Final Cost:", round(representative["distance"], 4))
        print("Average Cost:", round(avg_cost, 4))
        print("Average Time:", round(avg_time * 1000, 4), "ms")

    #CREAR LAS CUATRO GRAFICAS

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    for name, data in results.items():

        result = data["representative"]

        axs[0, 0].plot(
            result["best_costs"],
            label=name,
            color=colors[name],
            linewidth=2
        )

    axs[0, 0].set_title("Convergence: Cost vs Iterations")
    axs[0, 0].set_xlabel("Iterations")
    axs[0, 0].set_ylabel("Best Cost (Distance)")
    axs[0, 0].legend()
    axs[0, 0].grid(True)


    for name, data in results.items():

        result = data["representative"]

        axs[0, 1].plot(
            result["temperatures"],
            result["current_costs"],
            label=name,
            color=colors[name],
            alpha=0.8
        )

    axs[0, 1].set_xscale("log")
    axs[0, 1].invert_xaxis()

    axs[0, 1].set_title("Current Cost vs Temperature")
    axs[0, 1].set_xlabel("Temperature (High to Low)")
    axs[0, 1].set_ylabel("Current Cost (Distance)")
    axs[0, 1].legend()
    axs[0, 1].grid(True)


    for name, data in results.items():

        trial_times = [
            r["time"] * 1000
            for r in data["trials"]
        ]

        trial_costs = [
            r["distance"]
            for r in data["trials"]
        ]

        axs[1, 0].scatter(
            trial_times,
            trial_costs,
            label=name,
            color=colors[name],
            alpha=0.6,
            s=35
        )

        # Marcar el promedio
        axs[1, 0].scatter(
            data["avg_time"] * 1000,
            data["avg_cost"],
            color=colors[name],
            marker="X",
            s=180,
            edgecolors="black"
        )

    axs[1, 0].set_title("Execution Time vs Final Solution Quality")
    axs[1, 0].set_xlabel("Execution Time (ms)")
    axs[1, 0].set_ylabel("Final Cost (Lower is Better)")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    names = list(results.keys())

    avg_costs = [
        results[name]["avg_cost"]
        for name in names
    ]

    bar_colors = [colors[name] for name in names]

    bars = axs[1, 1].bar(
        names,
        avg_costs,
        color=bar_colors
    )

    axs[1, 1].set_title("Average Final Solution Quality")
    axs[1, 1].set_ylabel("Average Final Cost")
    axs[1, 1].set_ylim(0, max(avg_costs) * 1.2)
    axs[1, 1].grid(axis="y")

    for bar, cost in zip(bars, avg_costs):
        axs[1, 1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{cost:.3f}",
            ha="center",
            va="bottom"
        )

    plt.suptitle(
        "Simulated Annealing - Cooling Schedule Comparison",
        fontsize=16
    )

    plt.tight_layout()
    plt.show()
