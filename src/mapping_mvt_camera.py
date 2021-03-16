import main
from throughput import Throughput
from graph import Graph
import analysis_data


def graph_camera(conf1, conf2, file):
    packet_cam1, packet_cam2 = main.execute_multiple_config('mapping_camera_mvt/' + conf1,
                                                            'mapping_camera_mvt/' + conf2, file)

    timestamp_rate_cam1 = Throughput([x[0] for x in packet_cam1], 1)
    timestamp_rate_cam2 = Throughput([x[0] for x in packet_cam2], 1)

    graph_cam = Graph(timestamp_rate_cam1.packet_per_second_tuple, 'time', 'size', "Comparison light camera",
                      True, 'camera 1')
    graph_cam.add_data(timestamp_rate_cam2.packet_per_second_tuple, 'camera 2')
    graph_cam.create_graph()
    graph_cam.show_graph()
    cus1, cus2 = cusum_search(timestamp_rate_cam1, timestamp_rate_cam2)



def cusum_search(timestamp_rate_cam1, timestamp_rate_cam2):
    timestamp_rate_cusum_cam1 = analysis_data.cusum(timestamp_rate_cam1.packet_per_second_tuple)
    timestamp_rate_cusum_cam2 = analysis_data.cusum(timestamp_rate_cam2.packet_per_second_tuple)
    graph = Graph(timestamp_rate_cusum_cam1, 'time', 'size', "camera1 cusum",
                  True, 'camera')
    graph.add_data(timestamp_rate_cusum_cam2, "camera 2 cusum")
    acceptable_interval_cam1 = analysis_data.generate_interval(timestamp_rate_cusum_cam1, 10)
    acceptable_interval_cam2 = analysis_data.generate_interval(timestamp_rate_cusum_cam2, 10)
    line = intersections(acceptable_interval_cam1, acceptable_interval_cam2)
    graph.add_area(acceptable_interval_cam1, "red")
    graph.add_area(acceptable_interval_cam2, "green")


    # showing line superposition ------
    # list_line = list()
    # for elem in line:
    #    list_line.append(elem[0])
    #    list_line.append(elem[1])
    # graph.add_vertical_line(list_line, "line")
    # -------------------------------


    # ratio is percentage are covered by the two
    ratio = 2*(sum_interval(line))/(sum_interval(acceptable_interval_cam2)+sum_interval(acceptable_interval_cam1))
    print("ratio")
    print(ratio)

    graph.create_graph()
    graph.show_graph()

    return timestamp_rate_cusum_cam1, timestamp_rate_cusum_cam2


# from https://stackoverflow.com/questions/40367461/intersection-of-two-lists-of-ranges-in-python/40368603
def intersections(a, b):
    ranges = []
    i = j = 0
    while i < len(a) and j < len(b):
        a_left, a_right = a[i]
        b_left, b_right = b[j]

        if a_right < b_right:
            i += 1
        else:
            j += 1

        if a_right >= b_left and b_right >= a_left:
            end_pts = sorted([a_left, a_right, b_left, b_right])
            middle = (end_pts[1], end_pts[2])
            ranges.append(middle)

    ri = 0
    while ri < len(ranges)-1:
        if ranges[ri][1] == ranges[ri+1][0]:
            ranges[ri:ri+2] = [[ranges[ri][0], ranges[ri+1][1]]]

        ri += 1
    return ranges


def sum_interval(interval):
    sum = 0
    for elem in interval:
        sum = elem[1] - elem[0] + sum
    return sum