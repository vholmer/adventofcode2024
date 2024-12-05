def get_rules_and_updates() -> tuple[dict[int, set[int]], list[list[int]]]:
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

def get_updates_idx(rules: dict[int, int], updates: list[list[int]], return_ordered: bool = True) -> list[int]:
    ordered_updates = []
    unordered_updates = []
        
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
        else:
            unordered_updates.append(i)

    if return_ordered:
        return ordered_updates
    else:
        return unordered_updates

def get_middle_sum_idx(updates: list[list[int]], ordered_updates_idx: list[int]) -> int:
    middle_sum = 0

    for idx in ordered_updates_idx:
        ordered_update = updates[idx]

        middle_idx = len(ordered_update) // 2

        middle_sum += ordered_update[middle_idx]

    return middle_sum

def get_middle_sum(updates: list[list[int]]) -> int:
    middle_sum = 0

    for i in range(len(updates)):
        update = updates[i]

        middle_idx = len(update) // 2

        middle_sum += update[middle_idx]

    return middle_sum

def sort_update(update: list[int], rules: dict[int, set[int]]) -> list[int]:
    sorted_update = []
    offset = -1000
    for page in update:
        if page not in rules:
            sorted_update.append((offset, page))
            continue

        rule = rules[page]

        n = sum([1 for otherpage in update if page != otherpage and otherpage in rule])

        sorted_update.append((n, page))

    sorted_update.sort(key = lambda x: x[0], reverse = True)

    return [x[1] for x in sorted_update]

def solve() -> None:
    rules, updates = get_rules_and_updates()

    ordered_updates_idx = get_updates_idx(rules, updates)

    n = get_middle_sum_idx(updates, ordered_updates_idx)

    print(f"5A: {n}")

    unordered_updates_idx = get_updates_idx(rules, updates, return_ordered = False)

    fixed_updates = []
    for idx in unordered_updates_idx:
        fixed_updates.append(sort_update(updates[idx], rules))

    n = get_middle_sum(fixed_updates)

    print(f"5B: {n}")
