# -*- coding: utf-8 -*-
"""
Portfolio Optimization with CVXPY

Created on Thu Aug  4 20:56:31 2022

@author: Cookie
"""

import pandas as pd
import numpy as np
import cvxpy as cvx

class portfolio_optimizer:
    def __init__(self, mode = 'MVP'):
        self.mode = mode        # default: minimum-variance portfolio
        
    def getCovMat(self, r):
        '''
        Geneate covariance matrix from return series

        Parameters
        ----------
        r : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        cov_mat = ((r.std().values.reshape(-1,1) @ r.std().values.reshape(-1,1).T) * r.corr().values)
        
        return cov_mat
        
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
        
        objective = cvx.Minimize(cvx.quad_form(x, cov_mat))
        constraints = [0 <= x, x <= 1, cvx.sum(x) == 1]
        problem = cvx.Problem(objective, constraints)
        
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
            beta[i] = np.polyfit(historical.iloc[:, i], market, deg = 1)[0]
            
        weights = 1/beta
        weights = weights/np.sum(weights)
        
        return weights
        


"""For debug
if __name__ == "__main__":
    opt = portfolio_optimizer().mvp(cov_mat = np.array([[1, .2, .3], [.2, 1, .25], [.3, .25, 1]]))
    print(opt)
"""