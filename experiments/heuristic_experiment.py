import csv
import os
from time import perf_counter

from warehouse.generator import generate_warehouse
from search.astar import a_star_search

from search.heuristics import (
    zero_heuristic,
    half_manhattan_heuristic,
    primary_heuristic,
)


HEURISTICS = [
    ("h=0", zero_heuristic),
    ("0.5x Manhattan", half_manhattan_heuristic),
    ("Manhattan", primary_heuristic),
]


def run_heuristic_experiment(
    number_of_seeds=20,
    output_file="results/heuristic_results.csv",
):
    results = []

    for seed in range(number_of_seeds):
        warehouse = generate_warehouse(
            rows=8,
            cols=8,
            obstacle_density=0.15,
            charger_count=3,
            battery_capacity=12,
            initial_battery=12,
            min_movement_time=1,
            max_movement_time=5,
            seed=seed,
            start=(0, 0),
            goal=(7, 7),
            ensure_solution=True,
        )

        for heuristic_name, heuristic_function in HEURISTICS:
            start_time = perf_counter()

            result = a_star_search(
                warehouse,
                heuristic_function=heuristic_function,
            )

            end_time = perf_counter()

            results.append(
                {
                    "seed": seed,
                    "heuristic": heuristic_name,
                    "success": result["success"],
                    "total_cost": result["total_cost"],
                    "nodes_expanded": result["nodes_expanded"],
                    "execution_time_ms": (
                        end_time - start_time
                    ) * 1000,
                }
            )

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True,
    )

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "seed",
                "heuristic",
                "success",
                "total_cost",
                "nodes_expanded",
                "execution_time_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nHEURISTIC EXPERIMENT")
    print("=" * 60)

    for heuristic_name, _ in HEURISTICS:
        matching = [
            result
            for result in results
            if result["heuristic"] == heuristic_name
        ]

        successful = [
            result
            for result in matching
            if result["success"]
        ]

        average_cost = sum(
            result["total_cost"]
            for result in successful
        ) / len(successful)

        average_nodes = sum(
            result["nodes_expanded"]
            for result in successful
        ) / len(successful)

        average_time = sum(
            result["execution_time_ms"]
            for result in successful
        ) / len(successful)

        print(f"\n{heuristic_name}")
        print("-" * len(heuristic_name))

        print(
            "Success:",
            f"{len(successful)}/{len(matching)}",
        )

        print(
            f"Average cost: {average_cost:.2f}"
        )

        print(
            f"Average nodes: {average_nodes:.2f}"
        )

        print(
            f"Average runtime: {average_time:.4f} ms"
        )

    print(
        "\nResults saved to:",
        output_file,
    )


if __name__ == "__main__":
    run_heuristic_experiment()