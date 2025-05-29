import yfinance as yf

def get_stock_summary(ticker):
    data = {}
    for t in ticker:
        stock = yf.Ticker(t)
        hist = stock.history(period='2d')
        if len(hist) < 2:
            continue
        change = ((hist['Close'].iloc[-1] -hist['Close'].iloc[-2]) /
hist['Close'].iloc[-2]) * 100
        data[ticker] = {
            'name' : stock.info.get('longName',ticker),
            'close' : hist['Close'].iloc[-1],
            'change_percent' : round(change,2)
        }
    return data

if __name__ == '__main__':
    print(get_stock_summary(['TSM','005930.KQ']))
