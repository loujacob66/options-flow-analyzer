"""CLI entry point for Options Flow Analyzer using Typer."""

import typer
from typing import Optional
from .data_fetcher import OptionsDataFetcher
from .analyzer import OptionsAnalyzer
from .display import OptionsDisplay
from .config import Config

app = typer.Typer(help="Options Flow Analyzer - Analyze options market activity")


@app.command()
def analyze(
    ticker: str = typer.Argument(..., help="Stock ticker symbol (e.g., SPY, AAPL)"),
    expiration: Optional[str] = typer.Option(
        None, "--expiration", "-e", help="Expiration date in YYYY-MM-DD format"
    ),
    min_volume: int = typer.Option(
        10, "--min-volume", "-v", help="Minimum volume for filtering"
    ),
    option_type: Optional[str] = typer.Option(
        None, "--option-type", "-t", help="Option type: calls or puts"
    ),
    show_unusual: bool = typer.Option(
        True, "--unusual/--no-unusual", help="Show unusual activity analysis"
    ),
    show_max_pain: bool = typer.Option(
        True, "--max-pain/--no-max-pain", help="Show max pain analysis"
    ),
    detect_sweeps: bool = typer.Option(
        True, "--sweeps/--no-sweeps", help="Detect and analyze sweep trades"
    ),
    multiple_expirations: bool = typer.Option(
        False, "--multi-exp", "-m", help="Analyze multiple expirations"
    ),
):
    """Analyze options flow data for a given ticker."""

    # Initialize components
    fetcher = OptionsDataFetcher()
    analyzer = OptionsAnalyzer()
    display = OptionsDisplay()

    # Validate ticker format
    ticker = ticker.upper().strip()

    try:
        # Show loading message
        display.console.print(
            f"\n[bold blue]Fetching options data for {ticker}...[/bold blue]"
        )

        # Try to get ticker info from Polygon first, fallback to yfinance
        ticker_info = fetcher.get_polygon_ticker_info(ticker)
        if "error" in ticker_info:
            display.show_warning("Polygon API failed, trying yfinance...")
            ticker_info = fetcher.get_ticker_info(ticker)

        display.show_ticker_info(ticker_info)

        if "error" in ticker_info:
            display.show_error(
                "All data sources failed. Try using demo mode: python -m options_analyzer demo"
            )
            return

        current_price = ticker_info.get("current_price", 0)

        # Fetch options data using Polygon API
        if multiple_expirations:
            display.show_warning(
                "Multiple expirations not fully supported with Polygon API yet"
            )
            options_data = fetcher.get_polygon_options_data(ticker, expiration)
        else:
            options_data = fetcher.get_polygon_options_data(ticker, expiration)

        if options_data.empty:
            display.show_error(f"No options data found for {ticker}")
            return

        # Filter data based on criteria
        filtered_data = fetcher.filter_options_data(
            options_data, min_volume=min_volume, option_type=option_type
        )

        if filtered_data.empty:
            display.show_warning(f"No options data matches the specified criteria")
            return

        display.show_success(
            f"Found {len(filtered_data)} option contracts matching criteria"
        )

        # Detect sweeps if requested
        if detect_sweeps:
            display.console.print(
                "\n[bold yellow]Detecting sweep trades...[/bold yellow]"
            )
            filtered_data = analyzer.detect_sweeps(filtered_data)

            # Show trade classification
            display.show_trade_classification(filtered_data)

            # Analyze with and without sweeps
            sweep_analysis = analyzer.analyze_without_sweeps(filtered_data)
            display.show_sweep_analysis(sweep_analysis)

            # Use clean data (without sweeps) for main analysis
            clean_data = filtered_data[filtered_data["trade_type"] != "sweep"].copy()
            if not clean_data.empty:
                flow_summary = analyzer.calculate_flow_summary(clean_data)
                strike_analysis = analyzer.analyze_strike_distribution(
                    clean_data, current_price
                )
                display.console.print(
                    "\n[bold green]Analysis below excludes sweep trades for cleaner sentiment:[/bold green]"
                )
            else:
                flow_summary = analyzer.calculate_flow_summary(filtered_data)
                strike_analysis = analyzer.analyze_strike_distribution(
                    filtered_data, current_price
                )
        else:
            # Regular analysis without sweep detection
            flow_summary = analyzer.calculate_flow_summary(filtered_data)
            strike_analysis = analyzer.analyze_strike_distribution(
                filtered_data, current_price
            )

        # Display results
        display.show_flow_summary(flow_summary)
        display.show_strike_analysis(strike_analysis)

        # Optional analyses
        if show_unusual:
            unusual_activity = analyzer.identify_unusual_activity(filtered_data)
            if not unusual_activity.empty:
                display.show_unusual_activity(unusual_activity)

        if show_max_pain:
            max_pain_strike, max_pain_df = analyzer.find_max_pain(filtered_data)
            if not max_pain_df.empty:
                display.show_max_pain(max_pain_strike, max_pain_df)

        # Show expiration analysis if multiple expirations
        if multiple_expirations:
            exp_analysis = analyzer.analyze_expiration_flow(filtered_data)
            if not exp_analysis.empty:
                display.show_expiration_analysis(exp_analysis)

        display.console.print("\n[bold green]Analysis complete![/bold green]")

    except Exception as e:
        display.show_error(f"An error occurred during analysis: {str(e)}")
        raise typer.Exit(1)


@app.command()
def expirations(ticker: str = typer.Argument(..., help="Stock ticker symbol")):
    """List available expiration dates for a ticker."""

    fetcher = OptionsDataFetcher()
    display = OptionsDisplay()

    ticker = ticker.upper().strip()

    try:
        expirations = fetcher.get_options_expirations(ticker)

        if not expirations:
            display.show_error(f"No options expirations found for {ticker}")
            return

        display.console.print(
            f"\n[bold blue]Available expirations for {ticker}:[/bold blue]"
        )
        for exp in expirations:
            display.console.print(f"  • {exp}")

    except Exception as e:
        display.show_error(f"Error fetching expirations: {str(e)}")
        raise typer.Exit(1)


@app.command()
def demo(
    ticker: str = typer.Argument("SPY", help="Stock ticker symbol for demo"),
    min_volume: int = typer.Option(
        50, "--min-volume", "-v", help="Minimum volume for filtering"
    ),
):
    """Run a demo with sample data (no API keys required)."""

    # Initialize components
    fetcher = OptionsDataFetcher()
    analyzer = OptionsAnalyzer()
    display = OptionsDisplay()

    ticker = ticker.upper().strip()

    try:
        display.console.print(
            f"\n[bold blue]Running demo analysis for {ticker} with sample data...[/bold blue]"
        )

        # Show sample ticker info
        ticker_info = {
            "symbol": ticker,
            "current_price": 100.0,
            "market_cap": 50000000000,
            "volume": 75000000,
            "company_name": f"{ticker} Sample Company",
        }
        display.show_ticker_info(ticker_info)

        current_price = ticker_info["current_price"]

        # Get sample options data
        options_data = fetcher.get_sample_options_data(ticker)

        # Filter data based on criteria
        filtered_data = fetcher.filter_options_data(options_data, min_volume=min_volume)

        if filtered_data.empty:
            display.show_warning(f"No sample data matches the specified criteria")
            return

        display.show_success(f"Generated {len(filtered_data)} sample option contracts")

        # Perform analysis
        flow_summary = analyzer.calculate_flow_summary(filtered_data)
        strike_analysis = analyzer.analyze_strike_distribution(
            filtered_data, current_price
        )

        # Display results
        display.show_flow_summary(flow_summary)
        display.show_strike_analysis(strike_analysis)

        # Show unusual activity
        unusual_activity = analyzer.identify_unusual_activity(filtered_data)
        if not unusual_activity.empty:
            display.show_unusual_activity(unusual_activity)

        # Show max pain
        max_pain_strike, max_pain_df = analyzer.find_max_pain(filtered_data)
        if not max_pain_df.empty:
            display.show_max_pain(max_pain_strike, max_pain_df)

        # Show expiration analysis
        exp_analysis = analyzer.analyze_expiration_flow(filtered_data)
        if not exp_analysis.empty:
            display.show_expiration_analysis(exp_analysis)

        display.console.print("\n[bold green]Demo analysis complete![/bold green]")
        display.console.print(
            "\n[yellow]Note: This demo uses randomly generated sample data for demonstration purposes.[/yellow]"
        )

    except Exception as e:
        display.show_error(f"An error occurred during demo: {str(e)}")
        raise typer.Exit(1)


@app.command()
def config():
    """Show current configuration."""

    display = OptionsDisplay()
    config = Config()

    config_text = f"""
API Configuration:
  Tradier API Key: {'✓ Set' if config.TRADIER_API_KEY else '✗ Not set'}
  Polygon API Key: {'✓ Set' if config.POLYGON_API_KEY else '✗ Not set'}
  
Default Settings:
  Min Volume: {config.DEFAULT_MIN_VOLUME}
  Expiration Days: {config.DEFAULT_EXPIRATION_DAYS}
  Max Strikes Display: {config.MAX_STRIKES_DISPLAY}
  Decimal Places: {config.DECIMAL_PLACES}
"""

    display.console.print(config_text)


if __name__ == "__main__":
    app()
