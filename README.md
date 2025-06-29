# Options Flow Analyzer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/YOUR_USERNAME/options-flow-analyzer/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/options-flow-analyzer/actions)

A powerful command-line tool designed to help traders and analysts interpret options market activity by aggregating and visualizing option volume, open interest, and estimated dollar flow.

**🚀 Key Feature: Advanced Sweep Detection** - Filter out institutional noise to reveal true retail sentiment!

## Features

### Core Analysis
- 📊 Query options data by ticker and expiration
- 💰 Calculate net estimated dollar flow (volume × premium × 100)
- 🎯 Strike and expiration breakdowns
- 🔍 Identify unusual activity (high volume/OI ratios)
- 🎯 Max pain analysis

### 🚀 Advanced Features
- **🔥 Sweep Detection**: Automatically identify and filter institutional sweep trades
- **🎨 Rich CLI Display**: Beautiful tables and analysis with color coding
- **📦 Multiple Data Sources**: Support for Polygon.io, Yahoo Finance, and more
- **🎭 Demo Mode**: Test the tool with sample data (no API key required)

### Filtering & Analysis
- Filter by expiration date, minimum volume, and option type
- Compare analysis with and without sweep trades
- Trade classification (Retail, Block, Sweep)
- Sentiment analysis (Bullish/Bearish indicators)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Try the Demo (No API Key Required)
```bash
# Run demo with sample data
python -m options_analyzer demo

# Demo with specific ticker and volume filter
python -m options_analyzer demo AAPL --min-volume 100
```

### Real Data Analysis
1. Get a free API key from [Polygon.io](https://polygon.io)
2. Create a `.env` file:
   ```bash
   POLYGON_API_KEY=your_api_key_here
   ```
3. Run analysis:
   ```bash
   python -m options_analyzer analyze SPY
   ```

## Usage Examples

```bash
# Basic analysis with sweep detection
python -m options_analyzer analyze SPY

# Filter by minimum volume and disable sweep detection
python -m options_analyzer analyze AAPL --min-volume 100 --no-sweeps

# Show only calls with specific expiration
python -m options_analyzer analyze TSLA --option-type calls --expiration 2024-01-19

# Check configuration
python -m options_analyzer config

# Show help
python -m options_analyzer --help
```

## Example Output

```
📈 Options Flow Summary
┏━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ Metric ┃ Calls ┃  Puts ┃   Net ┃
┡━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━┩
│ Volume │ 14,742│ 10,516│  4,226│
│ Flow   │  $8.5M│  $5.8M│ $2.7M │
└───────┴───────┴───────┴───────┘

Sentiment: 🟢 Bullish | P/C Ratio: 0.71

🔍 Sweep Detection: 3 sweeps (6.1%) detected and filtered
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
