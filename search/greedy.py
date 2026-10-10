import heapq
from itertools import count

from warehouse.state import State
from search.heuristics import primary_heuristic


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


def greedy_best_first_search(warehouse):
    """
    Battery-aware Greedy Best-First Search.

    Priority:
        h(n)

    Greedy chooses the state estimated to be closest
    to the goal, without considering accumulated path cost.
    """

    start_state = State(
        row=warehouse.start[0],
        col=warehouse.start[1],
        battery=warehouse.initial_battery,
    )

    frontier = []
    tie_breaker = count()

    start_h = primary_heuristic(
        start_state,
        warehouse,
    )

    heapq.heappush(
        frontier,
        (
            start_h,
            next(tie_breaker),
            start_state,
        ),
    )

    visited = set()

    parent = {
        start_state: None
    }

    action_taken = {}

    path_cost = {
        start_state: 0
    }

    nodes_expanded = 0

    while frontier:
        _, _, current_state = heapq.heappop(frontier)

        if current_state in visited:
            continue

        visited.add(current_state)
        nodes_expanded += 1

        current_cost = path_cost[current_state]

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

                if next_state in visited:
                    continue

                movement_time = warehouse.get_movement_time(
                    current_state.position,
                    neighbor,
                )

                new_cost = current_cost + movement_time

                if (
                    next_state not in path_cost
                    or new_cost < path_cost[next_state]
                ):
                    path_cost[next_state] = new_cost
                    parent[next_state] = current_state

                    action_taken[next_state] = (
                        f"Move {current_state.position} -> {neighbor} "
                        f"(time={movement_time}, battery={new_battery})"
                    )

                    heuristic_value = primary_heuristic(
                        next_state,
                        warehouse,
                    )

                    heapq.heappush(
                        frontier,
                        (
                            heuristic_value,
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

            if recharged_state not in visited:
                if (
                    recharged_state not in path_cost
                    or new_cost < path_cost[recharged_state]
                ):
                    path_cost[recharged_state] = new_cost
                    parent[recharged_state] = current_state

                    action_taken[recharged_state] = (
                        f"Recharge at {current_state.position} "
                        f"(time={recharge_cost}, "
                        f"battery={warehouse.battery_capacity})"
                    )

                    heuristic_value = primary_heuristic(
                        recharged_state,
                        warehouse,
                    )

                    heapq.heappush(
                        frontier,
                        (
                            heuristic_value,
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