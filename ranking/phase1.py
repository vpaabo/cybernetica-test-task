from typing import List, Tuple
from .models import Candidate

def run_phase1(candidates: List[Candidate]) -> Tuple[List[Candidate], List[Tuple[int, int]], List[Candidate]]:
    """
    Phase 1: Selection of qualifying candidates

    Returns:
        ranked_candidates: List[Candidate] with votes >= 1, sorted descending
        tie_groups: List of (start_index, end_index) among ranked_candidates with same votes
        zero_vote_candidates: List[Candidate] with 0 votes, sorted alphabetically
    """
    # Separate candidates
    positive = [c for c in candidates if c.votes > 0]
    zero_votes = [c for c in candidates if c.votes == 0]

    # Sort candidates
    positive.sort(key=lambda c: (-c.votes, c.name))
    zero_votes.sort(key=lambda c: c.name)

    # Identify tie groups among positive votes
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

    return positive, tie_groups, zero_votes