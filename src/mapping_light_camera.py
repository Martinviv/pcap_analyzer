import main
import test_statistics
from throughput import Throughput
from graph import Graph
from house import House
from distribution import Distribution


def graph_light_camera(conf1, conf2, file):
    packet, packet_light = main.execute_multiple_config(conf1, conf2, file)

    timestamp_rate = Throughput([x[0] for x in packet], 1)
    timestamp_rate_bis = Throughput([x[0] for x in packet_light], 1)
    list_threshold = timestamp_rate_bis.check_threshold(1)

    # size (in second) for the interval after and before
    size = 15
    # before delay of 4
    is_present = sub_array(timestamp_rate, size, list_threshold, 0, 4)

    vertical_line = Graph(timestamp_rate.packet_per_second_tuple, 'time', 'size', "Comparison light camera",
                          True, 'camera')
    vertical_line.create_graph()
    vertical_line.add_vertical_line(is_present, 'light_same_room')

    # for showing 2 same time
    vertical_line.add_data(timestamp_rate_bis.packet_per_second_tuple, 'light')

    vertical_line.show_graph()


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
    list_is_in_same_room = []

    my_house = House()

    for y in time:
        if last < y-delay - 2 and abs(timestamp_rate.start-y)>size:  # choose arbitrarily to avoid similar graph ( in future merge the intervals)
            print('time')
            print(y)
            subarray = timestamp_rate.get_interval(size, y, shift)
            statistics, pvalue, distribution_1, distribution_2 = test_statistics.difference_data([x[1] for x in subarray]
                                                                                                 , size, delay)

            if pvalue is None:
                break
            last = y
            h0 = hypothesis_check_update_threshold(list_is_present, pvalue, y)

            if not h0:
                is_room = my_house.pattern_compare(distribution_1, distribution_2)
                if is_room:
                    list_is_in_same_room.append(y)

            # graph.throughput_graph(subarray, 'hhh', 'gg', y)
    print('threshold')
    print(my_house.in_same_room)
    #return list_is_present
    return list_is_in_same_room


def hypothesis_check_update_threshold(list_is_present, pvalue, y):
    alpha = 0.05
    if pvalue > alpha / 2:
        #print('H0 accepted -> mean_left=mean_right')
        return True
    else:
        #print('H0 rejected')
        list_is_present.append(y)
        return False
