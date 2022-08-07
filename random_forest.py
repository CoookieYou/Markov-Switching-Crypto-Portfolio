# -*- coding: utf-8 -*-
"""
Random Forest Regressor for Ensembling Indicators

Created on Sat Jul 23 16:16:55 2022

@author: Cookie
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from tqdm import tqdm

class random_forest:
    def one_fold_RF(self, indicators, returns, **kwargs):
        '''
        One-fold training

        Parameters
        ----------
        indicators : TYPE
            DESCRIPTION.
        returns : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        regr : TYPE
            DESCRIPTION.

        '''
        assert indicators.shape[0] == returns.shape[0], 'incompatile shapes.'
        
        RF = RandomForestRegressor(kwargs)
        regr = RF.fit(indicators, returns)
        
        return regr
    
    def rolling_RF(self, indicators, returns, window, train, test, opt = False, **kwargs):
        '''
        Rolling training and testing

        Parameters
        ----------
        indicators : TYPE
            DESCRIPTION.
        returns : TYPE
            DESCRIPTION.
        window : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        RandomForestRegressor object

        '''
        assert indicators.shape[0] == returns.shape[0], 'incompatile shapes.'
        
        n = np.ceiling(returns.shape[0]/window)
        pred_y = []
        for i in tqdm(range(n-1), 'Rolling Random Forest...'):
            training_x = indicators.iloc[(i)*window: (train+i)*window]
            training_y = returns.iloc[(i)*window: (train+i)*window]
            testing_x = indicators.iloc[(i+train)*window: min((i+train+test)*window, indicators.shape[0])]
            
            RF_i = self.one_fold_RF(training_x, training_y, kwargs)
            y_i = RF_i.predict(testing_x)
            pred_y.append(y_i)
            
        pred_y = pd.Series(np.vstack(pred_y), index = indicators.index[window:], name = 'prediction')
        
        return pred_y
    
    def optimize_RF(self, indicators, returns, params, cv, **kwargs):
        '''
        Optimize in-sample Random Forest Parameters

        Parameters
        ----------
        indicators : TYPE
            DESCRIPTION.
        returns : TYPE
            DESCRIPTION.
        params : TYPE
            DESCRIPTION.
        cv : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        assert indicators.shape[0] == returns.shape[0], 'incompatile shapes.'
        
        n = indicators.shape[0]
        train_idx = list(range(cv))
        valid_idx = list(range(cv, n))
        custom_cv = zip(train_idx, valid_idx)
        
        search = GridSearchCV(RandomForestRegressor, param_grid = params, cv = custom_cv, **kwargs)
        res_search = search.fit(indicators, returns)
        
        return res_search
        
        
        
            
