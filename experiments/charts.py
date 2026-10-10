import csv
import os

import matplotlib.pyplot as plt


RESULT_FILES = {
    "map_size": "results/map_size_results.csv",
    "obstacle_density": "results/obstacle_density_results.csv",
    "movement_cost": "results/movement_cost_results.csv",
    "battery_capacity": "results/battery_capacity_results.csv",
    "charger_availability": "results/charger_availability_results.csv",
    "heuristic": "results/heuristic_results.csv",
    "distance": "results/start_goal_distance_results.csv",
}


def read_csv(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as csv_file:
        return list(
            csv.DictReader(csv_file)
        )


def safe_float(value):
    if value in (
        None,
        "",
        "None",
    ):
        return None

    return float(value)


def average(values):
    clean_values = [
        value
        for value in values
        if value is not None
    ]

    if not clean_values:
        return None

    return sum(clean_values) / len(clean_values)


def group_algorithm_metric(
    rows,
    factor_column,
    metric_column,
):
    grouped = {}

    for row in rows:
        factor = row[factor_column]
        algorithm = row["algorithm"]

        value = safe_float(
            row[metric_column]
        )

        key = (
            factor,
            algorithm,
        )

        grouped.setdefault(
            key,
            [],
        )

        grouped[key].append(
            value
        )

    averages = {}

    for key, values in grouped.items():
        averages[key] = average(
            values
        )

    return averages


def make_algorithm_chart(
    file_path,
    factor_column,
    metric_column,
    title,
    x_label,
    y_label,
    output_name,
):
    rows = read_csv(
        file_path
    )

    grouped = group_algorithm_metric(
        rows,
        factor_column,
        metric_column,
    )

    factors = sorted(
        {
            row[factor_column]
            for row in rows
        },
        key=lambda value: float(
            value.split("-")[0]
        ),
    )

    algorithms = [
        "UCS",
        "Greedy Best-First",
        "A*",
    ]

    plt.figure(
        figsize=(8, 5)
    )

    for algorithm in algorithms:
        y_values = []

        for factor in factors:
            value = grouped.get(
                (
                    factor,
                    algorithm,
                )
            )

            y_values.append(
                value
            )

        plt.plot(
            factors,
            y_values,
            marker="o",
            label=algorithm,
        )

    plt.title(
        title
    )

    plt.xlabel(
        x_label
    )

    plt.ylabel(
        y_label
    )

    plt.legend()

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    os.makedirs(
        "results/charts",
        exist_ok=True,
    )

    output_path = os.path.join(
        "results/charts",
        output_name,
    )

    plt.savefig(
        output_path,
        dpi=200,
    )

    plt.close()

    print(
        "Saved:",
        output_path,
    )


def make_success_chart(
    file_path,
    factor_column,
    title,
    x_label,
    output_name,
):
    rows = read_csv(
        file_path
    )

    factors = sorted(
        {
            row[factor_column]
            for row in rows
        },
        key=float,
    )

    algorithms = [
        "UCS",
        "Greedy Best-First",
        "A*",
    ]

    plt.figure(
        figsize=(8, 5)
    )

    for algorithm in algorithms:
        percentages = []

        for factor in factors:
            matching = [
                row
                for row in rows
                if row[factor_column] == factor
                and row["algorithm"] == algorithm
            ]

            successes = sum(
                1
                for row in matching
                if row["success"] == "True"
            )

            if matching:
                percentage = (
                    successes
                    / len(matching)
                ) * 100
            else:
                percentage = 0

            percentages.append(
                percentage
            )

        plt.plot(
            factors,
            percentages,
            marker="o",
            label=algorithm,
        )

    plt.title(
        title
    )

    plt.xlabel(
        x_label
    )

    plt.ylabel(
        "Success Rate (%)"
    )

    plt.ylim(
        0,
        105,
    )

    plt.legend()

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    os.makedirs(
        "results/charts",
        exist_ok=True,
    )

    output_path = os.path.join(
        "results/charts",
        output_name,
    )

    plt.savefig(
        output_path,
        dpi=200,
    )

    plt.close()

    print(
        "Saved:",
        output_path,
    )


def make_heuristic_chart():
    rows = read_csv(
        RESULT_FILES["heuristic"]
    )

    heuristics = [
        "h=0",
        "0.5x Manhattan",
        "Manhattan",
    ]

    average_nodes = []

    for heuristic in heuristics:
        matching = [
            row
            for row in rows
            if row["heuristic"] == heuristic
        ]

        values = [
            safe_float(
                row["nodes_expanded"]
            )
            for row in matching
        ]

        average_nodes.append(
            average(values)
        )

    plt.figure(
        figsize=(8, 5)
    )

    plt.bar(
        heuristics,
        average_nodes,
    )

    plt.title(
        "Effect of Heuristic Quality on A* Search"
    )

    plt.xlabel(
        "Heuristic"
    )

    plt.ylabel(
        "Average Nodes Expanded"
    )

    plt.tight_layout()

    os.makedirs(
        "results/charts",
        exist_ok=True,
    )

    output_path = (
        "results/charts/"
        "heuristic_nodes.png"
    )

    plt.savefig(
        output_path,
        dpi=200,
    )

    plt.close()

    print(
        "Saved:",
        output_path,
    )


def generate_all_charts():
    make_algorithm_chart(
        RESULT_FILES["map_size"],
        "factor_value",
        "nodes_expanded",
        "Search Effort vs Map Size",
        "Map Size",
        "Average Nodes Expanded",
        "map_size_nodes.png",
    )

    make_algorithm_chart(
        RESULT_FILES["map_size"],
        "factor_value",
        "total_cost",
        "Solution Cost vs Map Size",
        "Map Size",
        "Average Solution Cost",
        "map_size_cost.png",
    )

    make_algorithm_chart(
        RESULT_FILES["obstacle_density"],
        "factor_value",
        "nodes_expanded",
        "Search Effort vs Obstacle Density",
        "Obstacle Density",
        "Average Nodes Expanded",
        "obstacle_density_nodes.png",
    )

    make_algorithm_chart(
        RESULT_FILES["movement_cost"],
        "factor_value",
        "total_cost",
        "Solution Cost vs Movement-Time Range",
        "Movement-Time Cost Range",
        "Average Solution Cost",
        "movement_cost_solution_cost.png",
    )

    make_success_chart(
        RESULT_FILES["battery_capacity"],
        "factor_value",
        "Feasibility vs Battery Capacity",
        "Battery Capacity",
        "battery_success_rate.png",
    )

    make_success_chart(
        RESULT_FILES["charger_availability"],
        "factor_value",
        "Feasibility vs Charger Availability",
        "Number of Chargers",
        "charger_success_rate.png",
    )

    make_algorithm_chart(
        RESULT_FILES["distance"],
        "distance",
        "nodes_expanded",
        "Search Effort vs Start-to-Goal Distance",
        "Manhattan Distance",
        "Average Nodes Expanded",
        "distance_nodes.png",
    )

    make_algorithm_chart(
        RESULT_FILES["distance"],
        "distance",
        "total_cost",
        "Solution Cost vs Start-to-Goal Distance",
        "Manhattan Distance",
        "Average Solution Cost",
        "distance_cost.png",
    )

    make_heuristic_chart()

    print(
        "\nAll charts generated."
    )


if __name__ == "__main__":
    generate_all_charts()