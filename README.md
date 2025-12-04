# Leaderboard Live‑Update Service

## Overview
This repository contains a **self‑contained Python utility** that reads an Excel workbook (`leaderboard.xlsx`) representing a championship leaderboard, applies a sophisticated ranking algorithm, and writes a sorted version (`leaderboard_sorted.xlsx`).  The ranking follows the exact criteria described in the original task brief:

1. **Total Points** – descending (zero for `D$Q` or `-`).
2. **Total Spending** – ascending (lower spend wins the tie).
3. **Count‑back System** – compare each player’s event scores from highest to lowest.
4. **Alphabetical Order** – final deterministic tie‑breaker; tied names are highlighted in **red**.

A short rationale (`rationale.md`) explains the tie‑breakers and suggests additional criteria for future extensions.

## Challenge Details
- The workbook contains a single sheet named **Leaderboard**.
- The top table (player points) and bottom table (spending) share the same layout as shown in the sample file.
- Columns for round scores are named `R01` … `R24` (24 events in the series).
- Cells containing `D$Q` or `-` are treated as **0**.
- No formulas need to be preserved – the script overwrites values with the sorted data.

## Design Decisions
| Decision | Reasoning |
|---|---|
| **Pandas + Openpyxl** | Pandas gives powerful data‑manipulation; Openpyxl lets us preserve the original workbook structure and apply cell‑level styling (red fill). |
| **Manual column renaming** | The source file has duplicate column names (`Pts`). Renaming ensures deterministic column access and avoids pandas errors. |
| **Full rewrite of the sheet** | Simpler than moving rows in‑place; guarantees the sorted order and correct styling. |
| **No GUI** | The task is a batch script; a UI would add unnecessary complexity for a 2‑3 hour prototype. |

---

## Architecture & Design Choices
- **`rank_leaderboard.py`** – Core script:
  - Loads the workbook with `pandas.read_excel(..., header=None)` to keep raw rows.
  - Detects the start of the top and bottom tables by searching for the header rows.
  - Normalises column names, cleans values, and builds a **sort key** tuple:
    ```python
    (-total_points, total_spending, tuple(-score for score in countback), player_name)
    ```
  - Detects ties (identical keys except the name) and highlights those rows in red.
  - Writes the sorted data back using **Openpyxl**, preserving the original sheet layout.
- **`rationale.md`** – Human‑readable explanation of the ranking logic and possible future tie‑breakers.
- **`verify_ranking.py`** – Small helper that loads the sorted workbook and asserts that the ranking respects the defined criteria (useful for CI or quick sanity checks).
- **`README.md`** – This documentation file (generated now).

---

## File Structure
```
leaderboard-live-update-service/
│
├─ leaderboard.xlsx               # Original data (provided)
├─ rank_leaderboard.py            # Main ranking implementation
├─ rationale.md                   # Design rationale & future ideas
├─ verify_ranking.py              # Simple verification script
└─ leaderboard_sorted.xlsx        # Generated Output after running the script
---

## How to Run
1. **Install dependencies** (once):
   ```bash
   pip install pandas openpyxl
   ```
2. **Execute the ranking script**:
   ```bash
   python rank_leaderboard.py
   ```
   You will see a console message:
   ```
   Sorted leaderboard saved to leaderboard_sorted.xlsx
   ```
3. Open `leaderboard_sorted.xlsx` – the rows are now ordered according to the rules, and any tied players are highlighted in **red**.

---

## Future Improvements (If i have more time)
- **Command‑line arguments** for input/output paths, sheet name, and custom tie‑breaker selection.
- **Unit‑test suite** using `pytest` to cover edge cases (e.g., all `D$Q`, missing columns).
- **Web UI** (e.g., a lightweight Flask app) to upload a workbook and display the sorted table instantly.
- **Persist original formulas** – copy formulas instead of raw values when possible.
- **Configurable ranking pipeline** – plug‑in additional criteria such as recent form, disqualification count, or head‑to‑head comparison.
- **Docker container** for reproducible execution across environments.

