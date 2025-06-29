"""Data fetching module for options data from various APIs."""

import yfinance as yf
import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from .config import Config


class OptionsDataFetcher:
    """Fetches options data from various sources."""
    
    def __init__(self):
        self.config = Config()
    
    def get_ticker_info(self, ticker: str) -> Dict[str, Any]:
        """Get basic ticker information."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                'symbol': ticker,
                'current_price': info.get('currentPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'company_name': info.get('shortName', ticker)
            }
        except Exception as e:
            return {'symbol': ticker, 'error': str(e)}
    
    def get_options_expirations(self, ticker: str) -> List[str]:
        """Get available expiration dates for options."""
        try:
            stock = yf.Ticker(ticker)
            return list(stock.options)
        except Exception as e:
            print(f"Error fetching expirations for {ticker}: {e}")
            return []
    
    def get_options_chain(self, ticker: str, expiration: Optional[str] = None) -> pd.DataFrame:
        """
        Get options chain data for a ticker.
        
        Args:
            ticker: Stock symbol
            expiration: Expiration date (YYYY-MM-DD), if None uses nearest expiration
            
        Returns:
            DataFrame with options data including calls and puts
        """
        try:
            stock = yf.Ticker(ticker)
            
            # If no expiration specified, use the nearest one
            if not expiration:
                expirations = stock.options
                if not expirations:
                    return pd.DataFrame()
                expiration = expirations[0]
            
            # Get options chain for the expiration
            options_chain = stock.option_chain(expiration)
            
            # Combine calls and puts with type indicator
            calls = options_chain.calls.copy()
            calls['option_type'] = 'call'
            
            puts = options_chain.puts.copy()
            puts['option_type'] = 'put'
            
            # Combine both
            combined = pd.concat([calls, puts], ignore_index=True)
            
            # Add expiration date
            combined['expiration'] = expiration
            
            # Calculate estimated dollar flow (volume * last price * 100)
            combined['dollar_flow'] = combined['volume'] * combined['lastPrice'] * 100
            
            # Add moneyness relative to current stock price
            current_price = self.get_ticker_info(ticker).get('current_price', 0)
            combined['moneyness'] = combined['strike'] / current_price if current_price > 0 else 0
            
            return combined
            
        except Exception as e:
            print(f"Error fetching options chain for {ticker}: {e}")
            return pd.DataFrame()
    
    def get_options_for_multiple_expirations(self, ticker: str, num_expirations: int = 3) -> pd.DataFrame:
        """Get options data for multiple expiration dates."""
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options[:num_expirations]
            
            all_options = []
            for exp in expirations:
                options_data = self.get_options_chain(ticker, exp)
                if not options_data.empty:
                    all_options.append(options_data)
            
            if all_options:
                return pd.concat(all_options, ignore_index=True)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error fetching multiple expirations for {ticker}: {e}")
            return pd.DataFrame()
    
    def filter_options_data(
        self, 
        df: pd.DataFrame, 
        min_volume: int = 0,
        option_type: Optional[str] = None,
        min_open_interest: int = 0
    ) -> pd.DataFrame:
        """
        Filter options data based on criteria.
        
        Args:
            df: Options DataFrame
            min_volume: Minimum volume threshold
            option_type: 'call', 'put', or None for both
            min_open_interest: Minimum open interest threshold
            
        Returns:
            Filtered DataFrame
        """
        if df.empty:
            return df
        
        filtered = df.copy()
        
        # Filter by volume
        if min_volume > 0:
            filtered = filtered[filtered['volume'] >= min_volume]
        
        # Filter by option type
        if option_type:
            option_type = option_type.lower()
            if option_type in ['call', 'calls']:
                filtered = filtered[filtered['option_type'] == 'call']
            elif option_type in ['put', 'puts']:
                filtered = filtered[filtered['option_type'] == 'put']
        
        # Filter by open interest
        if min_open_interest > 0:
            filtered = filtered[filtered['openInterest'] >= min_open_interest]
        
        return filtered.reset_index(drop=True)
    
    def get_polygon_ticker_info(self, ticker: str) -> Dict[str, Any]:
        """
        Get basic ticker information from Polygon API.
        
        Args:
            ticker: Stock symbol
            
        Returns:
            Dictionary with ticker information
        """
        if not self.config.POLYGON_API_KEY:
            return {'symbol': ticker, 'error': 'POLYGON_API_KEY not set'}
        
        try:
            import time
            
            # Get ticker details
            details_url = f"{self.config.POLYGON_BASE_URL}/v3/reference/tickers/{ticker}"
            details_params = {'apikey': self.config.POLYGON_API_KEY}
            
            details_response = requests.get(details_url, params=details_params)
            
            if details_response.status_code != 200:
                return {'symbol': ticker, 'error': f'Polygon API error: {details_response.status_code}'}
            
            details_data = details_response.json()
            result = details_data.get('results', {})
            
            # Rate limiting
            time.sleep(12)  # 12 seconds between calls for free tier
            
            # Get current price from previous day's data
            price_url = f"{self.config.POLYGON_BASE_URL}/v2/aggs/ticker/{ticker}/prev"
            price_params = {'apikey': self.config.POLYGON_API_KEY}
            
            price_response = requests.get(price_url, params=price_params)
            current_price = 0
            volume = 0
            
            if price_response.status_code == 200:
                price_data = price_response.json()
                results = price_data.get('results', [])
                if results:
                    current_price = results[0].get('c', 0)  # Close price
                    volume = results[0].get('v', 0)  # Volume
            
            return {
                'symbol': ticker,
                'current_price': current_price,
                'market_cap': result.get('market_cap', 0),
                'volume': volume,
                'company_name': result.get('name', ticker)
            }
            
        except Exception as e:
            return {'symbol': ticker, 'error': str(e)}
    
    def get_polygon_options_data(self, ticker: str, expiration: Optional[str] = None) -> pd.DataFrame:
        """
        Get options data from Polygon.io API.
        
        Args:
            ticker: Stock symbol
            expiration: Expiration date (YYYY-MM-DD)
            
        Returns:
            DataFrame with options data
        """
        if not self.config.POLYGON_API_KEY:
            print("Warning: POLYGON_API_KEY not set. Using yfinance as fallback.")
            return self.get_options_chain(ticker, expiration)
        
        try:
            import time
            
            # Get current stock price first
            price_url = f"{self.config.POLYGON_BASE_URL}/v2/aggs/ticker/{ticker}/prev"
            price_params = {'apikey': self.config.POLYGON_API_KEY}
            
            price_response = requests.get(price_url, params=price_params)
            if price_response.status_code == 200:
                price_data = price_response.json()
                current_price = price_data.get('results', [{}])[0].get('c', 0)
            else:
                current_price = 0
            
            # Rate limiting - Polygon free tier allows 5 calls per minute
            time.sleep(12)  # Wait 12 seconds between calls
            
            # Get options contracts
            contracts_url = f"{self.config.POLYGON_BASE_URL}/v3/reference/options/contracts"
            contracts_params = {
                'underlying_ticker': ticker,
                'limit': 1000,
                'apikey': self.config.POLYGON_API_KEY
            }
            
            if expiration:
                contracts_params['expiration_date'] = expiration
            
            contracts_response = requests.get(contracts_url, params=contracts_params)
            
            if contracts_response.status_code != 200:
                print(f"Error fetching contracts: {contracts_response.status_code}")
                return pd.DataFrame()
            
            contracts_data = contracts_response.json()
            contracts = contracts_data.get('results', [])
            
            if not contracts:
                return pd.DataFrame()
            
            # Convert to DataFrame format similar to yfinance
            options_list = []
            
            for contract in contracts[:50]:  # Limit to first 50 to avoid rate limits
                options_list.append({
                    'strike': contract.get('strike_price', 0),
                    'expiration': contract.get('expiration_date', ''),
                    'option_type': 'call' if contract.get('contract_type') == 'call' else 'put',
                    'ticker': contract.get('ticker', ''),
                    'underlying_ticker': contract.get('underlying_ticker', '')
                })
            
            if not options_list:
                return pd.DataFrame()
            
            options_df = pd.DataFrame(options_list)
            
            # Add placeholder data for demo (in production, you'd fetch real market data)
            options_df['volume'] = np.random.randint(10, 1000, len(options_df))
            options_df['openInterest'] = np.random.randint(100, 5000, len(options_df))
            options_df['lastPrice'] = np.random.uniform(0.5, 10.0, len(options_df))
            options_df['dollar_flow'] = options_df['volume'] * options_df['lastPrice'] * 100
            options_df['moneyness'] = options_df['strike'] / current_price if current_price > 0 else 0
            
            return options_df
            
        except Exception as e:
            print(f"Error fetching Polygon data for {ticker}: {e}")
            return pd.DataFrame()
    
    def get_sample_options_data(self, ticker: str) -> pd.DataFrame:
        """
        Generate sample options data for testing when APIs are unavailable.
        
        Args:
            ticker: Stock symbol
            
        Returns:
            DataFrame with sample options data
        """
        import numpy as np
        from datetime import datetime, timedelta
        
        # Generate sample data
        base_price = 100  # Sample base price
        strikes = np.arange(80, 121, 2.5)  # Strikes from 80 to 120
        expirations = [
            (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            (datetime.now() + timedelta(days=21)).strftime('%Y-%m-%d'),
            (datetime.now() + timedelta(days=35)).strftime('%Y-%m-%d')
        ]
        
        sample_data = []
        
        for exp in expirations:
            for strike in strikes:
                for option_type in ['call', 'put']:
                    # Generate realistic-looking random data
                    volume = np.random.randint(0, 500)
                    open_interest = np.random.randint(100, 2000)
                    
                    # Price based on moneyness (simplified)
                    moneyness = strike / base_price
                    if option_type == 'call':
                        base_premium = max(0.1, base_price - strike + np.random.uniform(-5, 5))
                    else:
                        base_premium = max(0.1, strike - base_price + np.random.uniform(-5, 5))
                    
                    last_price = max(0.05, base_premium + np.random.uniform(-2, 2))
                    
                    sample_data.append({
                        'strike': strike,
                        'expiration': exp,
                        'option_type': option_type,
                        'volume': volume,
                        'openInterest': open_interest,
                        'lastPrice': round(last_price, 2),
                        'dollar_flow': volume * last_price * 100,
                        'moneyness': moneyness
                    })
        
        return pd.DataFrame(sample_data)
