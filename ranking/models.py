from dataclasses import dataclass, field
from typing import List


@dataclass
class Candidate:
    name: str
    team: str
    votes: int
    elected: bool = False

    def __post_init__(self) -> None:
        if self.votes < 0:
            raise ValueError("Vote count cannot be negative.")


@dataclass
class RankingConfig:
    team_seat_count: int
    open_position_count: int


@dataclass
class RankingResult:
    elected: List[Candidate] = field(default_factory=list)
    alternates: List[Candidate] = field(default_factory=list)
    full_ranking: List[Candidate] = field(default_factory=list)