from typing import List, Tuple
from .models import Candidate


def run_phase1(candidates: List[Candidate]) -> Tuple[List[Candidate], List[Tuple[int, int]]]:
    """
    Returns:
        ranked_candidates
        tie_groups as list of (start_index, end_index) inclusive
    """

    positive = [c for c in candidates if c.votes > 0]
    zero_votes = [c for c in candidates if c.votes == 0]

    # Sort positive votes descending, stable by name
    positive.sort(key=lambda c: (-c.votes, c.name))
    zero_votes.sort(key=lambda c: c.name)

    ranked = positive + zero_votes

    # Identify tie groups (only among positive votes)
    tie_groups: List[Tuple[int, int]] = []
    i = 0
    while i < len(positive):
        start = i
        while i + 1 < len(positive) and positive[i].votes == positive[i + 1].votes:
            i += 1
        end = i
        if end > start:
            tie_groups.append((start, end))
        i += 1

    return ranked, tie_groups