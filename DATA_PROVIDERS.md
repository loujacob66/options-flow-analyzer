# Data Provider Setup Guide

This guide explains how to set up different data providers for the Options Flow Analyzer.

## Quick Start (No API Key Required)

Run the demo to see the tool in action with sample data:

```bash
python -m options_analyzer demo
```

## Free Data Providers

### 1. Polygon.io (Recommended)

**Free Tier**: 5 API calls per minute, good daily limits

1. Sign up at [polygon.io](https://polygon.io)
2. Get your free API key
3. Set environment variable:
   ```bash
   export POLYGON_API_KEY="your_api_key_here"
   ```

### 2. Alpha Vantage

**Free Tier**: 25 API calls per day

1. Sign up at [alphavantage.co](https://www.alphavantage.co)
2. Get your free API key
3. Set environment variable:
   ```bash
   export ALPHA_VANTAGE_API_KEY="your_api_key_here"
   ```

### 3. Tradier Developer

**Free Tier**: Delayed data (15-20 minutes)

1. Sign up at [developer.tradier.com](https://developer.tradier.com)
2. Get your sandbox API key
3. Set environment variable:
   ```bash
   export TRADIER_API_KEY="your_api_key_here"
   ```

## Environment Variable Setup

### macOS/Linux (Add to ~/.zshrc or ~/.bashrc):
```bash
export POLYGON_API_KEY="your_polygon_key"
export TRADIER_API_KEY="your_tradier_key"
```

### Windows:
```cmd
set POLYGON_API_KEY=your_polygon_key
set TRADIER_API_KEY=your_tradier_key
```

## Rate Limiting Guidelines

- **Polygon.io Free**: 5 calls/minute
- **Alpha Vantage**: 25 calls/day
- **Tradier**: 120 calls/minute (sandbox)
- **Yahoo Finance**: Variable rate limits

## Usage Examples

```bash
# Demo mode (no API key required)
python -m options_analyzer demo

# With specific ticker
python -m options_analyzer demo AAPL --min-volume 100

# Real data (requires API key)
python -m options_analyzer analyze SPY --min-volume 50

# Check your configuration
python -m options_analyzer config
```

## Troubleshooting

1. **Rate Limit Errors**: Wait and try again, or switch to a different provider
2. **API Key Issues**: Run `python -m options_analyzer config` to check if keys are set
3. **No Data**: Try the demo mode first to verify the tool works

## Production Considerations

For production use, consider:
- Paid API plans for higher rate limits
- Data caching to reduce API calls
- Multiple provider fallbacks
- Error handling and retry logic
