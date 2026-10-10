from maps.test_maps import small_test_map
from warehouse.state import State


def main():
    warehouse = small_test_map()

    start_state = State(
        row=warehouse.start[0],
        col=warehouse.start[1],
        battery=warehouse.battery_capacity,
    )

    print("Battery-Aware Warehouse Robot")
    print("-----------------------------")
    print("Grid size:", warehouse.rows, "x", warehouse.cols)
    print("Start:", warehouse.start)
    print("Goal:", warehouse.goal)
    print("Battery capacity:", warehouse.battery_capacity)
    print("Chargers:", warehouse.chargers)
    print("Blocked cells:", warehouse.blocked_cells)

    print("\nInitial state:")
    print(start_state)

    print("\nValid neighbors from start:")
    for neighbor in warehouse.get_neighbors(
        start_state.row,
        start_state.col,
    ):
        movement_time = warehouse.get_movement_time(
            start_state.position,
            neighbor,
        )

        print(
            neighbor,
            "- movement time:",
            movement_time,
        )


if __name__ == "__main__":
    main()