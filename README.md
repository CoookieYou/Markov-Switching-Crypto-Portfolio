# Markov-Regime-Switching-Portfolio
Crypto currencies Trading Strategy based on Markov Switching GARCH
Data is from https://www.cryptodatadownload.com/data/gemini/

- Trade on groups of crypto currencies
-Use technical indicators in Random Forest to predict price movements
- Dynamic Allocation based on downside risk predictions

### Specification for the strategy
- trading frequency is hourly
- use all asset data for model training
- model each asset's risk profile separately

### 1. Test Indicators

* Different sets of indicators in different regimes
* Use random forest as a regressor to predict the direction of movements

### 2. MSGARCH Model

* Volatility Regime for each instrument
* Predict future volatility as the input of allocation model

### 3. Allocation Model

* Dynamic Allocation, Risk Parity across assets


