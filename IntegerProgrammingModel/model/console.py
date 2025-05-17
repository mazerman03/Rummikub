from helper import generate_all_sets, build_sij, build_ti, build_ri, build_wj, tile_id, JOKER_ID, visualize_rack, visualize_table,pretty_print_solution, visualize_post_move
from ilp import solve_rummikub_ilp
from collections import Counter

def main():
    sets = generate_all_sets()
    sij = build_sij(sets)

    # Tiles on the table
    table_tiles = [
        # Run of orange: 5, 6, 7
        tile_id('orange', 5), tile_id('orange', 6), tile_id('orange', 7),
        # Run of Red: 5, 6, 7
        tile_id('red', 5), tile_id('red', 6), tile_id('red', 7),
        # Run of Black: 5, 6, 7, 8, 9
        tile_id('black', 5), tile_id('black', 6), tile_id('black', 7), tile_id('black', 8), tile_id('black', 9)
    ]
    ti = build_ti(table_tiles)

    # Tiles on player's rack
    rack_tiles = [
        tile_id('red', 4),
        tile_id('black', 4),
        tile_id('black', 10),
        tile_id('blue', 5),
        tile_id('orange', 2),
        tile_id('red', 3),
        tile_id('red', 6),
        tile_id('orange', 12),
        tile_id('orange', 8),
        tile_id('blue', 6),
        tile_id('black', 9)
    ]
    ri = build_ri(rack_tiles)

    # Existing sets on table (auto-match based on tiles)
    table_sets = [
        s['id'] for s in sets if 
            set([tile_id('orange', 5), tile_id('orange', 6), tile_id('orange', 7)]).issubset(s['tiles']) or
            set([tile_id('red', 5), tile_id('red', 6), tile_id('red', 7)]).issubset(s['tiles']) or
            set([tile_id('black', 5), tile_id('black', 6), tile_id('black', 7), tile_id('black', 8), tile_id('black', 9)]).issubset(s['tiles'])
    ]
    wj = build_wj(sets, table_sets)

    # Tile values (1-13, joker=30)
    vi = {i: (i - 1) // 4 + 1 if i != JOKER_ID else 30 for i in range(1, 54)}

    # Before ILP:
    print("\n--- Initial State ---\n")
    visualize_rack(ri)
    visualize_table(ti)

    # Solve ILP
    result = solve_rummikub_ilp(sij, ti, ri, vi, wj)

    pretty_print_solution(result, sets)

    visualize_post_move(ti, ri, result['played_tiles'], result['formed_sets'], result['kept_sets'], sets)




if __name__ == "__main__":
    main()
