def get_rules_and_updates() -> tuple[dict[int, int], list[list[int]]]:
    rules = {}
    updates = []
    
    with open("data/5/data.txt", "r") as f:
        for line in f:
            if "|" in line:
                parts = line.split("|")

                first = int(parts[0])
                second = int(parts[1])

                if first not in rules:
                    rules[first] = set()

                rules[first].add(second) 
            elif "," in line:
                updates.append([int(x) for x in line.split(",")])

    return rules, updates

def get_ordered_updates_idx(rules: dict[int, int], updates: list[list[int]]) -> list[int]:
    ordered_updates = []
        
    for i, update in enumerate(updates):
        #if i == 4:
        #    breakpoint()
        update_ordered = True
        for j, page in enumerate(update):
            if page not in rules:
                continue

            rule = rules[page]

            for k, otherpage in enumerate(update):
                if j == k:
                    continue
            
                if j >= k and otherpage in rule:
                    update_ordered = False
                    break
            
        if update_ordered:
            ordered_updates.append(i)

    return ordered_updates

def get_middle_sum(updates: list[list[int]], ordered_updates_idx: list[int]) -> int:
    middle_sum = 0

    for idx in ordered_updates_idx:
        ordered_update = updates[idx]

        middle_idx = len(ordered_update) // 2

        middle_sum += ordered_update[middle_idx]

    return middle_sum

def solve() -> None:
    rules, updates = get_rules_and_updates()

    ordered_updates_idx = get_ordered_updates_idx(rules, updates)

    n = get_middle_sum(updates, ordered_updates_idx)

    print(f"5A: {n}")
