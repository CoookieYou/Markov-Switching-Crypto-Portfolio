# -*- coding: utf-8 -*-
"""
Data Management and Sampling features

Created on Thu Aug  4 20:30:29 2022

@author: Cookie
"""

import pandas as pd
import numpy as np
import datatable as dt
import os

class data_manager:
    '''
    A class for data management
    '''
    def __init__(self):
        # hourly crypto data dirctory
        self.datadir = r"D:\Career\Quant\My_Research\Markov_Switching_Portfolio\cryptodatadownload"
        
    def readPair(self, pairs, start, end, fields = ['open', 'high', 'low', 'close', 'Volume']):
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
        pairs_list = pairs.split('_')
        pairs_df = {}
        
        for pair in pairs_list:
            pairs_df[pair] = pd.read_csv(os.join(self.datadir, f"Gemini_{pair}_1h.csv"),
                                         skiprows = 1, index_col = 1, parse_dates = True)
            pairs_df[pair] = pairs_df[pair].loc[start:end]
            if 'Volume' in fields:
                pairs_df[pair] = pairs_df[pair].rename({f'Volume_{pair[:-3]}': 'Volume'})
            pairs_df[pair] = pairs_df[fields]
            
        pairs_df = pd.concat(pairs_df, axis = 0)
        print('Pairs: ', pairs_list)
        
        return pairs_df
        
        