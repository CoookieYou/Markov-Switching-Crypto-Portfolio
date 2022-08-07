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
from scipy.stats import skew, kurtosis

sns.set_style('darkgrid')

class TestIndicators:
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
        data = tic.history(interval, start_date, end_date)
        
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
    
    def trades_stats(self, start, end, mid = False, log = False):
        '''
        Calculate trades statistics

        Returns
        -------
        statistics of trades

        '''
        if not self.signals:
            return 'No signals.'
        
        recalculate = False
        if not self.returns:
            recalculate = True
        elif (self.returns.index[0].strftime("%Y-%m-%d")!=start) | (self.returns.index[-1].strftime("%Y-%m-%d")!=end):
            recalculate = True
            
        if recalculate:
            r = self.signals_return(self.signals, start, end, mid = False, log = False)
            self.returns = r
            
        signal_diff = self.signals.diff()
        trades = signal_diff.where(signal_diff==0, self.signals).to_frame(name = 'trades')
        trades = trades.where(trades!=0)
        trades['label'] = np.nan
        trades['return'] = self.returns()
        trades.loc[trades.trades!=0] = trades.index.to_array()
        trade_type = trades.groupby('label')['trades'].mean()
        trade_return = trades.groupby('label')['return'].apply(lambda x: x.add(1).cumprod().sub(1).iloc[-1])
        trades_detail = pd.concat([trade_type, trade_return], axis = 1)
        trades_detail.columns = ['type', 'return']
        trades_detail['number'] = np.array(list(range(1, trades_detail.shape[0]+1)))
        
        stats = pd.DataFrame(index = ['mean', 'median', 'stddev', 'skewness', 'kurtosis'], 
                             columns = ['short', 'long'])
        stats.loc['mean'] = trades_detail.groupby('type')['return'].mean()
        stats.loc['median'] = trades_detail.groupby('type')['return'].median()
        stats.loc['stddev'] = trades_detail.groupby('type')['return'].std()
        stats.loc['skewness'] = trades_detail.groupby('type')['return'].apply(lambda x: skew(x))
        stats.loc['kurtosis'] = trades_detail.groupby('type')['return'].apply(lambda x: kurtosis(x))
        
        return {'statistics': stats, 
                'details': trades_detail,
                'time_series': trades}
    
    def return_distribution(self, start, end, mid = False, log = False):
        '''
        Visulize the distribution of return for each hypothetical trade
        
        start:
            start of the testing period
        end:
            end of the testing period
        Returns
        -------
        statistics of trades 

        '''
        stats = self.trade_stats(start, end, mid, log)['statistics']
        
        fig, ax = plt.subplots(figsize = (20, 10))
        sns.displot(x = 'return', hue = 'type', data = stats, ax = ax)
        ax.set_title('Return distribution per trades', fontsize = 15)
        
        return stats
    
    def return_beanplot(self, periods, start, end, mid = False, log = False):
        '''
        Visuzlize the return distribution
        with different holding periods

        Returns
        -------
        None.

        '''
        trade_stats = self.trade_stats(start, end, mid, log)
        details = trade_stats['details']
        ts = trade_stats['time_series']
        
        all_returns = []
        
        for period in periods:
            if log:
                return_p = ts['return'].rolling(period).sum().shift(-period).loc[details.index]
            else:
                return_p = ts['return'].rolling(period).apply(lambda x: x.add(1).cumprod().sub(1).iloc[-1]).shift(-period).loc[details.index]
            return_p = return_p.to_frame(name = 'return')
            return_p['period'] = period
            return_p['type'] = details['type']
            
            all_returns.append(return_p)
            
        fig, ax = plt.subplots(figsize = (20, 10))
        sns.violinplot(x = 'period', y = 'return', hue = 'type', data = all_returns, ax = ax)
        ax.set_title('Return distribution in periods')
        
        return
    
        
        
