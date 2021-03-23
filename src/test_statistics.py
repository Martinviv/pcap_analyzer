from scipy import stats
import numpy as np
import logging
from distribution import Distribution


def difference_data(data, size, delay):
    """
    :param data:
    :param size: size of the right (or the left part of the array
    :param delay: time in the second that are not take in account in the right part (to avoid irrelevant threshold during the transition
    :return: print p-value, mean, std and return True if the hypothesis nul is accepted
    """
    x2 = np.array(data)
    if len(x2[size:2*size])-size < 0:
        logging.debug('not enough data to continue : %s but we must have at least %s ', print(x2[size:2*size]), size)
        return None, None, None, None
    x2_left = x2[0:size]
    x2_right = x2[size+delay:2*size]
    x2_left_mean = np.mean(x2_left)
    x2_right_mean = np.mean(x2_right)
    x2_left_std = np.std(x2_left)
    x2_right_std = np.std(x2_right)
    # print(x2_left)
    # print(x2_left_mean)
    # print(x2_right)
    # print(x2_right_mean)

    # test T H0 same variance True for same variance
    statistics, pvalue = stats.ttest_ind_from_stats(x2_left_mean, x2_left_std, size, x2_right_mean,
                                                    x2_right_std, size-delay, False)
    size_right = size - delay
    distribution_1 = Distribution(x2_left_mean, x2_left_std, size)
    distribution_2 = Distribution(x2_right_mean, x2_right_std, size_right)
    logging.info('p_value between left and right part : %s', pvalue)
    return statistics, pvalue, distribution_1, distribution_2