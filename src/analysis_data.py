import csv


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
    return packet_per_second