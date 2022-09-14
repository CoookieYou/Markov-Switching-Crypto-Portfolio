# Markov-Regime-Switching-Portfolio
Crypto currencies Trading Strategy based on Markov Switching GARCH

Data from https://www.cryptodatadownload.com/data/gemini/

- Trade on groups of crypto currencies
- Use technical indicators in Random Forest to predict price movements
- Dynamic Allocation based on downside risk predictions

## Specification for the strategy
- trading frequency is hourly
- use all asset data for model training
- model each asset's risk profile separately

## 1. Sample Features

Use Cusum filter(Lam, K. and H. Yam (1997): “CUSUM techniques for technical trading in financial markets.” 
            Financial Engineering and the Japanese Markets, Vol. 4, pp. 257–274) to sample the data points that observed significant price movements

Train the model with the selected samples.

<img src="https://user-images.githubusercontent.com/60916875/183550956-b68c7858-66b8-4cbd-b216-788c0d0afd55.png" width = "750">

## 2. Indicators

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
  
<img src="https://user-images.githubusercontent.com/60916875/183321818-7e2fd509-469d-44db-b4e6-77ec59ef5819.png" width = "750">

  
* Use random forest as a regressor to predict the direction of movements
  * Relative high frequency, so should use non-linear model for more convexity

## 3. MSGARCH Model

The general Markov-Switching GARCH specification can be expressed as: (Ardia et al. 2017 https://doi.org/10.1016/j.ijforecast.2018.05.004.)

$y_t|(s_t = k, F_{t-1}) \sim D(0, h_{k,t}, \delta_k)$

where $D(0, h_{k,t})$, $\delta_k$ is a continuous distribution with a zero mean, time-varying variance $h_{k,t}$ , and additional shape parameters (e.g., asymmetry) gathered in the vector $\delta_k$. $s_t$ is the latent variables that evolves according to an unobserved first-order ergodic homogeneous Markov chain. $F_{t}$ is the filter of information we have by the time $t$.

An illustration of MSGARCH on SPY: the black line is the probability of being in the high volatility regime

<img src="https://user-images.githubusercontent.com/60916875/183322196-b7c2b678-e552-4159-93ec-cd3b0a81ea14.png" width = "600">

* Detect Volatility Regime for each instrument
* Predict future volatility as the input of allocation model to replace realized volatility

## 4. Allocation Model

* Rebalance weekly, based on forecast volatility, following minimum variance principle across assets

$max_{W} \sum_i \sum_j w_i w_j \sigma_i \sigma_j \rho_{ij}$

$s.t. \sum_i w_i = 1,\quad w_i \ge 0, \quad for i = 1,2,3,...,n$

where $\sigma_i$ are forecast volatilities, which are obtained from the MSGARCH model.

##
See the notebook [here](https://github.com/CoookieYou/Markov-Switching-Crypto-Portfolio/blob/main/backtest.ipynb)

## Reference

[1] Lam, K. and H. Yam (1997): “CUSUM techniques for technical trading in financial markets.” Financial Engineering and the Japanese Markets, Vol. 4, pp. 257–274

[2] David Ardia, Keven Bluteau, Kris Boudt, Leopoldo Catania, "Forecasting risk with Markov-switching GARCH models:A large-scale performance study", International Journal of Forecasting, Volume 34, Issue 4

[3] APA. Lopez de Prado, M. (2018). Advances in financial machine learning, 38-40
