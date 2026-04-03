# Ranking Application Prototype

## Overview

This project implements a prototype application that processes voting results and produces rankings according to a multi-phase election algorithm.

The system follows a staged approach:

- Phase 1 – Selection of qualifying candidates
- Phase 2 – Manual draw resolution (conceptual support)
- Phase 3 – Allocation of seats (team seats and vacancies)
- Phase 4 – Final result display

The implementation is written in Python and includes unit tests covering core logic, edge cases, and algorithmic invariants.

---

## Problem Description

The application reads structured input data containing:

- Number of team seats
- Number of open positions
- Candidate name
- Team name
- Vote count

It then executes a deterministic ranking and seat allocation process according to the provided specification.

Zero-vote candidates are treated as non-qualifying and are excluded from ranking and seat allocation.

---

## File Structure
<pre>
project-root/ 
│
├── ranking/
│   ├── engine.py
│   ├── models.py
│   ├── parser.py
│   ├── phase1.py
│   ├── phase2.py
│   ├── phase3.py
│   └── pahse4.py
│
├── tests/
│   ├── __init__.py
│   └── test_ranking.py
│
├── cli.py
├── example_input.txt
└── README.md
</pre>
---

## Algorithm Description

### Phase 1 – Selection of Qualifying Candidates

- Candidates with at least one vote are ranked in descending order of votes.
- Ties are detected and recorded.
- Candidates with zero votes are separated and excluded from further phases.

Output:
- Ranked candidates (votes >= 1)
- Groups of tied people
- Zero-vote candidates

---

### Phase 2 – Solving Draws

If tie groups exist from Phase 1, the user can manually adjust their order via the CLI.

This allows deterministic resolution of tied candidates according to the manual draw.

---

### Phase 3 – Seat Allocation

Seat allocation occurs in two stages:

1. Team Seat Allocation  
   - Iterate through ranked candidates.
   - Elect the highest-ranked candidate from each team.
   - Stop when all seats are filled or when all teams have a representative.

2. Vacancy Allocation  
   - Remaining seats are filled by the next highest-ranked candidates.
   - Previously elected candidates are skipped.

Remaining ranked candidates become alternates.

Zero-vote candidates are excluded from election and alternates.

---

### Phase 4 – Result Display

The application outputs:

- List of elected candidates
- List of alternates
- Full ranked list

Each candidate has a status:
- "ELECTED"
- "ALTERNATE"
- "" (non-qualifying / zero votes)

---

## Design Decisions

### 1. Separation of Phases

Each phase is implemented independently to:
- Improve clarity
- Enable testing at phase granularity
- Simplify future modifications

### 2. Deterministic Ordering

Sorting uses:
- Primary key: vote count (descending)
- Secondary key: candidate name (ascending)

This ensures deterministic behavior without randomness.

### 3. Zero-Vote Handling

Zero-vote candidates:
- Are excluded from ranking
- Are not eligible for election
- Are not alternates
- Are shown only in the full results

This is a deliberate strict interpretation of the specification.

---
## Running the CLI
```python
python cli.py example_input.txt
```

## Testing

The test suite includes:

1. Phase-level tests
2. Invariant validation
3. Edge case coverage
4. Boundary condition checks
5. Negative input validation

Examples of tested invariants:

- No more candidates elected than available seats
- No duplicate elections
- Elected and alternate sets are disjoint
- Deterministic behavior for tie cases
- Proper handling of empty inputs

Run tests with:
```python
python -m unittest discover
```

---

## Versioning Strategy

Recommended approach:

- Semantic Versioning (MAJOR.MINOR.PATCH)
- Git feature branching
- Pull request reviews
- Protected main branch

Branching model:

- main – stable production-ready branch
- feature/* – new features
- fix/* – bug fixes

Rationale:
- Clear history
- Controlled integration
- Scalable to team development

---

## Assumptions

- Candidate names are unique identifiers.
- Vote counts are non-negative integers.
- Input file format strictly follows specification.
- Team seat count and open position count are valid integers.

---

## Future Improvements

- Web-based interface
- Integration-level tests
- Property-based randomized testing
- Coverage enforcement

---

## Disclaimer

This project was developed with the assistance of AI tools to support reasoning, structuring, and validation. Design decisions, implementation adjustments, and final review were critically evaluated by the author.
