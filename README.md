# Options Flow Analyzer

A command-line tool designed to help traders and analysts interpret options market activity by aggregating and visualizing option volume, open interest, and estimated dollar flow.

## Features

- Query options data by ticker and expiration
- Display call/put volume and open interest
- Calculate net estimated dollar flow (volume × premium × 100)
- Strike and expiration breakdowns
- Filter by expiration date, minimum volume, and option type

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage
python -m options_analyzer SPY

# With specific expiration
python -m options_analyzer SPY --expiration 2024-01-19

# Filter by minimum volume
python -m options_analyzer AAPL --min-volume 100

# Show only calls or puts
python -m options_analyzer TSLA --option-type calls

# Show help
python -m options_analyzer --help
```

## Project Structure

```
options-flow-analyzer/
├── options_analyzer/
│   ├── __init__.py
│   ├── cli.py           # CLI interface
│   ├── data_fetcher.py  # Data fetching from APIs
│   ├── analyzer.py      # Core analysis logic
│   ├── display.py       # Output formatting
│   └── config.py        # Configuration
├── tests/
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- Internet connection for API calls
