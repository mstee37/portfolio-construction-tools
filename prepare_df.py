import yfinance as yf
import pandas as pd
from pandas.tseries.offsets import BusinessDay

def prepare_portfolio_df(start, end, tickers, base=1000):
    """
    Prepares a portfolio DataFrame with percentage changes, cumulative returns,
    and portfolio value given tickers, weights, and initial total investment.

    Parameters:
        start (datetime): Start date for data retrieval.
        end (datetime): End date for data retrieval.
        tickers (list): List of stock tickers.
        weights (dict): Dictionary with tickers as keys and weights as values.
        total (float): Initial portfolio value. Default is 1,000,000.

    Returns:
        pd.DataFrame: DataFrame with portfolio value and other metrics.
    """
    if not tickers:
        raise ValueError("Tickers list cannot be empty.")

    if sum(abs(x) for x in tickers.values()) > 1:
        raise ValueError("total of weight > 1")
    
    # Initialize an empty DataFrame
    df = pd.DataFrame(index=pd.bdate_range(start=start, end=end-BusinessDay(1)))

    # Download data and calculate percentage changes
    for ticker in tickers.keys():
        curr = yf.download(ticker, start=start, end=end)
        curr.columns = curr.columns.get_level_values(0)
        # df = pd.concat([df, curr[["Close"]]],axis=1).ffill().bfill()
        curr.rename(columns={"Close": ticker+"_Close"}, inplace=True)
        df = df.merge(curr[[ticker+"_Close"]], left_index=True, right_index=True, how="left").ffill().bfill()

    # print(df.columns)
    for ticker in tickers.keys():
        column_name = ticker+'_Close'
        df[ticker+"_pct_change"] = df[column_name].pct_change().fillna(0)

    # Calculate portfolio percentage change
    df["pf_pct_change"] = sum(
        df[ticker + "_pct_change"] * tickers[ticker] for ticker in tickers.keys()
    )

    # # Calculate cumulative returns and portfolio value
    df["cumulative_returns"] = (1 + df["pf_pct_change"]).cumprod()
    df["pf_val"] = base * df["cumulative_returns"]

    return df