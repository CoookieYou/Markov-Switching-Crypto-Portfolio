# Markov-Regime-Switching-Portfolio
Crypto currencies Trading Strategy based on Markov Switching GARCH

Data is from https://www.cryptodatadownload.com/data/gemini/

- Trade on groups of crypto currencies
- Use technical indicators in Random Forest to predict price movements
- Dynamic Allocation based on downside risk predictions

### Specification for the strategy
- trading frequency is hourly
- use all asset data for model training
- model each asset's risk profile separately

### 1. Indicators

* Select from a bunch of technical indicators that illustrate either momentum or volatility
  * Average Directional Index
  * Commodity Channel Index
  * Moving Average Convergence/Divergence
  * Price Momentum
  * Relative Strength Index
  * William's % R
  * On Balance Volume
  * Slope of Linear Regression
  * Return Volatility
  
* Use random forest as a regressor to predict the direction of movements
  * Relative high frequency, so should use non-linear model for more convexity

### 2. MSGARCH Model

The general Markov-Switching GARCH specification can be expressed as: (Ardia et al. 2017 https://doi.org/10.1016/j.ijforecast.2018.05.004.)

$y_t|(s_t = k, F_{t-1}) \sim D(0, h_{k,t}, \delta_k)$

where $D(0, h_{k,t})$, $\delta_k$ is a continuous distribution with a zero mean, time-varying variance $h_{k,t}$ , and additional shape parameters (e.g., asymmetry) gathered in the vector $\delta_k$. $s_t$ is the latent variables that evolves according to an unobserved first-order ergodic homogeneous Markov chain. $F_{t}$ is the filter of information we have by the time $t$.


* Detect Volatility Regime for each instrument
* Predict future volatility as the input of allocation model to replace realized volatility

### 3. Allocation Model

* Rebalance weekly, based on forecast volatility, following minimum variance principle across assets


