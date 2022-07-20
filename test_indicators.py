# -*- coding: utf-8 -*-
"""
Module for testing indicators

Created on Tue Jul 19 22:12:14 2022

@author: Cookie
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

sns.set_style('darkgrid')

class indicators:
    def __init__(self, ticker, **kwargs):
        '''
        Initialize the class
        '''
        # set up parameters for the indicator
        self.params = {}
        self.params.update(kwargs)
        # test on single ticker
        assert type(ticker) == str, 'Wrong Type of Ticker.'
        self.ticker = ticker
        self.data = None
        self.indicator = None
        self.signals = None
        self.returns = None
    
    def read_data(self, interval, start_date, end_date):
        '''
        get data from Yahoo! Finance
        '''
        tic = yf.Ticker(self.ticker)
        data = tic.history(interval=interval, start_date, end_date)
        
        return data
    
    def indicator_series(self):
        '''
        Over write this function to generate indicator series

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.
        

        '''
        return
    
    def indicator_signals(self, indicator):
        '''
        Generate signals for this indicator

        Parameters
        ----------
        indicator : TYPE
            DESCRIPTION.

        Returns
        -------
        signals: pd.Series
            composed of only 1, 0, -1

        '''
        
        return
    
    def signals_return(self, signals, start, end, mid = False, log = False):
        '''
        Calculate returns

        Parameters
        ----------
        signals : TYPE
            DESCRIPTION.
        log: Boolen
            whether to calculate log return
        mid : Boolen
            whether to use mid price of the bar for return

        Returns
        -------
        r: pd.Series
            the return series
        
        '''
        if not self.data:
            return 'No data to calculate.'
        
        if mid:
            use_data = self.data.close.add(self.data.open).div(2).loc[start:end]
        else:
            use_data = self.data.close.loc[start:end]
            
        if log:
            r = np.log(self.data.close).diff()
        else:
            r = self.data.close.pct_change()
            
        r = signals.loc[start:end].mul(r)
        self.returns = r
        
        return r
    
    def return_distribution(self, start, end, mid = False, log = False):
        '''
        Visulize the distribution of return for each hypothetical trade
        
        start:
            start of the testing period
        end:
            end of the testing period
        Returns
        -------
        the return series of 

        '''
        if not self.signals:
            return 'No signals.'
        
        recalculate = False
        if not self.returns:
            recalculate = True
        elif (self.returns.index[0].strftime("%Y-%m-%d")!=start) | () (self.returns.index[-1].strftime("%Y-%m-%d")!=end):
            recalculate = True
            
        if recalculate:
            r = self.signals_return(self.signals, start, end, mid = False, log = False)
            self.returns = r
            
        signal_diff = self.signals.diff()
        trades = signal_diff.where(signal_diff==0, self.signals).to_frame(name = 'trades')
        trades = trades.where(trades!=0)
        trades['label'] = np.nan
        trades['return'] = self.returns()
        trades.loc[trades.trades!=0] = trades.index.to_series()
        trade_type = trades.groupby('label')['trades'].mean()
        trade_return = trades.groupby('label')['return'].apply(lambda x: x.add(1).cumprod().sub(1).iloc[-1])
        trades = pd.concat([trade_type, trade_return], axis = 1)
        trades.columns = ['type', 'return']
        trades['number'] = np.array(list(range(1, trades.shape[0]+1)))
        
        fig, ax = plt.subplots(figsize = (20, 10))
        sns.scatterplot(x = 'number', y = 'return', hue = 'type', data = trades, ax = ax)
        ax.set_title('Return distribution per trades', fontsize = 15)
        
        return r
        
