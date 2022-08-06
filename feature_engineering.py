# -*- coding: utf-8 -*-
"""
Calculate indicators and feature engineering

Created on Sat Aug  6 14:07:18 2022

@author: Cookie
"""

import pandas as pd
import numpy as np
from talib import *
from tqdm import tqdm

class Indicators:
    '''
    Calculare Technical Indicators used to predict returns
    '''

    self.TAdict = {'ADX': self.adx, 'CCI': self.cci, 'MACD': self.macd_hist,
                   'MOM': self.mom, 'RSI': self.rsi, 'FastK': self.fastk,
                   'WILLR': self.willr, 'OBV': self.obv, 'AD': self.adline, 
                   'ATR': self.natr, 'BlackCrows': self.tblackcrows, 
                   'Inside': self.tinside, 'Beta': self.beta, 
                   'Regression': self.linregslope, 'Volatility': self.vol}
    
    def adx(self, data, window = 14):
        '''Calculate Average Directional Index
        data:
            HCL dataframe
        '''
        adx = ADX(data.high, data.low, data.close, window)
        
        return adx
    
    def cci(self, data, window = 14):
        '''Calculate Commodity Channel Index
        data:
            HCL dataframe
        '''
        cci = CCI(data.high, data.low, data.close, window)
        
        return cci
        
    def macd_hist(self, data, fast = 12, slow = 26, signal = 9):
        '''Caculate MACD histogram
        '''
        _, _, macd_hist = MACD(data.close, fast, slow, signal)
        
        return macd_hist
    
    def mom(self, data, window = 10):
        '''Calculate momentum
        '''
        mom = MOM(data.close, window)
        
    def rsi(self, data, window = 14):
        '''Calculate Raletive Strength Index
        '''
        rsi = RSI(data.lose, window)
        
        return rsi
    
    def fastk(self, data, k = 5, d = 3):
        '''Calculate stochastic fast K
        data:
            HCL dataframe
        '''
        fastk, _ = STOCHF(data.high, data.low, data.close, k, d)
        
        return fastk
    
    def willr(self, data, window = 14):
        '''Calculate William's %R
        data:
            HCL dataframe
        '''
        willr = WILLR(data.high, data.low, data.close, window)
        
        return willr
    
    def obv(self, data):
        '''Calculate On-balance-volume
        data:
            close & volume
        '''
        obv = OBV(data.close, data.volume)
        
        return obv
    
    def adline(self, data, volume):
        '''Calculate A/D line
        '''
        adline = AD(data.high, data.low, data.close, volume)
        
        return adline
    
    def natr(self, data, window = 14):
        '''Calculate Normalized Average True Range
        '''
        natr = NATR(data.high, data.low, data.close, window)
        
        return natr

    def tblackcrows(self, data):
        '''Pattern recognition: three black crows
        '''
        tbc = CDL3BLACKCROWS(data.open, data.high, data.low, data.close)
        
        return tbc
    
    def tinside(self, data):
        '''Pattern recognition: three inside up/down
        '''
        tin = CDL3INSIDE(data.open, data.high, data.low, data.close)
        
        return tin
    
    def beta(self, data, window = 5):
        '''Beta between high and low
        '''
        beta = BETA(data.high, data.low, window)
        
    def linregslope(self, data, window = 14):
        '''Linear regression slope
        '''
        slope = LINEARREG_SLOPE(data.close, window)
        
        return slope
    
    def vol(self, data, window = 5, nbdev = 1):
        '''Volatility
        '''
        vol = STDDEV(data.close, window, nbdev)
        
    def pool(self, data, params):
        '''Calculate a pool of indicators
        data:
            OHCL dataframe
        params: dictionary
            contains the names of indicators and their parameters
        '''
        
        ind = pd.DataFrame(index = data.index, columns = list(params.keys()))
        for ta in params:
            ind[ta] = self.TAdict[ta](data, params[ta])
            
        return ind
        
        
        
        
        
    
    
    

