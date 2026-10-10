import heapq
from itertools import count

from warehouse.state import State


def reconstruct_path(parent, action_taken, goal_state):
    path = []
    actions = []

    current = goal_state

    while current is not None:
        path.append(current)

        if current in action_taken:
            actions.append(action_taken[current])

        current = parent.get(current)

    path.reverse()
    actions.reverse()

    return path, actions


def uniform_cost_search(warehouse):
    start_state = State(
        row=warehouse.start[0],
        col=warehouse.start[1],
        battery=warehouse.initial_battery,
    )

    frontier = []
    tie_breaker = count()

    heapq.heappush(
        frontier,
        (0, next(tie_breaker), start_state),
    )

    best_cost = {
        start_state: 0
    }

    parent = {
        start_state: None
    }

    action_taken = {}

    nodes_expanded = 0

    while frontier:
        current_cost, _, current_state = heapq.heappop(frontier)

        if current_cost != best_cost.get(current_state):
            continue

        nodes_expanded += 1

        if current_state.position == warehouse.goal:
            path, actions = reconstruct_path(
                parent,
                action_taken,
                current_state,
            )

            return {
                "success": True,
                "path": path,
                "actions": actions,
                "total_cost": current_cost,
                "nodes_expanded": nodes_expanded,
            }

        # Move actions
        if current_state.battery > 0:
            neighbors = warehouse.get_neighbors(
                current_state.row,
                current_state.col,
            )

            for neighbor in neighbors:
                new_battery = warehouse.battery_after_move(
                    current_state.battery
                )

                if new_battery is None:
                    continue

                next_state = State(
                    row=neighbor[0],
                    col=neighbor[1],
                    battery=new_battery,
                )

                movement_time = warehouse.get_movement_time(
                    current_state.position,
                    neighbor,
                )

                new_cost = current_cost + movement_time

                if new_cost < best_cost.get(next_state, float("inf")):
                    best_cost[next_state] = new_cost
                    parent[next_state] = current_state

                    action_taken[next_state] = (
                        f"Move {current_state.position} -> {neighbor} "
                        f"(time={movement_time}, battery={new_battery})"
                    )

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            next(tie_breaker),
                            next_state,
                        ),
                    )

        # Recharge action
        if (
            warehouse.is_charger(
                current_state.row,
                current_state.col,
            )
            and current_state.battery < warehouse.battery_capacity
        ):
            recharge_cost = warehouse.charging_time(
                current_state.battery
            )

            recharged_state = State(
                row=current_state.row,
                col=current_state.col,
                battery=warehouse.battery_capacity,
            )

            new_cost = current_cost + recharge_cost

            if new_cost < best_cost.get(
                recharged_state,
                float("inf"),
            ):
                best_cost[recharged_state] = new_cost
                parent[recharged_state] = current_state

                action_taken[recharged_state] = (
                    f"Recharge at {current_state.position} "
                    f"(time={recharge_cost}, "
                    f"battery={warehouse.battery_capacity})"
                )

                heapq.heappush(
                    frontier,
                    (
                        new_cost,
                        next(tie_breaker),
                        recharged_state,
                    ),
                )

    return {
        "success": False,
        "path": [],
        "actions": [],
        "total_cost": None,
        "nodes_expanded": nodes_expanded,
    }