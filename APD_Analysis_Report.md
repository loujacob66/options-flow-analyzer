# Options Flow Analysis Report: APD (Air Products & Chemicals)

**Generated on:** June 28, 2025  
**Analysis Tool:** Options Flow Analyzer  
**Data Source:** Polygon.io API  

---

## 📊 Stock Information

- **Company:** Air Products & Chemicals, Inc.
- **Symbol:** APD
- **Current Price:** $282.35
- **Volume:** 2,433,377 shares
- **Market Cap:** $60,198,209,887

---

## 🎯 Options Flow Summary

| Metric | Calls | Puts | Net |
|--------|-------|------|-----|
| **Volume** | 14,742 | 10,516 | 4,226 |
| **Dollar Flow** | $8,543,240 | $5,844,979 | $2,698,261 |

### Key Metrics
- **Put/Call Ratio:** 0.71
- **Total Contracts Analyzed:** 50
- **Market Sentiment:** 🟢 **Bullish** (Net positive dollar flow toward calls)

---

## 📈 Top Strikes by Volume

| Strike | Type | Volume | Open Interest | Dollar Flow | Distance % | ITM/OTM |
|--------|------|--------|---------------|-------------|------------|---------|
| $260 | PUT | 999 | 938 | $603,100 | -7.9% | OTM |
| $200 | PUT | 972 | 2,591 | $871,212 | -29.2% | OTM |
| $185 | CALL | 969 | 4,332 | $791,946 | -34.5% | ITM |
| $220 | PUT | 968 | 2,042 | $568,762 | -22.1% | OTM |
| $195 | CALL | 936 | 576 | $368,287 | -30.9% | ITM |
| $290 | CALL | 931 | 2,711 | $479,026 | +2.7% | OTM |
| $350 | CALL | 931 | 2,489 | $219,303 | +24.0% | OTM |
| $340 | CALL | 899 | 1,561 | $809,985 | +20.4% | OTM |
| $230 | CALL | 859 | 570 | $688,785 | -18.5% | ITM |
| $280 | CALL | 841 | 188 | $331,733 | -0.8% | ITM |
| $175 | CALL | 780 | 4,259 | $230,511 | -38.0% | ITM |
| $180 | PUT | 707 | 4,675 | $417,749 | -36.2% | OTM |
| $190 | PUT | 703 | 3,598 | $39,278 | -32.7% | OTM |
| $320 | CALL | 694 | 4,767 | $478,981 | +13.3% | OTM |
| $270 | CALL | 642 | 1,038 | $315,243 | -4.4% | ITM |

---

## 🚨 Unusual Activity Alert

**High Volume/Open Interest Ratio Detected:**

| Strike | Type | Expiration | Volume | Open Interest | Vol/OI Ratio | Dollar Flow |
|--------|------|------------|--------|---------------|--------------|-------------|
| **$280** | **CALL** | **2025-07-18** | **841** | **188** | **4.4x** | **$331,733** |

⚠️ **Notable:** This $280 call option shows unusually high volume relative to open interest, suggesting potential new positioning or significant interest at this strike level.

---

## 🎯 Max Pain Analysis

**Max Pain Strike:** $190  
*(Strike with highest total open interest)*

### Open Interest Distribution

| Strike | Open Interest | Volume |
|--------|---------------|--------|
| $190 | 8,526 | 1,143 |
| $180 | 8,520 | 775 |
| $185 | 8,277 | 1,143 |
| $175 | 7,485 | 1,263 |
| $320 | 7,401 | 1,189 |
| $330 | 7,176 | 262 |
| $200 | 6,724 | 1,301 |
| $165 | 6,562 | 1,005 |
| $195 | 4,732 | 1,279 |
| $220 | 4,703 | 1,239 |

---

## 🔍 Analysis Summary

### Bullish Indicators:
- **Net call flow advantage:** $2.7M more in call dollar flow than puts
- **Strong call activity:** Multiple high-volume calls at various strikes
- **OTM call interest:** Significant activity in $290+ calls suggests bullish outlook

### Key Observations:
1. **Current Price Position:** At $282.35, the stock is trading near several active strike levels
2. **Put Protection:** Heavy put activity around $200-$260 suggests downside protection
3. **Upside Targets:** Call activity concentrated around $290, $320, $340, and $350 strikes
4. **Max Pain:** At $190, significantly below current price, suggesting potential downward pressure from options positioning

### Risk Considerations:
- High concentration of open interest at lower strikes could create downward pressure
- Unusual activity in $280 calls warrants monitoring for potential breakout or breakdown

---

*This analysis is based on options flow data and should be used for informational purposes only. Not investment advice.*

**Tool Info:** Generated using Options Flow Analyzer - a Python CLI tool for analyzing options market activity. Real market data provided by Polygon.io API.
