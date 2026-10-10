from time import perf_counter


def count_charging_stops(actions):
    """
    Count how many recharge actions occurred in a solution.
    """

    return sum(
        1
        for action in actions
        if action.startswith("Recharge")
    )


def count_moves(actions):
    """
    Count movement actions in a solution.
    """

    return sum(
        1
        for action in actions
        if action.startswith("Move")
    )


def measure_algorithm(
    algorithm_name,
    search_function,
    warehouse,
):
    """
    Run one search algorithm and collect its metrics.
    """

    start_time = perf_counter()

    result = search_function(
        warehouse
    )

    end_time = perf_counter()

    execution_time_ms = (
        end_time - start_time
    ) * 1000

    charging_stops = count_charging_stops(
        result["actions"]
    )

    moves = count_moves(
        result["actions"]
    )

    return {
        "algorithm": algorithm_name,
        "success": result["success"],
        "total_cost": result["total_cost"],
        "nodes_expanded": result["nodes_expanded"],
        "execution_time_ms": execution_time_ms,
        "charging_stops": charging_stops,
        "moves": moves,
        "path": result["path"],
        "actions": result["actions"],
    }