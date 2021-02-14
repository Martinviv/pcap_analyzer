import main
import graph
import analysis_data
import bimodal_statistics


def graph_light_camera(conf1, conf2, file):
    data = main.execute_config(conf1, file)
    # databis = main.execute_config(conf2, file)
    timestamp_rate = analysis_data.time_interval(1, [x[0] for x in data])
    # timestamp_rate_bis = analysis_data.time_interval(1, [x[0] for x in databis])
    print('subarray')
    size = 20
    subarray = analysis_data.get_interval(timestamp_rate, size, 1612689549, 0)
    print(subarray)
    # graph.multiple_throughput_graph(timestamp_rate, timestamp_rate_bis)
    bimodal_statistics.difference_data([x[1] for x in subarray], size, 5, 0.01)
    graph.throughput_graph(subarray, 'hhh', 'gg')
