from typing import List, Set
from .models import Candidate, RankingConfig, RankingResult


def run_phase3(
    ranked: List[Candidate],
    config: RankingConfig,
) -> RankingResult:

    elected: List[Candidate] = []
    teams_with_representative: Set[str] = set()

    # --- Team Seat Allocation ---
    for candidate in ranked:
        if len(teams_with_representative) >= config.team_seat_count:
            break

        if candidate.elected:
            continue

        if candidate.team not in teams_with_representative:
            candidate.elected = True
            elected.append(candidate)
            teams_with_representative.add(candidate.team)

    # --- Vacancy Allocation ---
    remaining_seats = config.open_position_count - len(elected)

    if remaining_seats > 0:
        for candidate in ranked:
            if remaining_seats == 0:
                break

            if not candidate.elected:
                candidate.elected = True
                elected.append(candidate)
                remaining_seats -= 1

    # --- Alternates ---
    alternates = [c for c in ranked if not c.elected]

    return RankingResult(
        elected=elected,
        alternates=alternates,
        full_ranking=ranked,
    )