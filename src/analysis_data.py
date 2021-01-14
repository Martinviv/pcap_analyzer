import csv
import numpy as np
import statistics


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
    :return: array with the number of packet per interval
    """

    start = timestamp[0]
    end = timestamp[len(timestamp)-1]
    packet_per_second = [0]*int(((end-start) * (1 / second)) + 1)
    for x in timestamp:
        packet_per_second[int((x-start) * (1 / second))] += 1
    print(np.cumsum(packet_per_second))
    return packet_per_second


def cusum(data):
    """
    :param data:
    :return: cusum value for all data
    """
    cus = [0]
    for i in range(1, len(data)-1):
        cus.append(cusum_calculation_up(data[i], statistics.mean(data),
                                        cus[i-1], statistics.stdev(data)))
    return cus


def cusum_calculation_up(rate, mean, previous, variance):
    """
    :param rate: rate from one sequence
    :param mean: packet rate in mean to detect variation
    :param previous: value cusum from the previous calculation
    :param variance: to evalute the k for the tolerance
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
