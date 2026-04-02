from typing import List, Tuple
from .models import Candidate, RankingConfig


def parse_input_file(path: str) -> Tuple[RankingConfig, List[Candidate]]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    if not lines:
        raise ValueError("Input file is empty.")

    # Parse header
    header_parts = lines[0].split("\t")
    if len(header_parts) != 2:
        raise ValueError("Header must contain exactly two TAB-separated values.")

    try:
        team_count = int(header_parts[0])
        open_positions = int(header_parts[1])
    except ValueError:
        raise ValueError("Header values must be integers.")

    config = RankingConfig(
        team_seat_count=team_count,
        open_position_count=open_positions,
    )

    # Parse candidates
    candidates: List[Candidate] = []

    for line in lines[1:]:
        if not line.strip():
            continue

        parts = line.split("\t")
        if len(parts) != 3:
            raise ValueError(f"Invalid candidate line: {line}")

        name, team, vote_str = parts

        try:
            votes = int(vote_str)
        except ValueError:
            raise ValueError(f"Invalid vote count for candidate {name}")

        candidates.append(Candidate(name=name, team=team, votes=votes))

    return config, candidates