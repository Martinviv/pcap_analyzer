from scipy import stats
from functools import partial
import numpy as np
import matplotlib.pyplot as plt


# code adapted from : https://docs.scipy.org/doc/scipy/reference/tutorial/stats.html


def my_kde_bandwidth(obj, fac=1./5):
    """We use Scott's Rule, multiplied by a constant factor."""
    return np.power(obj.n, -1./(obj.d+4)) * fac


def bimodal(data):
    loc1, scale1, size1 = (81.5, 3.7, 175)
    loc2, scale2, size2 = (63, 6.3, 175)
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

    idx_max = getExtremePoints(kde(x_eval), 'max')
    idx_min = getExtremePoints(kde(x_eval), 'min')
    ax.plot(x_eval[idx_max], kde(x_eval[idx_max]), 'ro')
    ax.plot(x_eval[idx_min], kde(x_eval[idx_min]), 'bo')

    ax.set_xlim([x_eval.min(), x_eval.max()])
    ax.legend(loc=2)
    ax.set_xlabel('x')
    ax.set_ylabel('Density')
    plt.show()
    print(stats.ks_2samp(bimodal_pdf, kde(x_eval)))


# from : https://towardsdatascience.com/modality-tests-and-kernel-density-estimations-3f349bb9e595

def getExtremePoints(data, typeOfInflexion=None, maxPoints=None):
    """
    This method returns the indeces where there is a change in the trend of the input series.
    typeOfExtreme = None returns all extreme points, max only maximum values and min
    only min,
    """
    a = np.diff(data)
    asign = np.sign(a)
    signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)
    idx = np.where(signchange == 1)[0]

    if typeOfInflexion == 'max' and data[idx[0]] < data[idx[1]]:
        idx = idx[1:][::2]

    elif typeOfInflexion == 'min' and data[idx[0]] > data[idx[1]]:
        idx = idx[1:][::2]
    elif typeOfInflexion is not None:
        idx = idx[::2]

        # sort ids by min value
    if 0 in idx:
        idx = np.delete(idx, 0)
    if (len(data) - 1) in idx:
        idx = np.delete(idx, len(data) - 1)
    idx = idx[np.argsort(data[idx])]
    # If we have maxpoints we want to make sure the timeseries has a cutpoint
    # in each segment, not all on a small interval
    if maxPoints is not None:
        idx = idx[:maxPoints]
        if len(idx) < maxPoints:
            return (np.arange(maxPoints) + 1) * (len(data) // (maxPoints + 1))

    return idx


