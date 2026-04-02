from typing import List, Set
from .models import Candidate, RankingConfig, RankingResult


def run_phase3(
    ranked: List[Candidate],
    config: RankingConfig,
) -> RankingResult:

    elected: List[Candidate] = []
    teams_with_representative: Set[str] = set()
    alternates: List[Candidate] = []

    # --- Team Seat Allocation ---
    for candidate in ranked:
        if len(teams_with_representative) >= config.team_seat_count:
            break
        
        if candidate.votes == 0:
            continue

        if candidate.team not in teams_with_representative:
            candidate.status = "ELECTED"
            elected.append(candidate)
            teams_with_representative.add(candidate.team)

    # --- Vacancy Allocation ---
    remaining_seats = config.open_position_count - len(elected)

    if remaining_seats > 0:
        for candidate in ranked:
            if remaining_seats == 0:
                break
            
            if candidate.votes == 0:
                continue

            if candidate.status == "":
                candidate.status = "ELECTED"
                elected.append(candidate)
                remaining_seats -= 1

    # --- Alternates ---
    for c in ranked:
        if c.status == "":
            c.status = "ALTERNATE"
            alternates.append(c)

    return RankingResult(
        elected=elected,
        alternates=alternates,
        full_ranking=ranked,
    )