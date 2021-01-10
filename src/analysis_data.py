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
    cus = [0]
    for i in range(1, len(data)-1):
        cus.append(cusum_calculation_up(data[i], statistics.mean(data) , cus[i-1]))
    return cus


def cusum_calculation_up(bitrate, mean, previous):
    return max(0, previous+bitrate-mean)


def cusum_calculation_lo(bitrate, mean, previous):
    return max(0, previous-bitrate+mean)
