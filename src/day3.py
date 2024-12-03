import re

def mul_sum(data: str) -> int:
    muls = re.findall(r"mul\(\d+,\d+\)", data)
    
    mul_sum = 0
    for mul in muls:
        x, y = mul.split("(")[1].split(")")[0].split(",")
        ints = (int(x), int(y))
        mul_sum += ints[0] * ints[1]

    return mul_sum

def solve() -> None:
    with open("data/3/data.txt", "r") as f:
        data = f.read().replace("\n", "")

    result = mul_sum(data)

    print(f"3A: {result}")

    # expr = r"(do\(\))(?!mul\(\d+,\d+\)|don't\(\)).+?(mul\(\d+,\d+\)+)(?!mul\(\d+,\d+\)|don't\(\)).+?(don't\(\))"
    expr = r"do\(\).+?(mul\(\d+,\d+\)+).+?don't\(\)"
    
    data = "do()" + data + "don't()"

    seqs = re.findall(expr, data)

    result = 0
    for seq in seqs:
        result += mul_sum(seq)

    print(f"3B: {result}")
