from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    row: int
    col: int
    battery: int

    @property
    def position(self):
        return self.row, self.col
