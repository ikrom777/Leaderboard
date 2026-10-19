# Leaderboard

A command-line leaderboard application written in Python. Players enter their names and scores, and the leaderboard is stored in a CSV file and always shown from the lowest score to the highest.

## Features

- **Add players** with a name and a score
- **No duplicate names**: a name can only appear once on the leaderboard
- **Update scores** for existing players
- **Search players** by name
- **Sorted display**: scores are listed in ascending order (lowest to highest)
- **CSV persistence**: data is saved to a CSV file and loaded again on the next run
- **Tested**: pytest test suite with 99% statement coverage

## Requirements

- Python 3
- `pytest` and `pytest-cov` (only needed to run the tests)

## Installation

```bash
git clone https://github.com/ikrom777/Leaderboard.git
cd Leaderboard
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python Leaderboard.py
```

Follow the on-screen prompts to add a player, update a score, search for a player, or view the leaderboard.

### Example

```
Leaderboard (lowest to highest)
1. Alex    - 120
2. Sam     - 250
3. Jordan  - 410
```

## Running the tests

Run all tests:

```bash
pytest -v
```

Run tests with a coverage report:

```bash
pytest --cov
```

Current coverage is **99%** (158 of 160 statements). The two uncovered lines belong to the `if __name__ == "__main__":` startup block, which is intentionally left out.

### What the tests cover

- Adding players and rejecting duplicate names
- Searching for existing and missing players
- Updating scores, including players that do not exist
- Sorting in ascending order (parametrized tests)
- Reading and writing CSV files using temporary files (`tmp_path`)
- Printed output (`capsys`) and user input (`monkeypatch`)
- Error handling (`pytest.raises`)

## Project structure

```
leaderboard/
├── Leaderboard.py        # Leaderboard class and program entry point
├── test_Leaderboard.py   # pytest tests
├── leaderboard.csv       # Saved player data
├── requirements.txt      # Test dependencies
├── .gitignore
└── README.md
```

## How it works

The project uses object-oriented design. A `Leaderboard` class manages the list of players: adding, searching, updating and sorting. Data is read from and written to a CSV file so scores are kept between runs.

## Possible improvements

- Reject invalid scores (negative numbers, non-numbers)
- Case-insensitive duplicate name check
- Delete a player
- Option to switch between ascending and descending order
- Top-N view

## What I learned

Python OOP and refactoring, writing a pytest suite, fixtures and temporary files, mocking input with `monkeypatch`, capturing output with `capsys`, testing exceptions with `pytest.raises`, and measuring coverage with `pytest-cov`.