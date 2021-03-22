import main
import test_statistics
from throughput import Throughput
from graph import Graph
from house import House


def light_camera(conf1, conf2, file):
    packet_camera, packet_light = main.execute_multiple_config("mapping_light/" + conf1, "mapping_light/" + conf2, file)

    timestamp_rate_camera = Throughput([x[0] for x in packet_camera], 1)
    timestamp_rate_light = Throughput([x[0] for x in packet_light], 1)
    list_threshold = timestamp_rate_light.check_threshold(1)

    # size (in second) for the interval after and before
    size = 15
    # before delay of 2
    is_light_and_camera = sub_array(timestamp_rate_camera, size, list_threshold, 0, 2)

    graph_representation = Graph(timestamp_rate_camera.packet_per_second_tuple, 'time', 'size',
                                 "Comparison light camera",
                                 True, 'camera')
    graph_representation.create_graph()
    graph_representation.add_vertical_line(is_light_and_camera, 'light_same_room')

    # for showing 2 same time
    graph_representation.add_data(timestamp_rate_light.packet_per_second_tuple, 'light')
    graph_representation.show_graph()
    return is_light_and_camera


def light_two_camera(conf1, conf2, conf3, file):
    """
    :param conf1 : configuration for the light
    :param conf2 : configuration first camera
    :param conf3 : configuration for the second camera
    """
    is_with_light_cam1 = light_camera(conf2, conf1, file)
    is_with_light_cam2 = light_camera(conf3, conf1, file)
    match_between_two_camera = (2*(len(set(is_with_light_cam1) & set(is_with_light_cam2))))/(len(is_with_light_cam1+is_with_light_cam2))
    print(match_between_two_camera)
    return is_with_light_cam1, is_with_light_cam2, match_between_two_camera


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
        if last < y - delay - 4 and abs(
                timestamp_rate.start - y) > size:  # choose arbitrarily to avoid similar graph ( in future merge the intervals)
            print('time')
            print(y)
            subarray = timestamp_rate.get_interval(size, y, shift)
            statistics, pvalue, distribution_1, distribution_2 = test_statistics.difference_data(
                [x[1] for x in subarray]
                , size, delay)

            if pvalue is None:
                break
            last = y
            h0 = hypothesis_check_update_threshold(list_is_present, pvalue, y)

            if not h0:
                is_room = my_house.pattern_compare(distribution_1, distribution_2)
                if is_room:
                    list_is_in_same_room.append(y)
    print('threshold')
    print(my_house.in_same_room)
    # return list_is_present
    return list_is_in_same_room


def hypothesis_check_update_threshold(list_is_present, pvalue, y):
    alpha = 0.05
    if pvalue > alpha / 2:
        # print('H0 accepted -> mean_left=mean_right')
        return True
    else:
        # print('H0 rejected')
        list_is_present.append(y)
        return False
