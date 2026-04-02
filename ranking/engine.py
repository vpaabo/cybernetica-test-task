from typing import List
from .models import RankingResult
from .parser import parse_input_file
from .phase1 import run_phase1
from .phase2 import resolve_draws
from .phase3 import run_phase3
from .phase4 import format_results


class RankingEngine:
    def __init__(self, input_path: str):
        self.config, self.candidates = parse_input_file(input_path)
        self.ranked = []
        self.zero_votes = []
        self.tie_groups = []

    def phase1(self) -> None:
        self.ranked, self.tie_groups, self.zero_votes = run_phase1(self.candidates)

    def phase2(self, reordered_indices: List[List[int]]) -> None:
        self.ranked = resolve_draws(
            self.ranked,
            self.tie_groups,
            reordered_indices,
        )

    def phase3(self) -> RankingResult:
        return run_phase3(self.ranked, self.config)

    def phase4(self, result: RankingResult) -> str:
        return format_results(result, self.zero_votes)