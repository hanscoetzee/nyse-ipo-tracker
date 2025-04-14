import finnhub
import pandas as pd
from datetime import date

# Initialize Finnhub Client
api_key = 'cvqk991r01qp88cm78e0cvqk991r01qp88cm78eg'
finnhub_client = finnhub.Client(api_key=api_key)

def get_upcoming_ipos():
    try:
        # Get today's date
        today = date.today().isoformat()

        # Fetch IPO calendar data
        ipo_data = finnhub_client.ipo_calendar(_from=today, to=today)

        # Extract the IPO details
        ipos = ipo_data.get("ipoCalendar", [])

        # Check if data is available
        if not ipos:
            print("No upcoming IPOs found.")
            return []

        data = []
        for ipo in ipos:
            company = ipo.get('name', 'N/A')
            symbol = ipo.get('symbol', 'N/A')
            ipo_date = ipo.get('date', 'N/A')
            shares = ipo.get('numberOfShares', 'N/A')
            exchange = ipo.get('exchange', 'N/A')
            price = ipo.get('price', 'N/A')
            status = ipo.get('status', 'N/A')

            data.append([company, symbol, ipo_date, shares, exchange, price, status])

        # Save the IPO data to a CSV file
        df = pd.DataFrame(data, columns=['Company', 'Symbol', 'IPO Date', 'Shares', 'Exchange', 'Price', 'Status'])
        df.to_csv('nasdaq_ipos.csv', index=False)
        print("Data saved to nasdaq_ipos.csv")
        return data

    except Exception as e:
        print(f"Error fetching IPO data: {e}")
        return []
