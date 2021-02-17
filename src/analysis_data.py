import numpy as np

def cusum(data):
    """
    :param data:
    :return: cusum value for all data
    """
    cus = [0]
    for i in range(1, len(data)):
        cus.append(cusum_calculation_up(data[i], np.mean(data),
                                        cus[i-1], np.std(data)))
    return cus


def cusum_calculation_up(rate, mean, previous, variance):
    """
    :param rate: rate from one sequence
    :param mean: packet rate in mean to detect variation
    :param previous: value cusum from the previous calculation
    :param variance: to evaluate the k for the tolerance
    :return: cusum value for the rate interval
    """
    # mou 1 or 1/2 standard deviation
    k = 0.5*variance
    return max(0, previous + rate - mean - k)


def cusum_calculation_lo(rate, mean, previous, variance):
    """
    :param rate: rate from one sequence
    :param mean: packet rate in mean to detect variation
    :param previous: value cusum from the previous calculation
    :param variance: to evalute the k for the tolerance
    :return: cusum value for the rate interval
    """
    # mou 1 or 1/2 standart deviantion
    k = 0.5*variance
    return max(0, previous - rate + mean - k)


def smooth(data, coefficient):
    """
    :param data: axe values that we want smooth
    :param coefficient: if 3 then x 0 1 2
    :return: values smoothed
    """
    data_smooth = []
    for pkt in range(len(data)-1-coefficient):
        sum_smooth = 0
        for x in range(coefficient):
            sum_smooth = data[pkt+x]+sum_smooth
        mean = sum_smooth/coefficient
        data_smooth.append(mean)
    return data_smooth
