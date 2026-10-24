
import matplotlib.pyplot as plt


items = ["A", "B", "C"]
values = [1, 20, 30]
weights = [1, 5, 6]
capacity = 11



# METODO GREEDY

def greedy_knapsack(values, weights, capacity, method):
    n = len(values)

    if method == "weight":
        order = sorted(range(n), key=lambda i: weights[i])

    elif method == "ratio":
        order = sorted(
            range(n),
            key=lambda i: values[i] / weights[i],
            reverse=True
        )
    else:
        raise ValueError("Invalid method")

    selected = []
    total_weight = 0
    total_value = 0

    for i in order:
        if total_weight + weights[i] <= capacity:
            selected.append(items[i])
            total_weight += weights[i]
            total_value += values[i]

    return selected, total_weight, total_value



if __name__ == "__main__":

    result_weight = greedy_knapsack(
        values, weights, capacity, "weight"
    )

    result_ratio = greedy_knapsack(
        values, weights, capacity, "ratio"
    )

    print("=== KNAPSACK COMPARISON ===")

    print("\nLowest Weight First:")
    print("Selected items:", result_weight[0])
    print("Used capacity:", result_weight[1])
    print("Total value:", result_weight[2])

    print("\nValue/Weight Ratio:")
    print("Selected items:", result_ratio[0])
    print("Used capacity:", result_ratio[1])
    print("Total value:", result_ratio[2])


    methods = ["Lowest Weight", "Value/Weight Ratio"]

    results = [result_weight, result_ratio]

    used_capacity = [r[1] for r in results]
    total_values = [r[2] for r in results]

    fig, axs = plt.subplots(
        2, 2,
        figsize=(12, 8),
        gridspec_kw={"height_ratios": [1, 1.2]}
    )

    # GRAFICA 1: CAPACIDAD UTILIZADA
    bars1 = axs[0, 0].bar(
        methods,
        used_capacity,
        color=["orange", "green"]
    )

    axs[0, 0].axhline(
        capacity,
        color="red",
        linestyle="--",
        label=f"Max Capacity = {capacity}"
    )

    axs[0, 0].set_title("Used Capacity Comparison")
    axs[0, 0].set_ylabel("Weight")
    axs[0, 0].set_ylim(0, capacity * 1.25)
    axs[0, 0].legend()
    axs[0, 0].grid(axis="y")

    for bar, value in zip(bars1, used_capacity):
        axs[0, 0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom"
        )

    # GRAFICA 2: VALOR TOTAL
    bars2 = axs[0, 1].bar(
        methods,
        total_values,
        color=["orange", "green"]
    )

    axs[0, 1].set_title("Total Value Comparison")
    axs[0, 1].set_ylabel("Value")
    axs[0, 1].set_ylim(0, max(total_values) * 1.2)
    axs[0, 1].grid(axis="y")

    for bar, value in zip(bars2, total_values):
        axs[0, 1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom"
        )

    # TABLA DE RESULTADOS
    table_data = [
        [
            methods[i],
            ", ".join(results[i][0]),
            str(results[i][1]),
            str(results[i][2])
        ]
        for i in range(2)
    ]

    axs[1, 0].axis("off")

    table = axs[1, 0].table(
        cellText=table_data,
        colLabels=[
            "Method",
            "Selected Items",
            "Used Capacity",
            "Total Value"
        ],
        cellLoc="center",
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    axs[1, 0].set_title("Knapsack Results Table")

    axs[1, 1].set_title("Selected Items by Method")

    for index, method in enumerate(methods):
        for item_index, item in enumerate(items):
            if item in results[index][0]:
                axs[1, 1].barh(
                    index,
                    weights[item_index],
                    left=sum(
                        weights[items.index(x)]
                        for x in results[index][0]
                        if results[index][0].index(x)
                        < results[index][0].index(item)
                    ),
                    label=item if index == 0 else None
                )

                axs[1, 1].text(
                    sum(
                        weights[items.index(x)]
                        for x in results[index][0]
                        if results[index][0].index(x)
                        < results[index][0].index(item)
                    ) + weights[item_index] / 2,
                    index,
                    item,
                    ha="center",
                    va="center"
                )

    axs[1, 1].set_yticks(range(2))
    axs[1, 1].set_yticklabels(methods)
    axs[1, 1].set_xlabel("Used Capacity")
    axs[1, 1].set_xlim(0, capacity + 1)
    axs[1, 1].grid(axis="x")

    plt.tight_layout()
    plt.show()
