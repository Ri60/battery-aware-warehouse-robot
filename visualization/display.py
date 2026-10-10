def display_warehouse(warehouse, path=None):
    """
    Print a simple grid representation of the warehouse.

    Symbols:
        S = start
        G = goal
        C = charging station
        # = blocked cell
        * = route
        . = open cell
    """

    path_positions = set()

    if path:
        for state in path:
            path_positions.add(state.position)

    print("\nWAREHOUSE MAP")
    print("=" * (warehouse.cols * 4))

    for row in range(warehouse.rows):
        row_display = []

        for col in range(warehouse.cols):
            position = (row, col)

            if position == warehouse.start:
                symbol = "S"

            elif position == warehouse.goal:
                symbol = "G"

            elif position in warehouse.blocked_cells:
                symbol = "#"

            elif position in warehouse.chargers:
                symbol = "C"

            elif position in path_positions:
                symbol = "*"

            else:
                symbol = "."

            row_display.append(symbol)

        print("   ".join(row_display))

    print("=" * (warehouse.cols * 4))

    print("\nLegend:")
    print("S = Start")
    print("G = Goal")
    print("C = Charger")
    print("# = Blocked cell")
    print("* = Selected route")
    print(". = Open cell")


def display_summary(results):
    """
    Display a compact comparison of algorithm results.
    """

    print("\nALGORITHM COMPARISON")
    print("=" * 60)

    print(
        f"{'Algorithm':<25}"
        f"{'Cost':<12}"
        f"{'Nodes':<12}"
        f"{'Success'}"
    )

    print("-" * 60)

    for name, result in results.items():

        if result["success"]:
            cost = result["total_cost"]
            nodes = result["nodes_expanded"]
            success = "Yes"

        else:
            cost = "-"
            nodes = result["nodes_expanded"]
            success = "No"

        print(
            f"{name:<25}"
            f"{str(cost):<12}"
            f"{str(nodes):<12}"
            f"{success}"
        )

    print("=" * 60)