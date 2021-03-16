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
    print(acceptable_interval_cam1)
    graph.add_area(acceptable_interval_cam1, "red")
    graph.add_area(acceptable_interval_cam2, "green")

    graph.create_graph()
    graph.show_graph()

    return timestamp_rate_cusum_cam1, timestamp_rate_cusum_cam2
