"""Analysis module for processing options data and calculating key metrics."""

import pandas as pd
from typing import Dict, Any, Tuple


class OptionsAnalyzer:
    """Analyzes options data to extract meaningful insights."""

    def __init__(self):
        pass

    def calculate_flow_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate summary statistics for options flow.

        Args:
            df: Options DataFrame

        Returns:
            Dictionary with flow summary metrics
        """
        if df.empty:
            return {}

        # Separate calls and puts
        calls = df[df["option_type"] == "call"]
        puts = df[df["option_type"] == "put"]

        # Calculate total flows
        total_call_volume = calls["volume"].sum()
        total_put_volume = puts["volume"].sum()
        total_call_flow = calls["dollar_flow"].sum()
        total_put_flow = puts["dollar_flow"].sum()

        # Calculate net flows
        net_volume = total_call_volume - total_put_volume
        net_dollar_flow = total_call_flow - total_put_flow

        # Call/Put ratio
        put_call_ratio = (
            total_put_volume / total_call_volume if total_call_volume > 0 else 0
        )

        return {
            "total_call_volume": int(total_call_volume),
            "total_put_volume": int(total_put_volume),
            "total_call_flow": total_call_flow,
            "total_put_flow": total_put_flow,
            "net_volume": int(net_volume),
            "net_dollar_flow": net_dollar_flow,
            "put_call_ratio": put_call_ratio,
            "total_contracts": len(df),
            "bullish_sentiment": net_dollar_flow > 0,
        }

    def analyze_strike_distribution(
        self, df: pd.DataFrame, current_price: float
    ) -> pd.DataFrame:
        """
        Analyze volume and flow distribution across strike prices.

        Args:
            df: Options DataFrame
            current_price: Current stock price

        Returns:
            DataFrame with strike-level analysis
        """
        if df.empty:
            return pd.DataFrame()

        # Group by strike and option type
        strike_analysis = (
            df.groupby(["strike", "option_type"])
            .agg(
                {
                    "volume": "sum",
                    "openInterest": "sum",
                    "dollar_flow": "sum",
                    "lastPrice": "mean",
                }
            )
            .reset_index()
        )

        # Add distance from current price
        strike_analysis["distance_from_price"] = (
            strike_analysis["strike"] - current_price
        )
        strike_analysis["distance_pct"] = (
            strike_analysis["distance_from_price"] / current_price
        ) * 100

        # Add ITM/OTM classification
        def classify_moneyness(row):
            if row["option_type"] == "call":
                return "ITM" if row["strike"] < current_price else "OTM"
            else:  # put
                return "ITM" if row["strike"] > current_price else "OTM"

        strike_analysis["moneyness"] = strike_analysis.apply(classify_moneyness, axis=1)

        # Sort by volume descending
        return strike_analysis.sort_values("volume", ascending=False)

    def find_max_pain(self, df: pd.DataFrame) -> Tuple[float, pd.DataFrame]:
        """
        Calculate max pain point (strike with maximum open interest).

        Args:
            df: Options DataFrame

        Returns:
            Tuple of (max_pain_strike, max_pain_analysis)
        """
        if df.empty:
            return 0.0, pd.DataFrame()

        # Group by strike and calculate total open interest
        oi_by_strike = (
            df.groupby("strike")
            .agg({"openInterest": "sum", "volume": "sum"})
            .reset_index()
        )

        # Find strike with maximum open interest
        max_pain_strike = oi_by_strike.loc[
            oi_by_strike["openInterest"].idxmax(), "strike"
        ]

        return max_pain_strike, oi_by_strike.sort_values(
            "openInterest", ascending=False
        )

    def analyze_expiration_flow(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze flow distribution across expiration dates.

        Args:
            df: Options DataFrame

        Returns:
            DataFrame with expiration-level analysis
        """
        if df.empty:
            return pd.DataFrame()

        exp_analysis = (
            df.groupby(["expiration", "option_type"])
            .agg({"volume": "sum", "openInterest": "sum", "dollar_flow": "sum"})
            .reset_index()
        )

        # Calculate total flow per expiration
        exp_totals = (
            df.groupby("expiration")
            .agg({"volume": "sum", "dollar_flow": "sum"})
            .reset_index()
        )

        exp_totals = exp_totals.sort_values("dollar_flow", ascending=False)

        return exp_totals

    def identify_unusual_activity(
        self, df: pd.DataFrame, volume_threshold: float = 2.0
    ) -> pd.DataFrame:
        """
        Identify contracts with unusually high volume relative to open interest.

        Args:
            df: Options DataFrame
            volume_threshold: Volume/OI ratio threshold for unusual activity

        Returns:
            DataFrame with unusual activity contracts
        """
        if df.empty:
            return pd.DataFrame()

        # Calculate volume to open interest ratio
        df_copy = df.copy()
        df_copy["volume_oi_ratio"] = df_copy["volume"] / (
            df_copy["openInterest"] + 1
        )  # +1 to avoid division by zero

        # Filter for unusual activity
        unusual = df_copy[df_copy["volume_oi_ratio"] >= volume_threshold]

        # Sort by volume and dollar flow
        unusual = unusual.sort_values(
            ["volume", "dollar_flow"], ascending=[False, False]
        )

        return unusual[
            [
                "strike",
                "option_type",
                "expiration",
                "volume",
                "openInterest",
                "volume_oi_ratio",
                "dollar_flow",
                "lastPrice",
            ]
        ]

    def calculate_gamma_exposure(
        self, df: pd.DataFrame, current_price: float
    ) -> Dict[str, float]:
        """
        Estimate gamma exposure at different price levels (simplified calculation).

        Args:
            df: Options DataFrame
            current_price: Current stock price

        Returns:
            Dictionary with gamma exposure estimates
        """
        if df.empty:
            return {}

        # Simplified gamma calculation (actual gamma would require Black-Scholes)
        # This is a rough approximation for demonstration

        gamma_exposure = {}
        price_levels = [
            current_price * (1 + i * 0.01) for i in range(-10, 11)
        ]  # ±10% in 1% increments

        for price in price_levels:
            total_gamma = 0

            for _, row in df.iterrows():
                # Simplified gamma approximation
                moneyness = row["strike"] / price
                if 0.9 <= moneyness <= 1.1:  # Near the money options have higher gamma
                    gamma_contribution = row["openInterest"] * (
                        1 - abs(moneyness - 1) * 5
                    )
                    if row["option_type"] == "call":
                        total_gamma += gamma_contribution
                    else:
                        total_gamma -= gamma_contribution

            gamma_exposure[f"{price:.2f}"] = total_gamma

        return gamma_exposure

    def detect_sweeps(
        self, df: pd.DataFrame, sweep_threshold: float = 0.5
    ) -> pd.DataFrame:
        """
        Detect and classify sweep trades in options data.

        Sweep characteristics:
        - Large volume relative to average
        - Rapid execution across multiple exchanges
        - Often institutional block trades
        - May indicate hedging rather than directional sentiment

        Args:
            df: Options DataFrame
            sweep_threshold: Minimum volume percentile to consider for sweep detection

        Returns:
            DataFrame with sweep classification
        """
        if df.empty:
            return df

        df_copy = df.copy()

        # Calculate volume statistics for sweep detection
        volume_75th = df_copy["volume"].quantile(0.75)
        volume_95th = df_copy["volume"].quantile(0.95)

        # Sweep detection criteria
        def classify_trade_type(row):
            volume = row["volume"]
            oi = row["openInterest"]
            vol_oi_ratio = volume / (oi + 1)  # Avoid division by zero

            # Large volume indicators
            is_large_volume = volume >= volume_95th
            is_high_vol_oi = vol_oi_ratio >= 2.0

            # Price characteristics (simplified - in real implementation would use bid/ask)
            # For now, we'll use dollar flow as a proxy
            dollar_flow = row["dollar_flow"]
            is_large_dollar_flow = dollar_flow >= df_copy["dollar_flow"].quantile(0.90)

            # Sweep classification
            if is_large_volume and (is_high_vol_oi or is_large_dollar_flow):
                return "sweep"
            elif volume >= volume_75th:
                return "block"
            else:
                return "retail"

        df_copy["trade_type"] = df_copy.apply(classify_trade_type, axis=1)

        # Add sweep confidence score
        def calculate_sweep_confidence(row):
            if row["trade_type"] != "sweep":
                return 0.0

            volume_score = min(row["volume"] / volume_95th, 3.0) / 3.0
            vol_oi_score = min(row["volume"] / (row["openInterest"] + 1), 5.0) / 5.0
            dollar_score = (
                min(row["dollar_flow"] / df_copy["dollar_flow"].quantile(0.95), 2.0)
                / 2.0
            )

            return (volume_score + vol_oi_score + dollar_score) / 3.0

        df_copy["sweep_confidence"] = df_copy.apply(calculate_sweep_confidence, axis=1)

        return df_copy

    def analyze_without_sweeps(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform flow analysis excluding sweep trades to get cleaner sentiment.

        Args:
            df: Options DataFrame with trade_type classification

        Returns:
            Dictionary comparing analysis with and without sweeps
        """
        if df.empty or "trade_type" not in df.columns:
            return {}

        # Original analysis (all trades)
        all_trades_summary = self.calculate_flow_summary(df)

        # Analysis without sweeps
        non_sweep_df = df[df["trade_type"] != "sweep"].copy()
        clean_summary = (
            self.calculate_flow_summary(non_sweep_df) if not non_sweep_df.empty else {}
        )

        # Sweep-only analysis
        sweep_df = df[df["trade_type"] == "sweep"].copy()
        sweep_summary = (
            self.calculate_flow_summary(sweep_df) if not sweep_df.empty else {}
        )

        # Calculate the impact of removing sweeps
        impact_analysis = {}
        if all_trades_summary and clean_summary:
            impact_analysis = {
                "volume_change": clean_summary.get("net_volume", 0)
                - all_trades_summary.get("net_volume", 0),
                "dollar_flow_change": clean_summary.get("net_dollar_flow", 0)
                - all_trades_summary.get("net_dollar_flow", 0),
                "sentiment_change": clean_summary.get("bullish_sentiment", False)
                != all_trades_summary.get("bullish_sentiment", False),
            }

        return {
            "all_trades": all_trades_summary,
            "without_sweeps": clean_summary,
            "sweeps_only": sweep_summary,
            "impact": impact_analysis,
            "sweep_count": len(sweep_df),
            "total_count": len(df),
            "sweep_percentage": len(sweep_df) / len(df) * 100 if len(df) > 0 else 0,
        }
