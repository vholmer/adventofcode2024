from enum import Enum
import time


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

    def dirpos(self) -> tuple[int, int, Direction]:
        return self.x, self.y, self.direction

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
    stones: list[tuple[int, int]]
    guard: Guard
    path: set[tuple[int, int]]
    dirpath: set[tuple[int, int, Direction]]

    def _initialize_map(self) -> None:
        with open("data/6/test2.txt", "r") as f:
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
        self.num_loops = 0
        self.path = set()
        self.loops = []
        self.dirpath = set()

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

    def wall_to_the_right(self) -> bool:
        right_dir_int = (int(self.guard.direction.value) + 1) % 4
        right_dir = Direction(right_dir_int)

        if right_dir == Direction.UP:
            for i in range(self.guard.y, -1, -1):
                if self._raw[i][self.guard.x].is_wall():
                    return True
        elif right_dir == Direction.RIGHT:
            for i in range(self.guard.x, self._size, 1):
                if self._raw[self.guard.y][i].is_wall():
                    return True
        elif right_dir == Direction.DOWN:
            for i in range(self.guard.y, self._size, 1):
                if self._raw[i][self.guard.x].is_wall():
                    return True
        elif right_dir == Direction.LEFT:
            for i in range(self.guard.x, -1, -1):
                if self._raw[self.guard.y][i].is_wall():
                    return True
        return False

    def move_guard_to_wall(self) -> None:
        if self.guard.direction == Direction.UP:
            for i in range(self.guard.y, -1, -1):
                if self._raw[i][self.guard.x].is_wall():
                    self.guard.y = i + 1
                    return
        elif self.guard.direction == Direction.RIGHT:
            for i in range(self.guard.x, self._size, 1):
                if self._raw[self.guard.y][i].is_wall():
                    self.guard.x = i - 1
                    return
        elif self.guard.direction == Direction.DOWN:
            for i in range(self.guard.y, self._size, 1):
                if self._raw[i][self.guard.x].is_wall():
                    self.guard.y = i - 1
                    return
        elif self.guard.direction == Direction.LEFT:
            for i in range(self.guard.x, -1, -1):
                if self._raw[self.guard.y][i].is_wall():
                    self.guard.x = i + 1
                    return

        # Just move guard out of bounds because no wall
        self.guard.x = -10
        self.guard.y = -10

    def find_next_stone(self, dirpos: tuple[int, int, Direction]) -> Tile:
        x, y, direction = dirpos

        if direction == Direction.UP:
            for i in range(y, -1, -1):
                if self._raw[i][x].is_wall():
                    return self._raw[i][x]
        elif direction == Direction.RIGHT:
            for i in range(x, self._size, 1):
                if self._raw[y][i].is_wall():
                    return self._raw[y][i]
        elif direction == Direction.DOWN:
            for i in range(y, self._size, 1):
                if self._raw[i][x].is_wall():
                    return self._raw[i][x]
        elif direction == Direction.LEFT:
            for i in range(x, -1, -1):
                if self._raw[y][i].is_wall():
                    return self._raw[y][i]

        return None

    def check_intersect(
        self, a: tuple[int, int, Direction], saved: tuple[int, int, Direction]
    ) -> bool:
        a_x = a[0]
        a_y = a[1]
        a_dir = a[2]

        saved_x = saved[0]
        saved_y = saved[1]
        saved_dir = saved[2]

        if a_dir != saved_dir:
            return False

        if a_dir == Direction.UP:
            s = self.find_next_stone(a)

            saved_above_a = saved_y <= a_y
            same_x = saved_x == a_x
            stone_between = a_y > s.y > saved_y if s else False

            return saved_above_a and same_x and not stone_between
        elif a_dir == Direction.RIGHT:
            s = self.find_next_stone(a)

            saved_right_of_a = saved_x >= a_x
            same_y = saved_y == a_y

            stone_between = a_x < s.x < saved_x if s else False

            return saved_right_of_a and same_y and not stone_between
        elif a_dir == Direction.DOWN:
            s = self.find_next_stone(a)

            saved_below_a = saved_y >= a_y
            same_x = saved_x == a_x
            stone_between = a_y < s.y < saved_y if s else False

            return saved_below_a and same_x and not stone_between
        elif a_dir == Direction.LEFT:
            s = self.find_next_stone(a)

            saved_left_of_a = saved_x <= a_x
            same_y = saved_y == a_y

            stone_between = a_x > s.x > saved_x if s else False

            return saved_left_of_a and same_y and not stone_between

        return False

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
                continue
            elif self.wall_to_the_right():
                # Simulate a wall here, and see if it leads to a loop!
                # Only do this if wall is on same row to the right as guard
                save_dirpos = self.guard.dirpos()

                stone_pos = self.guard.get_next()

                self.guard.turn()

                simulation_path = set()

                visited = self.guard.dirpos() in simulation_path

                while self.guard.dirpos() != save_dirpos and self.guard_inside():
                    x, y = self.guard.get_next()

                    x = max(0, x)
                    x = min(x, self._size - 1)

                    y = max(0, y)
                    y = min(y, self._size - 1)

                    if self._raw[y][x].is_wall():
                        self.guard.turn()

                    visited = self.guard.dirpos() in simulation_path

                    # Check if we WILL hit save_dirpos, not if current
                    # dirpos is equal to save_dirpos as with regular move
                    if self.check_intersect(self.guard.dirpos(), save_dirpos):
                        self.num_loops += 1
                        self.loops.append((stone_pos, simulation_path))
                        break

                    if not visited:
                        simulation_path.add(self.guard.dirpos())
                    else:
                        break

                    self.move_guard_to_wall()

                self.guard.x = save_dirpos[0]
                self.guard.y = save_dirpos[1]
                self.guard.direction = save_dirpos[2]

            # Add guard pos to set and move
            self.path.add(self.guard.pos())
            self.dirpath.add(self.guard.dirpos())

            self.guard.move()


def solve() -> None:
    world = World()

    world.walk()

    print(f"6A: {len(world.path)}")
    print(f"6B: {world.num_loops}")
