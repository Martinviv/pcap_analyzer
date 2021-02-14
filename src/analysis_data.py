import csv
import numpy as np


def to_csv_time_size(tcp_payload):
    """
    :param tcp_payload:
    :return: create csv file to the out directory with time packet and tcp payload packet
    """
    with open('out/data_payload.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['time', 'size'])
        for row in tcp_payload:
            csv_out.writerow(row)


def time_interval(second, timestamp):
    """
    :param int second: size in second of the interval where we count the number of packets
    :param collection.iterable timestamp: collection of all timestamp packets
    :return: list of tuple list(x,y) where x is time and y number packets per interval
    """

    start = timestamp[0]
    end = timestamp[len(timestamp)-1]
    packet_per_second = [0]*int(((end-start) * (1 / second)) + 1)
    real_time = list(range(start, start+len(packet_per_second), 1))
    for x in timestamp:
        packet_per_second[int((x-start) * (1 / second))] += 1
    packet_per_second_tuple = list(zip(real_time, packet_per_second))
    return packet_per_second_tuple


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


def get_interval(data,size, time, shift):
    """
    :param data:
    :param size: size of the (or the right) part of the subarray around the time value
    :param time: value that we want the most close in our array to have a right and left part
    :param shift: shift to the right from the array around the value
    :return: a subarray of data between arround the time value
    """
    a = find_nearest([x[0] for x in data], time)
    subdata = data[a-size+shift:a+size+1+shift]
    return subdata


# https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx







