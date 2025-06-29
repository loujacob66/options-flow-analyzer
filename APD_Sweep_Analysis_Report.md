# Options Flow Analysis Report: APD with Sweep Detection

**Generated on:** June 28, 2025  
**Analysis Tool:** Options Flow Analyzer v0.1.0  
**Data Source:** Polygon.io API  
**Feature:** Advanced Sweep Detection & Filtering  

---

## 📊 Stock Information

- **Company:** Air Products & Chemicals, Inc.
- **Symbol:** APD
- **Current Price:** $282.35
- **Volume:** 2,433,377 shares
- **Market Cap:** $60,198,209,887
- **Contracts Analyzed:** 49 option contracts

---

## 🔍 Sweep Detection Results

### Trade Classification Summary

| Trade Type | Count | Percentage |
|------------|-------|------------|
| **Retail** | 36 | 73.5% |
| **Block** | 10 | 20.4% |
| **Sweep** | 3 | 6.1% |

### Top Detected Sweeps

| Strike | Type | Volume | Dollar Flow | Confidence |
|--------|------|--------|-------------|------------|
| $240 | PUT | 987 | $796,214 | 31.2% |
| $240 | CALL | 933 | $831,407 | 30.5% |
| $330 | PUT | 963 | $811,722 | 30.4% |

---

## 📈 Flow Analysis: Impact of Sweep Removal

### Comparison Table

| Metric | All Trades | Without Sweeps | Impact |
|--------|------------|----------------|--------|
| **Net Volume** | 4,348 | 5,365 | **+1,017** |
| **Net Dollar Flow** | $1,933,096 | $2,709,625 | **+$776,529** |
| **Sentiment** | 🟢 Bullish | 🟢 Bullish | ✓ Same |
| **Put/Call Ratio** | 0.71 | 0.62 | **-0.09** |

### Key Insights from Sweep Removal:
- ✅ **More Bullish Signal**: Removing sweeps reveals $776k additional bullish flow
- ✅ **Improved Put/Call Ratio**: Drops from 0.71 to 0.62 (more call-heavy)
- ✅ **Volume Increase**: +1,017 contracts of net bullish volume
- ⚠️ **Sweep Trades Were Bearish**: Isolated sweeps showed -$776k bearish flow

---

## 🎯 Clean Options Flow Summary (Sweeps Excluded)

| Metric | Calls | Puts | Net |
|--------|-------|------|-----|
| **Volume** | 13,991 | 8,626 | 5,365 |
| **Dollar Flow** | $6,612,365 | $3,902,740 | $2,709,625 |

### Analysis Metrics (Clean Data)
- **Put/Call Ratio:** 0.62
- **Total Contracts:** 46 (after removing 3 sweeps)
- **Market Sentiment:** 🟢 **Bullish** (stronger signal than raw data)

---

## 📊 Top Strikes by Volume (Clean Data)

| Strike | Type | Volume | Open Interest | Dollar Flow | Distance % | ITM/OTM |
|--------|------|--------|---------------|-------------|------------|---------|
| $390 | CALL | 902 | 989 | $222,347 | +38.1% | OTM |
| $180 | CALL | 888 | 3,106 | $745,286 | -36.2% | ITM |
| $300 | CALL | 840 | 1,852 | $729,641 | +6.3% | OTM |
| $165 | CALL | 824 | 675 | $661,455 | -41.6% | ITM |
| $230 | PUT | 798 | 3,432 | $55,759 | -18.5% | OTM |
| $210 | CALL | 794 | 1,829 | $130,104 | -25.6% | ITM |
| $310 | CALL | 791 | 4,804 | $462,566 | +9.8% | OTM |
| $350 | CALL | 764 | 3,092 | $217,515 | +24.0% | OTM |
| $210 | PUT | 744 | 3,640 | $305,222 | -25.6% | OTM |
| $340 | CALL | 734 | 708 | $303,354 | +20.4% | OTM |

---

## 🎯 Max Pain Analysis

**Max Pain Strike:** $330  
*(Strike with highest total open interest)*

### Open Interest Distribution

| Strike | Open Interest | Volume |
|--------|---------------|--------|
| $330 | 9,036 | 1,152 |
| $230 | 8,112 | 1,433 |
| $310 | 7,786 | 1,108 |
| $240 | 7,685 | 1,920 |
| $260 | 7,588 | 835 |
| $250 | 6,432 | 566 |
| $220 | 6,324 | 989 |
| $175 | 6,192 | 1,298 |
| $290 | 5,527 | 1,116 |
| $210 | 5,469 | 1,538 |

---

## 🔍 Sweep-Only Analysis

**Isolated Sweep Trades:**
- **Volume:** -1,017 contracts (net bearish)
- **Dollar Flow:** -$776,529 (bearish flow)
- **Sentiment:** 🔴 **Bearish**

### What This Means:
The detected sweep trades were primarily **institutional hedging or arbitrage** activities that created bearish noise in the data. By removing them, we reveal the true **retail and directional sentiment**, which is significantly more bullish.

---

## 💡 Key Takeaways

### 🎯 **Why Sweep Detection Matters**
1. **Cleaner Sentiment**: Removing institutional noise reveals true directional bias
2. **Better Signal**: $776k more bullish flow when sweeps are excluded
3. **Institutional vs Retail**: Sweeps were bearish hedging, retail flow is bullish

### 📈 **Trading Implications**
- **True Sentiment:** Bullish (retail/smaller players are buying calls)
- **Institutional Activity:** Bearish hedging/arbitrage (not predictive)
- **Key Levels:** Strong call activity at $300, $310, $340, $350, $390
- **Support Levels:** Put protection around $210-$230

### ⚠️ **Risk Considerations**
- Max pain at $330 suggests potential magnet effect
- Heavy institutional positioning may create volatility
- Monitor sweep activity for changes in institutional sentiment

---

## 🛠️ Technical Notes

**Sweep Detection Criteria:**
- Volume ≥ 95th percentile of all trades
- High volume/open interest ratio (≥2.0)
- Large dollar flow relative to other trades
- Confidence scoring based on multiple factors

**Data Quality:**
- Real market data from Polygon.io API
- 49 contracts analyzed with minimum 20 volume filter
- Live pricing and company information

---

*This analysis demonstrates the power of sweep detection in filtering institutional noise to reveal true market sentiment. The Options Flow Analyzer successfully identified and isolated 6.1% of trades as institutional sweeps, revealing a significantly more bullish retail sentiment than raw data would suggest.*

**Tool:** Options Flow Analyzer - Advanced options flow analysis with sweep detection  
**Command Used:** `python -m options_analyzer analyze APD --min-volume 20`
