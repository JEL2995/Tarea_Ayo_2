import itertools
import math
import random
import matplotlib.pyplot as plt

# 1 CALCULAR DISTANCIAS
def distance_matrix(points):
    n = len(points)

    return [
        [math.dist(points[i], points[j]) for j in range(n)]
        for i in range(n)
    ]


def tour_length(dist, tour):
    return sum(
        dist[tour[i]][tour[(i + 1) % len(tour)]]
        for i in range(len(tour))
    )

# 2. MST - ALGORITMO DE PRIM
def mst_prim(points):
    """Algoritmo MST original de p2.py."""

    best = {
        v: (math.dist(points[0], points[v]), 0)
        for v in range(1, len(points))
    }

    children = {v: [] for v in range(len(points))}

    while best:
        v = min(best, key=lambda u: best[u][0])

        parent = best.pop(v)[1]
        children[parent].append(v)

        for u in best:
            d = math.dist(points[v], points[u])

            if d < best[u][0]:
                best[u] = (d, v)

    return children


# 3 RECORRIDO PREORDER


def preorder(children, root=0):
    return [root] + [
        c
        for child in children[root]
        for c in preorder(children, child)
    ]


# 4 RUTA OPTIMA - FUERZA BRUTA

def brute_force(dist):
    n = len(dist)

    best_route = None
    best_distance = float("inf")

    # La primera ciudad siempre es 0
    for perm in itertools.permutations(range(1, n)):

        # Evitar comparar una ruta con su inversa
        if perm[0] > perm[-1]:
            continue

        route = (0,) + perm
        distance = tour_length(dist, route)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return list(best_route), best_distance



# 5 MEJORA CON 2-OPT

def two_opt(dist, route):
    route = route.copy()
    n = len(route)
    improvements = 0

    while True:
        best_distance = tour_length(dist, route)
        best_route = route

        for i in range(1, n - 1):
            for k in range(i + 1, n):

                new_route = (
                    route[:i]
                    + route[i:k + 1][::-1]
                    + route[k + 1:]
                )

                new_distance = tour_length(dist, new_route)

                if new_distance < best_distance - 1e-10:
                    best_distance = new_distance
                    best_route = new_route

        if best_route == route:
            break

        route = best_route
        improvements += 1

    return route, improvements



# 6 REALIZAR 100 PRUEBAS

def run_experiment():

    random.seed(7)

    num_tests = 100
    num_cities = 9

    mst_ratios = []
    opt_ratios = []
    improvements_count = []

    example = None

    print("=== MST APPROXIMATION EXPERIMENT ===")

    for test in range(num_tests):

        # Generar 9 ciudades aleatorias
        points = [
            (random.uniform(0, 10),
             random.uniform(0, 10))
            for _ in range(num_cities)
        ]

        dist = distance_matrix(points)

        # Ruta MST
        mst_route = preorder(mst_prim(points))
        mst_distance = tour_length(dist, mst_route)

        # Ruta optima
        optimal_route, optimal_distance = brute_force(dist)

        # Aplicar 2-opt
        improved_route, improvements = two_opt(dist, mst_route)
        improved_distance = tour_length(dist, improved_route)

        # Calcular ratios
        mst_ratio = mst_distance / optimal_distance
        improved_ratio = improved_distance / optimal_distance

        mst_ratios.append(mst_ratio)
        opt_ratios.append(improved_ratio)
        improvements_count.append(improvements)

        print(
            f"Test {test + 1:3d} | "
            f"MST: {mst_ratio:.3f} | "
            f"MST + 2-opt: {improved_ratio:.3f} | "
            f"Improvements: {improvements}"
        )

        # Guardar la primera prueba para graficar rutas
        if test == 0:
            example = {
                "points": points,
                "mst": mst_route,
                "improved": improved_route,
                "optimal": optimal_route
            }

    # 7 RESULTADOS FINALES


    print("\n=== FINAL RESULTS ===")

    print("Total tests:", num_tests)

    print("Average MST ratio:",
          round(sum(mst_ratios) / num_tests, 4))

    print("Average MST + 2-opt ratio:",
          round(sum(opt_ratios) / num_tests, 4))

    print("Maximum MST ratio:",
          round(max(mst_ratios), 4))

    print("Maximum MST + 2-opt ratio:",
          round(max(opt_ratios), 4))

    print("Average 2-opt improvements:",
          round(sum(improvements_count) / num_tests, 2))

    print("Tests improved by 2-opt:",
          sum(a < b - 1e-10
              for a, b in zip(opt_ratios, mst_ratios)))

    # ==========================================
    # 8. GENERAR GRAFICAS
    # ==========================================

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    tests = list(range(1, num_tests + 1))

    # GRAFICA 1: RATIOS DE LAS 100 PRUEBAS
    axs[0, 0].plot(
        tests, mst_ratios,
        label="MST",
        color="red",
        marker=".",
        linewidth=1
    )

    axs[0, 0].plot(
        tests, opt_ratios,
        label="MST + 2-opt",
        color="green",
        marker=".",
        linewidth=1
    )

    axs[0, 0].axhline(
        y=2,
        color="black",
        linestyle="--",
        label="Theoretical bound = 2"
    )

    axs[0, 0].axhline(
        y=1,
        color="blue",
        linestyle=":",
        label="Optimal ratio = 1"
    )

    axs[0, 0].set_title("Approximation Ratio - 100 Tests")
    axs[0, 0].set_xlabel("Test Number")
    axs[0, 0].set_ylabel("Approximation Ratio")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # GRAFICA 2: PROMEDIO DE RATIOS
    averages = [
        sum(mst_ratios) / num_tests,
        sum(opt_ratios) / num_tests
    ]

    bars = axs[0, 1].bar(
        ["MST", "MST + 2-opt"],
        averages,
        color=["red", "green"]
    )

    axs[0, 1].axhline(
        y=1,
        color="blue",
        linestyle="--",
        label="Optimal"
    )

    axs[0, 1].set_title("Average Approximation Ratio")
    axs[0, 1].set_ylabel("Average Ratio")
    axs[0, 1].set_ylim(0, 2.1)
    axs[0, 1].legend()
    axs[0, 1].grid(axis="y")

    for bar, value in zip(bars, averages):
        axs[0, 1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.3f}",
            ha="center",
            va="bottom"
        )

    # GRAFICA 3: MEJORAS DE 2-OPT
    axs[1, 0].bar(
        tests,
        improvements_count,
        color="purple"
    )

    axs[1, 0].set_title("2-opt Improvements per Test")
    axs[1, 0].set_xlabel("Test Number")
    axs[1, 0].set_ylabel("Number of Improvements")
    axs[1, 0].grid(axis="y")

    # GRAFICA 4: COMPARAR RUTAS DE LA PRIMERA PRUEBA
    points = example["points"]

    def draw_route(route, label, color):
        x = [points[i][0] for i in route]
        y = [points[i][1] for i in route]

        # Regresar a la ciudad inicial
        x.append(x[0])
        y.append(y[0])

        axs[1, 1].plot(
            x, y,
            marker="o",
            label=label,
            color=color,
            alpha=0.75
        )

    draw_route(example["mst"], "MST", "red")
    draw_route(example["improved"], "MST + 2-opt", "green")
    draw_route(example["optimal"], "Optimal", "blue")

    for i, (x, y) in enumerate(points):
        axs[1, 1].annotate(
            str(i),
            (x, y),
            xytext=(5, 5),
            textcoords="offset points"
        )

    axs[1, 1].set_title("Route Comparison - Test 1")
    axs[1, 1].set_xlabel("X")
    axs[1, 1].set_ylabel("Y")
    axs[1, 1].set_aspect("equal", adjustable="box")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    run_experiment()

