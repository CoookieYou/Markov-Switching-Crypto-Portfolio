# -*- coding: utf-8 -*-
"""
Portfolio Optimization with CVXPY

Created on Thu Aug  4 20:56:31 2022

@author: Cookie
"""

import pandas as pd
import numpy as np
import CVXPY as cvx

class portfolio_optimizer:
    def __init__(self, mode = 'MVP'):
        self.mode = mode        # default: minimum-variance portfolio
        
    def mvp(self, cov_mat):
        '''
        Minimum-Variance Portfolio

        Parameters
        ----------
        cov_mat : numpy array
            covariance matrix

        Returns
        -------
        weights:
            optimal portfolio weights

        '''
        n = cov_mat.shape[1]
        x = cvx.Variable(n)
        objective = cvx.Minimize(cvx.sum_squares(x @ cov_mat @ x.t))
        constraints = [0 <= x, x <= 1]
        problem = cvx.Problem(objective, contraints)
        
        results = problem.solve()
        weights = x.value
        
        return weights
    
    def ERC(self, historical, market):
        '''
        Equal Risk Contribution Portfolio

        Parameters
        ----------
        historical : pandas dataframe
            Historical return series
        market: pandas dataframe
            Market Portfolio return series

        Returns
        -------
        weights:
            optimal portfolio weights

        '''
        if historical.shape[0] != market.shape[0]:
            return "Incompatible data shapes."
        
        beta = np.ones(shape = (historical.shape[1]))
        for i in range(historical.shape[1]):
            beta[i] = np.polyfit(historical,iloc[:, i], market, deg = 1)[0]
            
        weights = 1/beta
        weights = weights/np.sum(weights)
        
        return weights
        
