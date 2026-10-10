from config import (
    DEFAULT_BATTERY_CAPACITY,
    BATTERY_COST_PER_MOVE,
    CHARGING_TIME_PER_UNIT,
)


class Warehouse:
    def __init__(
        self,
        rows,
        cols,
        start,
        goal,
        blocked_cells=None,
        chargers=None,
        edge_costs=None,
        battery_capacity=DEFAULT_BATTERY_CAPACITY,
        initial_battery=None,
    ):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.blocked_cells = set(blocked_cells or [])
        self.chargers = set(chargers or [])
        self.edge_costs = edge_costs or {}
        self.battery_capacity = battery_capacity

        if initial_battery is None:
            initial_battery = battery_capacity

        if not 0 <= initial_battery <= battery_capacity:
            raise ValueError(
                "Initial battery must be between 0 and battery capacity."
            )

        self.initial_battery = initial_battery

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_blocked(self, row, col):
        return (row, col) in self.blocked_cells

    def is_charger(self, row, col):
        return (row, col) in self.chargers

    def valid_position(self, row, col):
        return self.in_bounds(row, col) and not self.is_blocked(row, col)

    def get_neighbors(self, row, col):
        directions = [
            (-1, 0),  # up
            (1, 0),   # down
            (0, -1),  # left
            (0, 1),   # right
        ]

        neighbors = []

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            if self.valid_position(new_row, new_col):
                neighbors.append((new_row, new_col))

        return neighbors

    def get_movement_time(self, current, neighbor):
        key = (current, neighbor)

        if key in self.edge_costs:
            return self.edge_costs[key]

        reverse_key = (neighbor, current)

        if reverse_key in self.edge_costs:
            return self.edge_costs[reverse_key]

        return 1

    def battery_after_move(self, battery):
        new_battery = battery - BATTERY_COST_PER_MOVE

        if new_battery < 0:
            return None

        return new_battery

    def charging_time(self, battery):
        return (
            self.battery_capacity - battery
        ) * CHARGING_TIME_PER_UNIT