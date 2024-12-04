import re, time


def mul_sum(data: str) -> int:
    muls = re.findall(r"mul\(\d+,\d+\)", data)

    mul_sum = 0
    for mul in muls:
        x, y = mul.split("(")[1].split(")")[0].split(",")
        ints = (int(x), int(y))
        mul_sum += ints[0] * ints[1]

    return mul_sum


def parse_do_statements(data: str, verbose=False) -> list[str]:
    read_data = ""
    print_data = ""
    do_statement = ""
    result = []

    in_do = False

    for i, char in enumerate(data):
        read_data += char

        if in_do:
            do_statement += char

        if verbose:
            middle = len(read_data) - 1 // 2
            offset = 100
            lower = max(middle - offset, 0)
            upper = min(middle + offset, len(read_data) - 1)
            print_data = read_data[lower:upper]

        if verbose:
            print(f"Read: {print_data}")
            time.sleep(0.01)

        if len(read_data) >= 4 and read_data[-4:] == "do()":
            if verbose:
                print("In do: True")
            in_do = True
        elif len(read_data) >= 7 and read_data[-7:] == "don't()":
            do_statement = do_statement.replace("don't()", "")

            if verbose:
                print(f"Appending {do_statement} to result")
                print("In do: False")

            result.append(do_statement)

            in_do = False
            do_statement = ""

    return result


def solve() -> None:
    with open("data/3/data.txt", "r") as f:
        data = f.read().replace("\n", "")

    result = mul_sum(data)

    print(f"3A: {result}")

    data = "do()" + data + "don't()"

    parsed_dos = parse_do_statements(data)

    result = 0
    for do in parsed_dos:
        result += mul_sum(do)

    print(f"3B: {result}")
