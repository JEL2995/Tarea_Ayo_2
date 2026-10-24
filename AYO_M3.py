
import math
import random
import matplotlib.pyplot as plt


def tour_length(route, cities):
    return sum(
        math.dist(
            cities[route[i]],
            cities[route[(i + 1) % len(route)]]
        )
        for i in range(len(route))
    )


def two_opt_move(route, i, k):
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]


def nearest_neighbour(cities):
    unvisited = set(cities.keys())

    current = 0
    route = [current]
    unvisited.remove(current)

    while unvisited:

        nearest = min(
            unvisited,
            key=lambda city: (
                math.dist(cities[current], cities[city]),
                city
            )
        )

        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return route


def random_tour(cities):
    route = list(cities.keys())

    # Mantener la ciudad inicial fija
    remaining = route[1:]
    random.shuffle(remaining)

    return [route[0]] + remaining


def two_opt(route, cities):
    route = route.copy()
    improvements = 0

    while True:

        best_route = route
        best_distance = tour_length(route, cities)

        for i in range(1, len(route) - 1):
            for k in range(i + 1, len(route)):

                new_route = two_opt_move(route, i, k)
                new_distance = tour_length(new_route, cities)

                if new_distance < best_distance - 1e-10:
                    best_distance = new_distance
                    best_route = new_route

        if best_route == route:
            break

        route = best_route
        improvements += 1

    return route, improvements



def run_experiment():

    random.seed(42)

    num_tests = 100
    num_cities = 10

    nn_improvements = []
    random_improvements = []

    nn_distances = []
    random_distances = []

    print("=== LOCAL SEARCH: 2-OPT ===")

    for test in range(num_tests):

        cities = {
            i: (
                random.uniform(0, 100),
                random.uniform(0, 100)
            )
            for i in range(num_cities)
        }

        nn_route = nearest_neighbour(cities)
        nn_final, nn_count = two_opt(nn_route, cities)

        rand_route = random_tour(cities)
        rand_final, rand_count = two_opt(rand_route, cities)

        nn_improvements.append(nn_count)
        random_improvements.append(rand_count)

        nn_distances.append(tour_length(nn_final, cities))
        random_distances.append(tour_length(rand_final, cities))

        print(
            f"Test {test + 1:3d} | "
            f"NN improvements: {nn_count:2d} | "
            f"Random improvements: {rand_count:2d} | "
            f"NN distance: {nn_distances[-1]:.2f} | "
            f"Random distance: {random_distances[-1]:.2f}"
        )


    avg_nn_imp = sum(nn_improvements) / num_tests
    avg_rand_imp = sum(random_improvements) / num_tests

    avg_nn_dist = sum(nn_distances) / num_tests
    avg_rand_dist = sum(random_distances) / num_tests

    print("\n=== FINAL RESULTS ===")

    print(f"Nearest Neighbour avg improvements: {avg_nn_imp:.2f}")
    print(f"Random Tour avg improvements: {avg_rand_imp:.2f}")

    print(f"Nearest Neighbour avg distance: {avg_nn_dist:.2f}")
    print(f"Random Tour avg distance: {avg_rand_dist:.2f}")

    fewer = sum(
        a < b for a, b in
        zip(nn_improvements, random_improvements)
    )

    equal = sum(
        a == b for a, b in
        zip(nn_improvements, random_improvements)
    )

    print(f"NN required fewer improvements: {fewer} tests")
    print(f"Same number of improvements: {equal} tests")


    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    methods = ["Nearest Neighbour", "Random Tour"]


    box1 = axs[0, 0].boxplot(
        [nn_improvements, random_improvements],
        tick_labels=methods,
        patch_artist=True
    )

    for patch, color in zip(
        box1["boxes"], ["skyblue", "orange"]
    ):
        patch.set_facecolor(color)

    axs[0, 0].set_title("2-opt Improvements - Boxplot")
    axs[0, 0].set_ylabel("Number of Improvements")
    axs[0, 0].grid(axis="y")

    bars1 = axs[0, 1].bar(
        methods,
        [avg_nn_imp, avg_rand_imp],
        color=["skyblue", "orange"]
    )

    axs[0, 1].set_title("Average Number of Improvements")
    axs[0, 1].set_ylabel("Average Improvements")
    axs[0, 1].grid(axis="y")

    for bar in bars1:
        axs[0, 1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{bar.get_height():.2f}",
            ha="center",
            va="bottom"
        )

    box2 = axs[1, 0].boxplot(
        [nn_distances, random_distances],
        tick_labels=methods,
        patch_artist=True
    )

    for patch, color in zip(
        box2["boxes"], ["skyblue", "orange"]
    ):
        patch.set_facecolor(color)

    axs[1, 0].set_title("Final Solution Quality - Boxplot")
    axs[1, 0].set_ylabel("Final Tour Distance")
    axs[1, 0].grid(axis="y")

    bars2 = axs[1, 1].bar(
        methods,
        [avg_nn_dist, avg_rand_dist],
        color=["skyblue", "orange"]
    )

    axs[1, 1].set_title("Average Final Distance")
    axs[1, 1].set_ylabel("Average Tour Distance")
    axs[1, 1].grid(axis="y")

    for bar in bars2:
        axs[1, 1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{bar.get_height():.2f}",
            ha="center",
            va="bottom"
        )

    plt.suptitle(
        "Local Search: Nearest Neighbour vs Random Tour",
        fontsize=15
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_experiment()
