from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Guard:
    x: int
    y: int
    direction: Direction

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = Direction.UP

    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    def char(self) -> str:
        if self.direction == Direction.UP:
            return "^"
        elif self.direction == Direction.DOWN:
            return "v"
        elif self.direction == Direction.RIGHT:
            return ">"
        elif self.direction == Direction.LEFT:
            return "<"

    def turn(self) -> None:
        new_direction = (int(self.direction.value) + 1) % 4

        self.direction = Direction(new_direction)

    def move(self) -> None:
        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1

    def get_next(self) -> tuple[int, int]:
        """Get next position on move"""
        if self.direction == Direction.UP:
            return self.x, self.y - 1
        elif self.direction == Direction.DOWN:
            return self.x, self.y + 1
        elif self.direction == Direction.RIGHT:
            return self.x + 1, self.y
        elif self.direction == Direction.LEFT:
            return self.x - 1, self.y


class Tile:
    char: str
    x: int
    y: int

    def __init__(self, char, x, y):
        if char == "^":
            char = "."
        self.char = char
        self.x = x
        self.y = y

    def is_wall(self) -> bool:
        return self.char == "#"


class World:
    _raw: list[list[Tile]]
    _size: int
    guard: Guard
    path: set[tuple[int, int]]

    def _initialize_map(self) -> None:
        with open("data/6/data.txt", "r") as f:
            for y, line in enumerate(f):
                row = []
                for x, char in enumerate(line):
                    if char == "\n":
                        continue
                    row.append(Tile(char, x, y))

                    if char == "^":
                        self.guard = Guard(x, y)
                self._size = len(row)
                self._raw.append(row)

    def __init__(self):
        self._raw = []
        self.path = set()

        self._initialize_map()

    def __str__(self) -> str:
        result = []
        for i in range(self._size):
            result += ["".join([tile.char for tile in self._raw[i]])]

        if self.guard_inside():
            g = result[self.guard.y]
            result[self.guard.y] = (
                g[: self.guard.x] + self.guard.char() + g[self.guard.x + 1 :]
            )

        return "\n".join(result)

    def guard_inside(self) -> bool:
        g = self.guard
        return g.x >= 0 and g.x < self._size and g.y >= 0 and g.y < self._size

    def walk(self) -> None:
        while self.guard_inside():
            # print(self)
            # print("-" * self._size)
            # Check if next is collision, if yes, turn
            x, y = self.guard.get_next()

            # Clip in case next is out of bounds
            x = max(0, x)
            x = min(x, self._size - 1)

            y = max(0, y)
            y = min(y, self._size - 1)

            if self._raw[y][x].is_wall():
                self.guard.turn()

            # Add guard pos to set and move
            self.path.add(self.guard.pos())
            self.guard.move()


def solve() -> None:
    world = World()

    world.walk()

    print(f"6A: {len(world.path)}")
