import numpy as np
import pandas as pd

from prepare_df import prepare_portfolio_df

def calculate_portfolio_std(weights, std_devs, correlations):
    """
    Calculate the portfolio standard deviation.

    Parameters:
    weights (list or np.array): Weights of the assets in the portfolio.
    std_devs (list or np.array): Standard deviations of the assets.
    correlations (2D list or np.array): Correlation matrix of the assets.

    Returns:
    float: Standard deviation of the portfolio.

    Formula:
    # Portfolio Variance Formula:
    # σ_p^2 = ∑(i=1 to n) ∑(j=1 to n) w_i w_j σ_i σ_j ρ_{ij}
    # Portfolio Standard Deviation:
    # σ_p = √(σ_p^2)
    """
    weights = np.array(weights)
    std_devs = np.array(std_devs)
    correlations = np.array(correlations)

    # Convert standard deviations and correlation matrix to covariance matrix
    covariance_matrix = np.outer(std_devs, std_devs) * correlations
    # print(np.outer(std_devs, std_devs), correlations, covariance_matrix, sep="\n")

    # Calculate portfolio variance
    portfolio_variance = np.dot(weights.T, np.dot(covariance_matrix, weights))
    # print(weights.T)

    # Return portfolio standard deviation
    return np.sqrt(portfolio_variance)

# Example usage
if __name__ == "__main__":
    # Example weights, standard deviations, and correlation matrix
    tickers = {"UUP": 0.25, "JPY=X": 0, "IBIT": .05, "XLU": 0.0, "XLF": 0.0, "XLC":0.0, "XLY":0, "GLD": .20, "SPY": .25, "SHY": .25, "USDCNY=X": 0}
    tickers = {ticker:weight for ticker, weight in tickers.items() if weight > 0}
    print(tickers)
    df = prepare_portfolio_df("2025-01-01", pd.to_datetime("2025-01-14"), tickers)
    # print(df.columns)

    weights = [w for w in tickers.values()]
    sd = []
    for ticker in tickers.keys():
        sd.append(df[ticker+"_pct_change"].std()*np.sqrt(252))

    # print(weights, sd)
    
    tickers_corr = df[[x+"_pct_change" for x in tickers]]
    corr = tickers_corr.corr().values
    # print(type(corr))

    result = calculate_portfolio_std(weights, sd, corr)
    print(f"Portfolio Standard Deviation: {result:.4f}")