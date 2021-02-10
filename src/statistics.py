from scipy import stats
from functools import partial
import numpy as np
import matplotlib.pyplot as plt


# code adapted from : https://docs.scipy.org/doc/scipy/reference/tutorial/stats.html


def my_kde_bandwidth(obj, fac=1./5):
    """We use Scott's Rule, multiplied by a constant factor."""
    return np.power(obj.n, -1./(obj.d+4)) * fac


def bimodal(data):
    x1 = np.array(data, dtype=np.float64)
    kde1 = stats.gaussian_kde(x1)
    kde2 = stats.gaussian_kde(x1, bw_method='silverman')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x1, np.zeros(x1.shape), 'b+', ms=20)  # rug plot
    x_eval = np.linspace(-10, 10, num=200)
    ax.plot(x_eval, kde1(x_eval), 'k-', label="Scott's Rule")
    ax.plot(x_eval, kde2(x_eval), 'r-', label="Silverman's Rule")
    plt.show()




    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x1, np.zeros(x1.shape), 'b+', ms=20)  # rug plot
    kde3 = stats.gaussian_kde(x1, bw_method=my_kde_bandwidth)
    ax.plot(x_eval, kde3(x_eval), 'g-', label="With smaller BW")
    plt.show()

    loc1, scale1, size1 = (80, 2, 175)
    loc2, scale2, size2 = (30, 2, 150)
    x2 = np.array(data)

    x_eval = np.linspace(x2.min() - 1, x2.max() + 1, 500)
    kde = stats.gaussian_kde(x2)
    kde2 = stats.gaussian_kde(x2, bw_method='silverman')
    kde3 = stats.gaussian_kde(x2, bw_method=partial(my_kde_bandwidth, fac=0.2))
    kde4 = stats.gaussian_kde(x2, bw_method=partial(my_kde_bandwidth, fac=0.5))

    pdf = stats.norm.pdf
    bimodal_pdf = pdf(x_eval, loc=loc1, scale=scale1) * float(size1) / x2.size + \
              pdf(x_eval, loc=loc2, scale=scale2) * float(size2) / x2.size

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    #pdf probabiliti density function
    ax.plot(x2, np.zeros(x2.shape), 'b+', ms=12)
    ax.plot(x_eval, kde(x_eval), 'k-', label="Scott's Rule")
    #ax.plot(x_eval, kde2(x_eval), 'b-', label="Silverman's Rule")
    #ax.plot(x_eval, kde3(x_eval), 'g-', label="Scott * 0.2")
    #ax.plot(x_eval, kde4(x_eval), 'c-', label="Scott * 0.5")
    ax.plot(x_eval, bimodal_pdf, 'r--', label="Actual PDF")

    ax.set_xlim([x_eval.min(), x_eval.max()])
    ax.legend(loc=2)
    ax.set_xlabel('x')
    ax.set_ylabel('Density')
    plt.show()



