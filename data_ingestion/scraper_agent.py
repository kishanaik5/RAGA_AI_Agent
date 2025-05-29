# data_ingestion/scraper_agent.py
import requests
from bs4 import BeautifulSoup

def fetch_yahoo_earnings_news(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Failed to retrieve data for {ticker}"

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3')

    news_items = []
    for h in headlines[:5]:  # Fetch top 5
        a_tag = h.find('a')
        if a_tag and a_tag.text:
            news_items.append(a_tag.text.strip())

    return {
        "ticker": ticker,
        "top_headlines": news_items
    }

if __name__ == "__main__":
    result = fetch_yahoo_earnings_news("TSM")  # Example: TSMC
    print(result)
