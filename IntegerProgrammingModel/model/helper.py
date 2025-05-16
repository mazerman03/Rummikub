from itertools import combinations
from collections import defaultdict
COLORS = ['red', 'blue', 'black', 'orange']
NUMBERS = list(range(1, 14))
JOKER_ID = 53

def tile_id(color, number):
    return (number - 1) * 4 + COLORS.index(color) + 1

def generate_all_sets():
    sets = []
    sid = 1

    # Groups of 3 and 4 tiles
    for num in NUMBERS:
        # Groups of 3 colors (no joker)
        for colors in combinations(COLORS, 3):
            sets.append({'id': sid, 'tiles': [tile_id(c, num) for c in colors], 'jokers': 0})
            sid += 1

        # Groups of 3 with 1 joker
        for colors in combinations(COLORS, 2):
            sets.append({'id': sid, 'tiles': [tile_id(c, num) for c in colors] + [JOKER_ID], 'jokers': 1})
            sid += 1

        # Groups of 4 colors (no joker)
        sets.append({'id': sid, 'tiles': [tile_id(c, num) for c in COLORS], 'jokers': 0})
        sid += 1

        # Groups of 4 with 1 joker
        for colors in combinations(COLORS, 3):
            sets.append({'id': sid, 'tiles': [tile_id(c, num) for c in colors] + [JOKER_ID], 'jokers': 1})
            sid += 1

        # Groups of 4 with 2 jokers
        for colors in combinations(COLORS, 2):
            sets.append({'id': sid, 'tiles': [tile_id(c, num) for c in colors] + [JOKER_ID, JOKER_ID], 'jokers': 2})
            sid += 1

    # Runs: Deduplicated by unique key
    dedup_keys = set()
    for color in COLORS:
        for length in [3, 4, 5]:
            
            for start in range(1, 14 - length + 1): 
                base_numbers = list(range(start, start + length))
                base_tiles = [tile_id(color, n) for n in base_numbers]

                # Run without jokers
                key = (color, tuple(base_numbers), 0)
                if key not in dedup_keys:
                    sets.append({'id': sid, 'tiles': base_tiles, 'jokers': 0})
                    dedup_keys.add(key)
                    sid += 1

                # Runs with 1 joker (unique substitution)
                for missing in combinations(base_numbers, 1):
                    present = sorted([n for n in base_numbers if n not in missing])
                    key = (color, tuple(present), 1)
                    if key not in dedup_keys:
                        tiles = [tile_id(color, n) for n in present] + [JOKER_ID]
                        sets.append({'id': sid, 'tiles': tiles, 'jokers': 1})
                        dedup_keys.add(key)
                        sid += 1

                # Runs with 2 jokers (unique substitution)
                for missing in combinations(base_numbers, 2):
                    present = sorted([n for n in base_numbers if n not in missing])
                    key = (color, tuple(present), 2)
                    if key not in dedup_keys:
                        tiles = [tile_id(color, n) for n in present] + [JOKER_ID, JOKER_ID]
                        sets.append({'id': sid, 'tiles': tiles, 'jokers': 2})
                        dedup_keys.add(key)
                        sid += 1

    return sets


def build_sij(sets):
    sij = {}
    for s in sets:
        for i in s['tiles']:
            sij[(i, s['id'])] = 1
    return sij

def build_ti(table_tiles):
    ti = {i: 0 for i in range(1, 54)}
    for tid in table_tiles:
        ti[tid] += 1
    return ti

def build_ri(rack_tiles):
    ri = {i: 0 for i in range(1, 54)}
    for tid in rack_tiles:
        ri[tid] += 1
    return ri

def build_wj(sets, current_table_sets):
    wj = {s['id']: 0 for s in sets}
    for sid in current_table_sets:
        wj[sid] = 1
    return wj


def tile_id_to_description(tile_id):
    if tile_id == JOKER_ID:
        return "JOKER"
    number = (tile_id - 1) // 4 + 1
    color = COLORS[(tile_id - 1) % 4]
    return f"{color} {number}"

def describe_set(set_obj):
    return [tile_id_to_description(tid) for tid in set_obj['tiles']]


def visualize_rack(ri):
    print("Player's Rack:")
    rack_tiles = []
    for tid, count in ri.items():
        rack_tiles.extend([tile_id_to_description(tid)] * int(count))
    print(' '.join(rack_tiles) if rack_tiles else "(empty)")
    print()

def visualize_table(ti):
    print("Table Tiles:")
    table_tiles = []
    for tid, count in ti.items():
        table_tiles.extend([tile_id_to_description(tid)] * int(count))
    print(' '.join(table_tiles) if table_tiles else "(empty)")
    print()

def pretty_print_solution(result, sets):
    print(f"Status: {result['status']}")
    print(f"Tiles placed: {result['objective_value']}\n")

    print("Tiles Played (from rack):")
    for tid in result['played_tiles']:
        print(f" - {tile_id_to_description(tid)}")

    print("\nFormed Sets:")
    for s in sets:
        if s['id'] in result['formed_sets']:
            tiles = describe_set(s)
            print(f" - Set {s['id']}: {tiles}")

    print("\nKept Sets (unchanged):")
    for s in sets:
        if s['id'] in result['kept_sets']:
            tiles = describe_set(s)
            print(f" - Set {s['id']}: {tiles}")

def visualize_post_move(ti, ri, played_tiles, formed_sets, kept_sets, sets):
    print("\n--- After ILP Move ---\n")

    print("Table after move (formed + kept sets):")
    for s in sets:
        if s['id'] in formed_sets or s['id'] in kept_sets:
            tiles = describe_set(s)
            print(f" Set {s['id']}: {' '.join(tiles)}")
    print()

    print("Player's rack after move:")
    remaining_ri = {tid: ri.get(tid, 0) - played_tiles.get(tid, 0) for tid in ri}
    remaining_tiles = []
    for tid, count in remaining_ri.items():
        if count > 0:
            remaining_tiles.extend([tile_id_to_description(tid)] * int(count))
    print(' '.join(remaining_tiles) if remaining_tiles else "(empty)")
    print()