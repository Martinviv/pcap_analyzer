import main
import graph
import analysis_data
import bimodal_statistics


def graph_light_camera(conf1, conf2, file):
    data = main.execute_config(conf1, file)
    databis = main.execute_config(conf2, file)
    timestamp_rate = analysis_data.time_interval(1, [x[0] for x in data])
    timestamp_rate_bis = analysis_data.time_interval(1, [x[0] for x in databis])

    list_threshold = analysis_data.check_threshold(timestamp_rate_bis, 1)
    print('subarray')
    size = 20
    #subarray = analysis_data.get_interval(timestamp_rate, size, 1612689549, 0)
    sub_array(timestamp_rate,size,list_threshold, 0, 0)
    # graph.multiple_throughput_graph(timestamp_rate, timestamp_rate_bis)


def sub_array(timestamp_rate, size, time_list, shift, delay):
    time = [x[0] for x in time_list]
    last = 0
    for y in time:
        if last < y-5: # choose arbitrarly to avoid similar graph
            print('time')
            print(y)
            subarray = analysis_data.get_interval(timestamp_rate, size, y, shift)
            bimodal_statistics.difference_data([x[1] for x in subarray], size, delay, 0.01)
            graph.throughput_graph(subarray, 'hhh', 'gg', y)
            last = y
