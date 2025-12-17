import streamlit as st
import requests
import pandas as pd
import statsmodels.api as sm
import plotly.express as px
from datetime import datetime


BTC_URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=120"
ETH_URL = "https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1m&limit=120"
ROLLING_WINDOW = 20
Z_THRESHOLD = 2.0

st.set_page_config(page_title="BTC–ETH Stat Arb", layout="wide")
st.title(" Live BTC–ETH Statistical Arbitrage Dashboard")

@st.cache_data(ttl=10)
def fetch_prices():
    btc = requests.get(BTC_URL).json()
    eth = requests.get(ETH_URL).json()

    btc_df = pd.DataFrame(btc, columns=[
        "time","o","h","l","c","v","ct","qv","n","tb","tq","ig"
    ])
    eth_df = pd.DataFrame(eth, columns=btc_df.columns)

    btc_df["time"] = pd.to_datetime(btc_df["time"], unit="ms")
    eth_df["time"] = pd.to_datetime(eth_df["time"], unit="ms")

    btc_df["btcusdt"] = btc_df["c"].astype(float)
    eth_df["ethusdt"] = eth_df["c"].astype(float)

    df = btc_df[["time","btcusdt"]].merge(
        eth_df[["time","ethusdt"]],
        on="time"
    ).set_index("time")

    return df

prices = fetch_prices()


y = prices["btcusdt"]
x = sm.add_constant(prices["ethusdt"])
model = sm.OLS(y, x).fit()
hedge_ratio = model.params["ethusdt"]

prices["hedge_spread"] = prices["btcusdt"] - hedge_ratio * prices["ethusdt"]
prices["z_score"] = (
    (prices["hedge_spread"] - prices["hedge_spread"].rolling(ROLLING_WINDOW).mean()) /
    prices["hedge_spread"].rolling(ROLLING_WINDOW).std()
)

latest_z = prices["z_score"].iloc[-1]


c1, c2, c3 = st.columns(3)
c1.metric("Hedge Ratio (Beta)", round(hedge_ratio, 4))
c2.metric("Latest Z-Score", round(latest_z, 3))
c3.metric(
    "Alert",
    "🚨 ALERT" if abs(latest_z) > Z_THRESHOLD else "Normal"
)


st.subheader("BTC vs ETH Prices")
st.plotly_chart(
    px.line(prices, y=["btcusdt", "ethusdt"]),
    use_container_width=True
)

st.subheader("Hedge Spread")
st.plotly_chart(
    px.line(prices, y="hedge_spread"),
    use_container_width=True
)

st.subheader("Z-Score")
st.plotly_chart(
    px.line(prices, y="z_score"),
    use_container_width=True
)

st.caption(f"Last updated: {datetime.utcnow().strftime('%H:%M:%S')} UTC")
