# agents/analysis_agent.py

def calculate_risk_exposure(portfolio, sector="Asia Tech"):
    """
    portfolio: list of dicts with keys: 'ticker', 'sector', 'value'
    sector: filter for which risk exposure is calculated
    """
    total_value = sum(stock['value'] for stock in portfolio)
    sector_value = sum(stock['value'] for stock in portfolio if stock['sector'] == sector)
    
    if total_value == 0:
        return 0.0
    
    return round((sector_value / total_value) * 100, 2)


def compare_earnings(earnings_data):
    """
    earnings_data: dict like { "TSM": {"actual": 2.5, "estimate": 2.4}, ... }
    Returns percentage surprise
    """
    surprises = {}
    for ticker, values in earnings_data.items():
        actual = values.get("actual")
        estimate = values.get("estimate")
        if actual is not None and estimate is not None:
            diff_pct = round(((actual - estimate) / estimate) * 100, 2)
            surprises[ticker] = diff_pct
    return surprises


if __name__ == "__main__":
    # Simulated data
    sample_portfolio = [
        {"ticker": "TSM", "sector": "Asia Tech", "value": 2200000},
        {"ticker": "005930.KQ", "sector": "Asia Tech", "value": 1800000},
        {"ticker": "AAPL", "sector": "US Tech", "value": 6000000}
    ]

    earnings = {
        "TSM": {"actual": 1.04, "estimate": 1.0},
        "005930.KQ": {"actual": 1.1, "estimate": 1.12}
    }

    exposure = calculate_risk_exposure(sample_portfolio)
    surprises = compare_earnings(earnings)

    print(f"Asia Tech Exposure: {exposure}%")
    print("Earnings Surprises:")
    for k, v in surprises.items():
        print(f"  {k}: {'+' if v >= 0 else ''}{v}%")
