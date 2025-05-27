import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

import datasets
import utils


class EFP(utils.LoggingBase):
    def __init__(self, X, y, h, p_type="OLS-MOSUM", verbosity=0):
        """
        Empirical fluctuation process. For now, only the Ordinary Least Squares MOving
        SUM (OLS-MOSUM) is supported

        :param X: matrix of x-values
        :param y: vector of y
        :param h: bandwidth parameter for the MOSUM process
        :param deg: degree of the polynomial to be fit [0,1]
        :param p_type: process type. Only OLS-MOSUM is supported
        :returns: instance of Empirical Fluctuation Process
        :raises ValueError: wrong type of process
        """
        super().__init__(verbosity)

        if p_type != "OLS-MOSUM":
            raise ValueError("Process type {} is not supported".format(p_type))

        X, y = utils.omit_nans(X, y)
        n, k = X.shape

        self.logger.info("Performing linear regression")
        # fit linear model
        fm = sm.OLS(y, X, missing='drop').fit()

        e = y - fm.predict(exog=X)
        self.logger.debug("Residuals:\n{}".format(e))

        sigma = np.sqrt(np.sum(e**2) / (n - k))
        self.logger.debug("sigma: {}".format(sigma))

        nh = np.floor(n * h)
        self.logger.debug("nh: {}".format(nh))

        e_zero = np.insert(e, 0, 0)

        process = np.cumsum(e_zero)
        self.logger.debug("process1:\n{}".format(process))
        process = process[int(nh):] - process[:(n - int(nh) + 1)]
        self.logger.debug("process2:\n{}".format(process))
        process = process / (sigma * np.sqrt(n))
        self.logger.debug("process3:\n{}".format(process))

        self.coefficients = fm
        self.sigma = sigma
        self.process = process
        self.par = h

    def p_value(self, x, h, k, max_k=6, table_dim=10):
        """
        Returns the p value for the process.

        :param x: result of application of the functional
        :param h: bandwidth parameter
        :param k: number of rows of matrix X
        :returns: p value for the process
        """
        self.logger.info("Calculating p-value")

        k = min(k, max_k)

        crit_table = utils.sc_me[((k - 1) * table_dim):(k * table_dim),:]
        tablen = crit_table.shape[1]
        tableh = np.arange(1, table_dim + 1) * 0.05
        tablep = np.array((0.1, 0.05, 0.025, 0.01))
        tableipl = np.zeros(tablen)

        for i in range(tablen):
            tableipl[i] = np.interp(h, tableh, crit_table[:, i])

        self.logger.debug("Interpolated row of p-values:\n{}".format(tableipl))
        tableipl = np.insert(tableipl, 0, 0)
        tablep = np.insert(tablep, 0, 1)

        p = np.interp(x, tableipl, tablep)

        return(p)

    def sctest(self, functional="max"):
        """
        Performs a generalized fluctuation test.

        :param functional: functional type. Only max is supported
        :raises ValueError: wrong type of functional
        :returns: a tuple of applied functional and p value
        """
        self.logger.info("Performing statistical test")
        if functional != "max":
            raise ValueError("Functional {} is not supported".format(functional))

        h = self.par
        x = self.process
        if (nd := np.ndim(x)) == 1:
            k = nd
        else:
            k = np.shape[0]

        self.logger.info("Calculating statistic")
        stat = np.max(np.abs(x))
        self.logger.debug("stat: {}".format(stat))

        p_value = self.p_value(stat, h, k)
        self.logger.debug("p_value: {}".format(stat))

        return(stat, p_value)


def test_dataset(y, name, h=0.15, level=0.15):
    # x = np.arange(1, y.shape[0] + 1).reshape(y.shape[0], 1)
    x = np.ones(y.shape[0]).reshape(y.shape[0], 1)
    efp = EFP(x, y, h)
    stat, p_value = efp.sctest()

    print("Testing '{}'".format(name))
    if p_value <= level:
        print("Breakpoint detected")
    else:
        print("No breakpoint detected")

    print("p_value", p_value)
    print("stat", stat)
    print()


if __name__ == "__main__":
    # test_dataset(datasets.nhtemp, "nhtemp")
    test_dataset(datasets.nile, "nile")


