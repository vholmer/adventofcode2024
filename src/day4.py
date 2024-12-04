xmas = "XMAS"
mas = "MAS"


def get_matrix(part_two=False) -> list[str]:
    result = []

    with open("data/4/test.txt", "r") as f:
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


def solve() -> None:
    m = get_matrix()
    dots = [["." for _ in range(len(m))] for _ in range(len(m))]

    n, dots = count_token(m, dots)

    print(f"4A: {n}")

    m = get_matrix(part_two=True)
    dots = [["." for _ in range(len(m))] for _ in range(len(m))]

    n, dots = count_token(m, dots, part_two=True, token=mas)

    print(n)

    for line in dots:
        print("".join(line))
