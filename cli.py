import argparse
import sys
from typing import List

from ranking.engine import RankingEngine


def print_phase1_state(ranked, tie_groups, zero_votes):
    print("\n=== PHASE 1: INITIAL RANKING ===\n")

    # Print candidates with votes first
    for idx, candidate in enumerate(ranked, start=1):
        print(f"{idx}. {candidate.name} ({candidate.team}) - {candidate.votes} votes")

    print("------- (0 votes) -------")

    # Print zero-vote candidates alphabetically (already sorted)
    for idx, candidate in enumerate(zero_votes):
        print(f"{candidate.name} ({candidate.team}) - {candidate.votes} votes")


def collect_draw_resolutions(engine: RankingEngine) -> List[List[int]]:
    reordered_indices = []

    for group_number, (start, end) in enumerate(engine.tie_groups, start=1):
        group = engine.ranked[start:end + 1]

        print(f"\n== RESOLVING DRAW {group_number} ==")
        for i, candidate in enumerate(group):
            print(f"{i}. {candidate.name} ({candidate.team}) - {candidate.votes} votes")

        while True:
            try:
                raw_input_order = input(
                    "Enter new order as space-separated indices (e.g. '1 0'): "
                )
                parts = raw_input_order.strip().split()
                order = [int(p) for p in parts]

                if sorted(order) != list(range(len(group))):
                    raise ValueError

                reordered_indices.append(order)
                break

            except ValueError:
                print("Invalid input. Please enter a valid permutation of indices.")

    return reordered_indices


def main():
    parser = argparse.ArgumentParser(
        description="Ranking application based on voting results."
    )
    parser.add_argument(
        "input_file",
        help="Path to input file containing ranking data.",
    )

    args = parser.parse_args()

    try:
        engine = RankingEngine(args.input_file)

        # Phase 1
        engine.phase1()
        print_phase1_state(engine.ranked, engine.tie_groups, engine.zero_votes)

        # Phase 2 (if necessary)
        
        if engine.tie_groups:
            print("\n=== PHASE 2: RESOLVE DRAWS ===\n")
            reordered_indices = collect_draw_resolutions(engine)
            engine.phase2(reordered_indices)
            
            for idx, candidate in enumerate(engine.ranked, start=1):
                print(f"{idx}. {candidate.name} ({candidate.team}) - {candidate.votes} votes")

        # Phase 3
        result = engine.phase3()

        # Phase 4
        final_output = engine.phase4(result)

        print("\n=== FINAL RESULTS ===\n")
        print(final_output)

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()