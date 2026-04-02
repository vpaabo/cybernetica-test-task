from .models import RankingResult


def format_results(result: RankingResult) -> str:
    lines = []

    lines.append("=== ELECTED MEMBERS ===")
    for idx, c in enumerate(result.elected, start=1):
        lines.append(f"{idx}. {c.name} ({c.team}) - {c.votes} votes")

    lines.append("")
    lines.append("=== ALTERNATES ===")
    if result.alternates:
        for idx, c in enumerate(result.alternates, start=1):
            lines.append(f"{idx}. {c.name} ({c.team}) - {c.votes} votes")
    else:
        lines.append("None")

    lines.append("")
    lines.append("=== FULL RESULTS ===")
    for c in result.full_ranking:
        status = "ELECTED" if c.elected else ""
        lines.append(f"{c.name} ({c.team}) - {c.votes} votes {status}")

    return "\n".join(lines)