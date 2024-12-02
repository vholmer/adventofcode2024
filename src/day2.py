def get_matrix() -> list[list[int]]:
    matrix = []

    with open("data/2/data.txt") as f:
        for line in f:
            ints = [int(x) for x in line.strip().split(" ")]
            matrix.append(ints)

    return matrix


def is_row_safe(row: list[int]) -> int:
    is_safe = row == sorted(row) or row == sorted(row, reverse=True)

    if not is_safe:
        return 0

    for i in range(len(row) - 1):
        cur = row[i]
        nex = row[i + 1]

        dist = abs(cur - nex)

        if dist < 1 or dist > 3:
            return 0

    return 1


def solve():
    m = get_matrix()

    num_safe = 0

    for row in m:
        num_safe += is_row_safe(row)

    print(f"2A: {num_safe}")

    m = get_matrix()

    num_safe = 0

    for row in m:
        # First check row regularly
        is_safe = bool(is_row_safe(row))

        # Then, attempt to remove each element one by one
        for i in range(len(row)):
            new_row = row[:i] + row[i + 1 :]

            is_safe = is_safe or bool(is_row_safe(new_row))

        if is_safe:
            num_safe += 1

    print(f"2B: {num_safe}")
