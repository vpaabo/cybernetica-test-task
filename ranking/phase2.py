from typing import List, Tuple
from .models import Candidate


def resolve_draws(
    ranked: List[Candidate],
    tie_groups: List[Tuple[int, int]],
    reordered_indices: List[List[int]],
) -> List[Candidate]:
    """
    reordered_indices:
        A list matching tie_groups.
        Each element is a list of relative indices indicating new order.
    """

    if len(tie_groups) != len(reordered_indices):
        raise ValueError("Mismatch between tie groups and reorder instructions.")

    for (group_idx, (start, end)) in enumerate(tie_groups):
        group = ranked[start:end + 1]
        order = reordered_indices[group_idx]

        if sorted(order) != list(range(len(group))):
            raise ValueError("Invalid reordering indices.")

        reordered_group = [group[i] for i in order]
        ranked[start:end + 1] = reordered_group

    return ranked