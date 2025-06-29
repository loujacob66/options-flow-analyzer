"""Basic tests for Options Flow Analyzer."""

import pytest
import pandas as pd
from options_analyzer.data_fetcher import OptionsDataFetcher
from options_analyzer.analyzer import OptionsAnalyzer
from options_analyzer.config import Config


def test_config_validation():
    """Test that config validation works."""
    assert Config.validate_api_keys() == True


def test_options_data_fetcher_init():
    """Test that OptionsDataFetcher initializes correctly."""
    fetcher = OptionsDataFetcher()
    assert fetcher is not None
    assert fetcher.config is not None


def test_options_analyzer_init():
    """Test that OptionsAnalyzer initializes correctly."""
    analyzer = OptionsAnalyzer()
    assert analyzer is not None


def test_empty_dataframe_handling():
    """Test that analyzer handles empty DataFrames gracefully."""
    analyzer = OptionsAnalyzer()
    empty_df = pd.DataFrame()
    
    # Test flow summary with empty data
    flow_summary = analyzer.calculate_flow_summary(empty_df)
    assert flow_summary == {}
    
    # Test strike analysis with empty data
    strike_analysis = analyzer.analyze_strike_distribution(empty_df, 100.0)
    assert strike_analysis.empty


def test_filter_options_data():
    """Test options data filtering."""
    fetcher = OptionsDataFetcher()
    
    # Create sample data
    sample_data = pd.DataFrame({
        'volume': [100, 50, 200, 10],
        'option_type': ['call', 'put', 'call', 'put'],
        'openInterest': [500, 300, 800, 50]
    })
    
    # Test volume filtering
    filtered = fetcher.filter_options_data(sample_data, min_volume=75)
    assert len(filtered) == 2  # Only rows with volume >= 75
    
    # Test option type filtering
    calls_only = fetcher.filter_options_data(sample_data, option_type='call')
    assert len(calls_only) == 2
    assert all(calls_only['option_type'] == 'call')


if __name__ == "__main__":
    pytest.main([__file__])
