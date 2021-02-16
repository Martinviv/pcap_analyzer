import main
import bimodal_statistics
from throughput import Throughput
from graph import Graph


def graph_light_camera(conf1, conf2, file):
    data = main.execute_config(conf1, file)
    databis = main.execute_config(conf2, file)
    timestamp_rate = Throughput([x[0] for x in data], 1)
    timestamp_rate_bis = Throughput([x[0] for x in databis], 1)
    list_threshold = timestamp_rate_bis.check_threshold(1)

    # size (in second) for the interval after and before
    size = 15
    is_present = sub_array(timestamp_rate, size, list_threshold, 0, 4)

    vertical_line = Graph(timestamp_rate.packet_per_second_tuple, 'rr', 'rr', "rate_vertical,", True)
    vertical_line.create_graph_with_vertical_line(is_present)

    # graph.multiple_throughput_graph(timestamp_rate, timestamp_rate_bis)


def sub_array(timestamp_rate, size, time_list, shift, delay):
    """
    :param timestamp_rate: list of tuple where (time, number of packets)
    :param size: size (in second) for the interval after and before
    :param time_list: list where light send data over a certain threshold
    :param shift: translate the interval
    :param delay: value that will no take in account after the potential cut
    :return: list with time where a cut is detected
    """
    time = [x[0] for x in time_list]
    last = 0
    list_is_present = []
    for y in time:
        if last < y-delay:  # choose arbitrarily to avoid similar graph ( in future merge the intervals)
            print('time')
            print(y)
            # subarray = analysis_data.get_interval(timestamp_rate, size, y, shift)
            subarray = timestamp_rate.get_interval(size, y, shift)
            H0 = bimodal_statistics.difference_data([x[1] for x in subarray], size, delay, 0.05)
            # graph.throughput_graph(subarray, 'hhh', 'gg', y)
            last = y
            if not H0:
                list_is_present.append(y)
    return list_is_present
