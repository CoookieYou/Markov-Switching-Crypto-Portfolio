# -*- coding: utf-8 -*-
"""
Data Management and Sampling features

Created on Thu Aug  4 20:30:29 2022

@author: Cookie
"""

import pandas as pd
import numpy as np
import os

class data_manager:
    '''
    A class for data management
    '''
    def __init__(self, datadir = r"D:\Career\Quant\My_Research\Markov_Switching_Portfolio\cryptodatadownload"):
        # hourly crypto data dirctory
        self.datadir = datadir
        
    def readPair(self, pairs, start, end, fields = ['open', 'high', 'low', 'close', 'volume']):
        '''
        Read the pairs data

        Parameters
        ----------
        pairs : str
            A string contains all the pairs.
        start: str
            start date
        end: str
            end date

        Returns
        -------
        pairs_df: pandas dataframe
            all data groupby pairs' names

        '''
        pairs_list = pairs.split(' ')
        pairs_df = {}
        
        for pair in pairs_list:
            pairs_df[pair] = pd.read_csv(os.path.join(self.datadir, f"Gemini_{pair}_1h.csv"),
                                         skiprows = 1, index_col = 1, parse_dates = True)
            pairs_df[pair].sort_index(inplace = True)
            pairs_df[pair] = pairs_df[pair].loc[start:end]
            if 'volume' in fields:
                pairs_df[pair] = pairs_df[pair].rename(columns = {f'Volume {pair[:-3]}': 'volume'})
            pairs_df[pair] = pairs_df[pair][fields]
            
        pairs_df = pd.concat(pairs_df, axis = 0)
        print('Pairs: ', pairs_list)
        
        return pairs_df
    
    def cusumFilter(self, r, h):
        '''
        Cusum Filter for sampling data points
        
        Reference:
        [1] APA. Lopez de Prado, M. (2018). Advances in financial machine learning, 38-40
        [2] Lam, K. and H. Yam (1997): “CUSUM techniques for technical trading in financial markets.” 
            Financial Engineering and the Japanese Markets, Vol. 4, pp. 257–274

        Parameters
        ----------
        data : pandas series or dataframe
            price used in calculating returns for all assets
        h:
            threshold for 

        Returns
        -------
        samples: dictionary of pandas index
            contains index of all the sample data points for all assets

        '''
        
        # r = data.pct_change().iloc[1:]
        
        samples = {}
        
        for ticker in r.columns:
            idx = self.getTEvents(r[ticker], h)
            samples[ticker] = pd.DatetimeIndex(idx)
            
        return samples
        
        
    def getTEvents(self, gRaw, h):
        '''
        Cusum Filter for single time-series
        
        see:
            APA. Lopez de Prado, M. (2018). Advances in financial machine learning, Page 39

        Parameters
        ----------
        gRaw : pandas series
            raw return series
        h : float
            threshold for sampling

        Returns
        -------
        list of index of the events

        '''
        tEvents,sPos,sNeg=[],0,0
        diff=gRaw.diff()
        
        for i in diff.index[1:]:
            sPos,sNeg=max(0,sPos+diff.loc[i]),min(0,sNeg+diff.loc[i])
        
            if sNeg<-h:
                sNeg=0
                tEvents.append(i)
            elif sPos>h:
                sPos=0
                tEvents.append(i)
            
        return pd.DatetimeIndex(tEvents)
        


"""For debug
if __name__ == '__main__':
    data = data_manager().readPair(pairs = "BTCUSD ETHUSD BATUSD FILUSD MKRUSD UNIUSD ZRXUSD",
                               start='2020-11-01', end='2021-12-31')
    btc_close = data.loc['BTCUSD'].close.to_frame(name = 'BTCUSD')
    cusum = data_manager().cusumFilter(btc_close, .01)
    print(cusum['BTCUSD'], btc_close.head(10).pct_change())
"""