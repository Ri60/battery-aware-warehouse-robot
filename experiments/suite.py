import csv
import os

from experiments.runner import run_single_instance


BASELINE = {
    "rows": 8,
    "cols": 8,
    "obstacle_density": 0.15,
    "charger_count": 3,
    "battery_capacity": 12,
    "initial_battery": 12,
    "min_movement_time": 1,
    "max_movement_time": 5,
}


def run_factor_experiment(
    experiment_name,
    factor_name,
    factor_values,
    number_of_seeds=20,
    ensure_solution=True,
):
    """
    Vary exactly one factor while keeping all other
    baseline settings unchanged.
    """

    all_results = []

    print("\n" + "=" * 70)
    print(experiment_name)
    print("=" * 70)

    for factor_value in factor_values:
        print(
            f"\nTesting {factor_name} = {factor_value}"
        )

        for seed in range(number_of_seeds):
            settings = BASELINE.copy()

            # Special handling for map size because
            # rows and columns change together.
            if factor_name == "map_size":
                settings["rows"] = factor_value
                settings["cols"] = factor_value

            elif factor_name == "movement_cost_range":
                settings["min_movement_time"] = factor_value[0]
                settings["max_movement_time"] = factor_value[1]

            else:
                settings[factor_name] = factor_value

                # Initial battery should follow capacity
                # when battery capacity is the factor.
                if factor_name == "battery_capacity":
                    settings["initial_battery"] = factor_value

            results = run_single_instance(
                seed=seed,
                rows=settings["rows"],
                cols=settings["cols"],
                obstacle_density=settings["obstacle_density"],
                charger_count=settings["charger_count"],
                battery_capacity=settings["battery_capacity"],
                initial_battery=settings["initial_battery"],
                min_movement_time=settings["min_movement_time"],
                max_movement_time=settings["max_movement_time"],
                ensure_solution=ensure_solution,
            )

            for result in results:
                result["experiment"] = experiment_name
                result["factor"] = factor_name

                if isinstance(factor_value, tuple):
                    result["factor_value"] = (
                        f"{factor_value[0]}-{factor_value[1]}"
                    )
                else:
                    result["factor_value"] = factor_value

                all_results.append(result)

    return all_results


def save_suite_results(
    results,
    output_file,
):
    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True,
    )

    fieldnames = [
        "experiment",
        "factor",
        "factor_value",
        "seed",
        "algorithm",
        "rows",
        "cols",
        "obstacle_density",
        "charger_count",
        "battery_capacity",
        "initial_battery",
        "min_movement_time",
        "max_movement_time",
        "success",
        "total_cost",
        "nodes_expanded",
        "execution_time_ms",
        "charging_stops",
        "moves",
        "suboptimality_ratio",
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)


def summarize_by_factor(results):
    """
    Print compact summaries grouped by
    factor value and algorithm.
    """

    combinations = sorted(
        {
            (
                str(result["factor_value"]),
                result["algorithm"],
            )
            for result in results
        }
    )

    print("\nSUMMARY")
    print("=" * 90)

    for factor_value, algorithm in combinations:

        matching = [
            result
            for result in results
            if str(result["factor_value"]) == factor_value
            and result["algorithm"] == algorithm
        ]

        successful = [
            result
            for result in matching
            if result["success"]
        ]

        success_count = len(successful)
        total_count = len(matching)

        if successful:
            avg_cost = sum(
                result["total_cost"]
                for result in successful
            ) / success_count

            avg_nodes = sum(
                result["nodes_expanded"]
                for result in successful
            ) / success_count

            avg_time = sum(
                result["execution_time_ms"]
                for result in successful
            ) / success_count

            ratios = [
                result["suboptimality_ratio"]
                for result in successful
                if result["suboptimality_ratio"] is not None
            ]

            if ratios:
                avg_ratio = sum(ratios) / len(ratios)
            else:
                avg_ratio = None

        else:
            avg_cost = None
            avg_nodes = None
            avg_time = None
            avg_ratio = None

        print(
            f"\nValue: {factor_value}"
            f" | Algorithm: {algorithm}"
        )

        print(
            f"Success: {success_count}/{total_count}"
        )

        if successful:
            print(
                f"Average cost: {avg_cost:.2f}"
            )

            print(
                f"Average nodes: {avg_nodes:.2f}"
            )

            print(
                f"Average runtime: {avg_time:.4f} ms"
            )

            if avg_ratio is not None:
                print(
                    f"Average suboptimality: "
                    f"{avg_ratio:.3f}"
                )


def run_map_size_experiment():
    results = run_factor_experiment(
        experiment_name="Map Size",
        factor_name="map_size",
        factor_values=[
            6,
            8,
            10,
            12,
        ],
        number_of_seeds=20,
        ensure_solution=True,
    )

    save_suite_results(
        results,
        "results/map_size_results.csv",
    )

    summarize_by_factor(results)


def run_obstacle_experiment():
    results = run_factor_experiment(
        experiment_name="Obstacle Density",
        factor_name="obstacle_density",
        factor_values=[
            0.05,
            0.15,
            0.25,
            0.35,
        ],
        number_of_seeds=20,
        ensure_solution=True,
    )

    save_suite_results(
        results,
        "results/obstacle_density_results.csv",
    )

    summarize_by_factor(results)


def run_movement_cost_experiment():
    results = run_factor_experiment(
        experiment_name="Movement Cost Distribution",
        factor_name="movement_cost_range",
        factor_values=[
            (1, 1),
            (1, 3),
            (1, 5),
            (1, 10),
        ],
        number_of_seeds=20,
        ensure_solution=True,
    )

    save_suite_results(
        results,
        "results/movement_cost_results.csv",
    )

    summarize_by_factor(results)


def run_battery_experiment():
    """
    We deliberately allow failure here because
    battery capacity is supposed to affect feasibility.
    """

    results = run_factor_experiment(
        experiment_name="Battery Capacity",
        factor_name="battery_capacity",
        factor_values=[
            6,
            8,
            10,
            12,
            16,
        ],
        number_of_seeds=20,
        ensure_solution=False,
    )

    save_suite_results(
        results,
        "results/battery_capacity_results.csv",
    )

    summarize_by_factor(results)


def run_charger_experiment():
    """
    We deliberately allow failure here because
    charger availability is supposed to affect feasibility.
    """

    results = run_factor_experiment(
        experiment_name="Charger Availability",
        factor_name="charger_count",
        factor_values=[
            0,
            1,
            2,
            3,
            5,
        ],
        number_of_seeds=20,
        ensure_solution=False,
    )

    save_suite_results(
        results,
        "results/charger_availability_results.csv",
    )

    summarize_by_factor(results)


def run_full_suite():
    print(
        "\nBattery-Aware Warehouse Robot"
        "\nControlled Experiment Suite"
    )

    run_map_size_experiment()
    run_obstacle_experiment()
    run_movement_cost_experiment()
    run_battery_experiment()
    run_charger_experiment()

    print(
        "\nAll controlled experiments completed."
    )


if __name__ == "__main__":
    run_full_suite()