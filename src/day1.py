def get_lists() -> tuple[list[int], list[int]]:
    x = []
    y = []

    with open("data/1/data.txt", "r") as f:
        for line in f:
            line_parsed = line.replace("   ", " ").strip()

            parts = line_parsed.split(" ")

            x.append(int(parts[0]))
            y.append(int(parts[1]))

    return x, y


def solve():
    x, y = get_lists()

    x.sort()
    y.sort()

    distance = 0

    for i in range(len(x)):
        distance += abs(x[i] - y[i])

    print(f"1A: {distance}")

    y_dict = {}

    for n in y:
        if n not in y_dict:
            y_dict[n] = 1
        else:
            y_dict[n] += 1

    similarity = 0

    for n in x:
        if n not in y_dict:
            continue

        similarity += n * y_dict[n]

    print(f"1B: {similarity}")
