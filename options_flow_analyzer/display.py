"""Display module for formatting and presenting analysis results using rich."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import pandas as pd
from typing import Dict, Any
from .config import Config


class OptionsDisplay:
    """Handles display and formatting of options analysis results."""

    def __init__(self):
        self.console = Console()
        self.config = Config()

    def show_ticker_info(self, ticker_info: Dict[str, Any]):
        """Display basic ticker information."""
        if "error" in ticker_info:
            self.console.print(
                f"[red]Error fetching data for {ticker_info['symbol']}: {ticker_info['error']}[/red]"
            )
            return

        info_text = f"""
[bold]{ticker_info.get('company_name', ticker_info['symbol'])}[/bold]
Symbol: {ticker_info['symbol']}
Current Price: ${ticker_info.get('current_price', 0):.2f}
Volume: {ticker_info.get('volume', 0):,}
Market Cap: ${ticker_info.get('market_cap', 0):,}
"""
        panel = Panel(info_text, title="Stock Information", border_style="blue")
        self.console.print(panel)

    def show_flow_summary(self, flow_summary: Dict[str, Any]):
        """Display options flow summary."""
        if not flow_summary:
            self.console.print("[yellow]No flow data available[/yellow]")
            return

        # Create summary table
        table = Table(
            title="Options Flow Summary", show_header=True, header_style="bold magenta"
        )
        table.add_column("Metric", style="cyan")
        table.add_column("Calls", justify="right", style="green")
        table.add_column("Puts", justify="right", style="red")
        table.add_column("Net", justify="right", style="blue")

        table.add_row(
            "Volume",
            f"{flow_summary['total_call_volume']:,}",
            f"{flow_summary['total_put_volume']:,}",
            f"{flow_summary['net_volume']:,}",
        )

        table.add_row(
            "Dollar Flow",
            f"${flow_summary['total_call_flow']:,.0f}",
            f"${flow_summary['total_put_flow']:,.0f}",
            f"${flow_summary['net_dollar_flow']:,.0f}",
        )

        # Add sentiment indicator
        sentiment = "🟢 Bullish" if flow_summary["bullish_sentiment"] else "🔴 Bearish"

        summary_text = f"""
Put/Call Ratio: {flow_summary['put_call_ratio']:.2f}
Total Contracts: {flow_summary['total_contracts']:,}
Sentiment: {sentiment}
"""

        self.console.print(table)
        self.console.print(Panel(summary_text, title="Analysis", border_style="yellow"))

    def show_strike_analysis(self, strike_df: pd.DataFrame, max_rows: int = 15):
        """Display strike price analysis."""
        if strike_df.empty:
            self.console.print("[yellow]No strike data available[/yellow]")
            return

        table = Table(
            title="Top Strikes by Volume", show_header=True, header_style="bold magenta"
        )
        table.add_column("Strike", justify="right")
        table.add_column("Type", justify="center")
        table.add_column("Volume", justify="right")
        table.add_column("Open Interest", justify="right")
        table.add_column("Dollar Flow", justify="right")
        table.add_column("Distance %", justify="right")
        table.add_column("ITM/OTM", justify="center")

        for _, row in strike_df.head(max_rows).iterrows():
            # Color coding for calls/puts
            type_style = "green" if row["option_type"] == "call" else "red"
            moneyness_style = "bold" if row["moneyness"] == "ITM" else ""

            table.add_row(
                f"${row['strike']:.0f}",
                f"[{type_style}]{row['option_type'].upper()}[/{type_style}]",
                f"{row['volume']:,}",
                f"{row['openInterest']:,}",
                f"${row['dollar_flow']:,.0f}",
                f"{row['distance_pct']:+.1f}%",
                f"{row['moneyness']}",
            )

        self.console.print(table)

    def show_unusual_activity(self, unusual_df: pd.DataFrame, max_rows: int = 10):
        """Display unusual options activity."""
        if unusual_df.empty:
            self.console.print("[yellow]No unusual activity detected[/yellow]")
            return

        table = Table(
            title="Unusual Activity (High Volume/OI Ratio)",
            show_header=True,
            header_style="bold red",
        )
        table.add_column("Strike", justify="right")
        table.add_column("Type", justify="center")
        table.add_column("Expiration")
        table.add_column("Volume", justify="right")
        table.add_column("OI", justify="right")
        table.add_column("Vol/OI", justify="right")
        table.add_column("Dollar Flow", justify="right")

        for _, row in unusual_df.head(max_rows).iterrows():
            type_style = "green" if row["option_type"] == "call" else "red"

            table.add_row(
                f"${row['strike']:.0f}",
                f"[{type_style}]{row['option_type'].upper()}[/{type_style}]",
                str(row["expiration"]),
                f"{row['volume']:,}",
                f"{row['openInterest']:,}",
                f"{row['volume_oi_ratio']:.1f}x",
                f"${row['dollar_flow']:,.0f}",
            )

        self.console.print(table)

    def show_max_pain(self, max_pain_strike: float, max_pain_df: pd.DataFrame):
        """Display max pain analysis."""
        if max_pain_df.empty:
            return

        # Max pain info
        max_pain_text = f"""
Max Pain Strike: ${max_pain_strike:.0f}
(Strike with highest total open interest)
"""
        self.console.print(
            Panel(max_pain_text, title="Max Pain Analysis", border_style="purple")
        )

        # Top strikes by OI
        table = Table(
            title="Open Interest by Strike",
            show_header=True,
            header_style="bold purple",
        )
        table.add_column("Strike", justify="right")
        table.add_column("Open Interest", justify="right")
        table.add_column("Volume", justify="right")

        for _, row in max_pain_df.head(10).iterrows():
            table.add_row(
                f"${row['strike']:.0f}",
                f"{row['openInterest']:,}",
                f"{row['volume']:,}",
            )

        self.console.print(table)

    def show_expiration_analysis(self, exp_df: pd.DataFrame):
        """Display expiration analysis."""
        if exp_df.empty:
            return

        table = Table(
            title="Flow by Expiration", show_header=True, header_style="bold cyan"
        )
        table.add_column("Expiration")
        table.add_column("Volume", justify="right")
        table.add_column("Dollar Flow", justify="right")

        for _, row in exp_df.iterrows():
            table.add_row(
                str(row["expiration"]),
                f"{row['volume']:,}",
                f"${row['dollar_flow']:,.0f}",
            )

        self.console.print(table)

    def show_loading(self, message: str):
        """Show loading spinner."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            progress.add_task(description=message, total=None)

    def show_error(self, error_message: str):
        """Display error message."""
        # Escape markup in the error message to avoid Rich parsing issues
        from rich.markup import escape

        escaped_message = escape(error_message)
        self.console.print(f"[bold red]Error:[/bold red] {escaped_message}")

    def show_warning(self, warning_message: str):
        """Display warning message."""
        self.console.print(f"[bold yellow]Warning:[/bold yellow] {warning_message}")

    def show_success(self, success_message: str):
        """Display success message."""
        self.console.print(f"[bold green]✓[/bold green] {success_message}")

    def show_sweep_analysis(self, sweep_analysis: Dict[str, Any]):
        """Display sweep trade analysis results."""
        if not sweep_analysis:
            return

        # Sweep detection summary
        sweep_summary = f"""
Sweep Detection Summary:
  Total Contracts: {sweep_analysis.get('total_count', 0)}
  Detected Sweeps: {sweep_analysis.get('sweep_count', 0)}
  Sweep Percentage: {sweep_analysis.get('sweep_percentage', 0):.1f}%
"""

        self.console.print(
            Panel(sweep_summary, title="🔍 Sweep Analysis", border_style="yellow")
        )

        # Comparison table
        all_trades = sweep_analysis.get("all_trades", {})
        without_sweeps = sweep_analysis.get("without_sweeps", {})
        impact = sweep_analysis.get("impact", {})

        if all_trades and without_sweeps:
            table = Table(
                title="Flow Analysis: With vs Without Sweeps",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("Metric", style="cyan")
            table.add_column("All Trades", justify="right", style="blue")
            table.add_column("Without Sweeps", justify="right", style="green")
            table.add_column("Impact", justify="right", style="yellow")

            # Volume comparison
            table.add_row(
                "Net Volume",
                f"{all_trades.get('net_volume', 0):,}",
                f"{without_sweeps.get('net_volume', 0):,}",
                f"{impact.get('volume_change', 0):+,}",
            )

            # Dollar flow comparison
            table.add_row(
                "Net Dollar Flow",
                f"${all_trades.get('net_dollar_flow', 0):,.0f}",
                f"${without_sweeps.get('net_dollar_flow', 0):,.0f}",
                f"${impact.get('dollar_flow_change', 0):+,.0f}",
            )

            # Sentiment comparison
            all_sentiment = (
                "🟢 Bullish"
                if all_trades.get("bullish_sentiment", False)
                else "🔴 Bearish"
            )
            clean_sentiment = (
                "🟢 Bullish"
                if without_sweeps.get("bullish_sentiment", False)
                else "🔴 Bearish"
            )
            sentiment_change = (
                "⚠️ Changed" if impact.get("sentiment_change", False) else "✓ Same"
            )

            table.add_row("Sentiment", all_sentiment, clean_sentiment, sentiment_change)

            # Put/Call ratio comparison
            table.add_row(
                "Put/Call Ratio",
                f"{all_trades.get('put_call_ratio', 0):.2f}",
                f"{without_sweeps.get('put_call_ratio', 0):.2f}",
                f"{(without_sweeps.get('put_call_ratio', 0) - all_trades.get('put_call_ratio', 0)):+.2f}",
            )

            self.console.print(table)

        # Sweep-only analysis
        sweeps_only = sweep_analysis.get("sweeps_only", {})
        if sweeps_only:
            sweep_info = f"""
Sweep Trades Only:
  Volume: {sweeps_only.get('net_volume', 0):,} contracts
  Dollar Flow: ${sweeps_only.get('net_dollar_flow', 0):,.0f}
  Sentiment: {'🟢 Bullish' if sweeps_only.get('bullish_sentiment', False) else '🔴 Bearish'}
"""
            self.console.print(
                Panel(sweep_info, title="Sweep-Only Analysis", border_style="red")
            )

    def show_trade_classification(self, df: pd.DataFrame, max_rows: int = 10):
        """Display trade classification results."""
        if df.empty or "trade_type" not in df.columns:
            return

        # Count by trade type
        trade_counts = df["trade_type"].value_counts()

        count_table = Table(
            title="Trade Classification", show_header=True, header_style="bold purple"
        )
        count_table.add_column("Trade Type", style="purple")
        count_table.add_column("Count", justify="right")
        count_table.add_column("Percentage", justify="right")

        total = len(df)
        for trade_type, count in trade_counts.items():
            percentage = (count / total) * 100
            count_table.add_row(trade_type.title(), f"{count:,}", f"{percentage:.1f}%")

        self.console.print(count_table)

        # Show top sweep trades
        sweeps = df[df["trade_type"] == "sweep"].sort_values(
            "sweep_confidence", ascending=False
        )
        if not sweeps.empty:
            sweep_table = Table(
                title="Top Detected Sweeps", show_header=True, header_style="bold red"
            )
            sweep_table.add_column("Strike", justify="right")
            sweep_table.add_column("Type", justify="center")
            sweep_table.add_column("Volume", justify="right")
            sweep_table.add_column("Dollar Flow", justify="right")
            sweep_table.add_column("Confidence", justify="right")

            for _, row in sweeps.head(max_rows).iterrows():
                type_style = "green" if row["option_type"] == "call" else "red"
                confidence = row["sweep_confidence"]

                sweep_table.add_row(
                    f"${row['strike']:.0f}",
                    f"[{type_style}]{row['option_type'].upper()}[/{type_style}]",
                    f"{row['volume']:,}",
                    f"${row['dollar_flow']:,.0f}",
                    f"[{'bold red' if confidence > 0.7 else 'yellow'}]{confidence:.1%}[/{'bold red' if confidence > 0.7 else 'yellow'}]",
                )

            self.console.print(sweep_table)
