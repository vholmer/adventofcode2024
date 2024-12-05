xmas = "XMAS"
mas = "MAS"


def get_matrix(part_two=False) -> list[str]:
    result = []

    with open("data/4/data.txt", "r") as f:
        for line in f:
            if part_two:
                result.append(line.replace("X", "."))
            else:
                result.append(line)

    return result


def within_bounds(m: list[str], pos_yx: tuple[int, int]) -> tuple[int, int]:
    y, x = pos_yx

    if x < 0 or x >= len(m):
        return False

    if y < 0 or y >= len(m):
        return False

    return True


def mark(
    dots: list[str],
    m: list[str],
    origin_yx: tuple[int, int],
    direction_yx: tuple[int, int],
    token=xmas,
) -> bool:
    cur_pos = origin_yx

    path = []

    for i in range(len(token)):
        if not within_bounds(m, cur_pos):
            return dots

        if m[cur_pos[0]][cur_pos[1]] == token[i]:
            path.append(cur_pos)
            cur_pos = (cur_pos[0] + direction_yx[0], cur_pos[1] + direction_yx[1])
        else:
            return dots

    for i, yx in enumerate(path):
        y, x = yx

        dots[y][x] = token[i]

    return dots


def check(
    m: list[str], origin_yx: tuple[int, int], direction_yx: tuple[int, int], token=xmas
) -> bool:
    cur_pos = origin_yx

    for i in range(len(token)):
        if not within_bounds(m, cur_pos):
            return False

        if m[cur_pos[0]][cur_pos[1]] == token[i]:
            cur_pos = (cur_pos[0] + direction_yx[0], cur_pos[1] + direction_yx[1])
        else:
            return False
    return True


def count_token(
    m: list[str], dots: list[str], part_two=False, token=xmas
) -> tuple[int, list[str]]:
    num = 0
    for y, row in enumerate(m):
        for x, col in enumerate(row):
            if col != token[0]:
                continue
            else:
                # up left
                num += int(
                    check(m=m, origin_yx=(y, x), direction_yx=(-1, -1), token=token)
                )
                dots = mark(
                    dots=dots, m=m, origin_yx=(y, x), direction_yx=(-1, -1), token=token
                )
                # up right
                num += int(
                    check(m=m, origin_yx=(y, x), direction_yx=(-1, 1), token=token)
                )
                dots = mark(
                    dots=dots, m=m, origin_yx=(y, x), direction_yx=(-1, 1), token=token
                )
                # down left
                num += int(
                    check(m=m, origin_yx=(y, x), direction_yx=(1, -1), token=token)
                )
                dots = mark(
                    dots=dots, m=m, origin_yx=(y, x), direction_yx=(1, -1), token=token
                )
                # down right
                num += int(
                    check(m=m, origin_yx=(y, x), direction_yx=(1, 1), token=token)
                )
                dots = mark(
                    dots=dots, m=m, origin_yx=(y, x), direction_yx=(1, 1), token=token
                )

                if not part_two:
                    # up
                    num += int(
                        check(m=m, origin_yx=(y, x), direction_yx=(-1, 0), token=token)
                    )
                    dots = mark(
                        dots=dots,
                        m=m,
                        origin_yx=(y, x),
                        direction_yx=(-1, 0),
                        token=token,
                    )
                    # down
                    num += int(
                        check(m=m, origin_yx=(y, x), direction_yx=(1, 0), token=token)
                    )
                    dots = mark(
                        dots=dots,
                        m=m,
                        origin_yx=(y, x),
                        direction_yx=(1, 0),
                        token=token,
                    )
                    # left
                    num += int(
                        check(m=m, origin_yx=(y, x), direction_yx=(0, -1), token=token)
                    )
                    dots = mark(
                        dots=dots,
                        m=m,
                        origin_yx=(y, x),
                        direction_yx=(0, -1),
                        token=token,
                    )
                    # right
                    num += int(
                        check(m=m, origin_yx=(y, x), direction_yx=(0, 1), token=token)
                    )
                    dots = mark(
                        dots=dots,
                        m=m,
                        origin_yx=(y, x),
                        direction_yx=(0, 1),
                        token=token,
                    )

    return num, dots


def has_ms_diag(m: list[str], a_pos: tuple[int, int]) -> bool:
    """Check 2M + 2S in diag positions, return True if correct."""
    num_m = 0
    num_s = 0

    def count_ms(m: list[str], check_pos: tuple[int, int]) -> tuple[int, int]:
        check_y, check_x = check_pos

        num_m = 0
        num_s = 0

        if within_bounds(m, check_pos):
            if m[check_y][check_x] == "M":
                num_m += 1
            elif m[check_y][check_x] == "S":
                num_s += 1

        return num_m, num_s

    # top left
    check_offset = (-1, -1)
    check_pos = (a_pos[0] + check_offset[0], a_pos[1] + check_offset[1])
    ms = count_ms(m, check_pos)
    num_m += ms[0]
    num_s += ms[1]

    # top right
    check_offset = (-1, 1)
    check_pos = (a_pos[0] + check_offset[0], a_pos[1] + check_offset[1])
    ms = count_ms(m, check_pos)
    num_m += ms[0]
    num_s += ms[1]

    # bottom left
    check_offset = (1, -1)
    check_pos = (a_pos[0] + check_offset[0], a_pos[1] + check_offset[1])
    ms = count_ms(m, check_pos)
    num_m += ms[0]
    num_s += ms[1]

    # bottom right
    check_offset = (1, 1)
    check_pos = (a_pos[0] + check_offset[0], a_pos[1] + check_offset[1])
    ms = count_ms(m, check_pos)
    num_m += ms[0]
    num_s += ms[1]

    return num_m == 2 and num_s == 2


def has_same_neighbor(m: list[str], a_pos: tuple[int, int]) -> bool:
    a_y, a_x = a_pos
    top_left = m[a_y - 1][a_x - 1]
    top_right = m[a_y - 1][a_x + 1]
    bottom_left = m[a_y + 1][a_x - 1]

    return (top_left == top_right) or (top_left == bottom_left)


def count_mas(m: list[str]) -> int:
    n = 0

    for y, row in enumerate(m):
        for x, col in enumerate(row):
            if m[y][x] != "A":
                continue
            else:
                # Check presence of 2 M and 2 S in diag positions
                # Check adjacent same from top left
                a_pos = (y, x)
                n += int(has_ms_diag(m, a_pos) and has_same_neighbor(m, a_pos))

    return n


def solve() -> None:
    m = get_matrix()
    dots = [["." for _ in range(len(m))] for _ in range(len(m))]

    n, dots = count_token(m, dots)

    print(f"4A: {n}")

    m = get_matrix(part_two=True)

    n = count_mas(m)

    print(f"4B: {n}")
