import main
from throughput import Throughput
from graph import Graph
import analysis_data


def graph_camera(conf1,conf2,file):
    packet, packet_light = main.execute_multiple_config('mapping_camera_mvt/' + conf1, 'mapping_camera_mvt/' + conf2, file)

    timestamp_rate = Throughput([x[0] for x in packet], 1)
    timestamp_rate_bis = Throughput([x[0] for x in packet_light], 1)

    vertical_line = Graph(timestamp_rate.packet_per_second_tuple, 'time', 'size', "Comparison light camera",
                          True, 'camera')

    vertical_line.add_data(timestamp_rate_bis.packet_per_second_tuple, 'light')


def cusum_search(conf1, file):
    packet = main.execute_single_config(conf1, file)
    timestamp_rate = Throughput([x[0] for x in packet], 1)
    graph = Graph(timestamp_rate.packet_per_second_tuple, 'time', 'size', "camera rate",
                          True, 'camera')
    graph.create_graph()

    timestamp_rate_cusum = analysis_data.cusum(timestamp_rate.packet_per_second_tuple)
    print(timestamp_rate_cusum)
    graphbis = Graph(timestamp_rate_cusum, 'time', 'size', "camera cusum",
                          True, 'camera')
    graphbis.create_graph()
    graphbis.show_graph()
