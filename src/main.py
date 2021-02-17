import analysis_data
import configparser
from filter import Filter
from throughput import Throughput
from graph import Graph
from packets import Packets
import mapping_light_camera
from scapy.layers.inet import UDP, TCP


def execute_config(filename_config, filename_data):
    """
    Read the config file and launch the analysis with the parameters chose

    :param filename_config: file with config
    :param filename_data: file with the data
    :return:
    """
    config_parser = configparser.RawConfigParser()
    config_parser.read('config/' + filename_config)

    TCP = convert_string_to_boolean_filter(config_parser, 'filter', 'TCP')
    UDP = convert_string_to_boolean_filter(config_parser, 'filter', 'UDP')
    SYN = convert_string_to_boolean_filter(config_parser, 'filter', 'SYN')
    IPv4 = convert_string_to_boolean_filter(config_parser, 'filter', 'IPv4')

    filter = Filter(IPv4, TCP, UDP, SYN)

    throughput = convert_string_to_boolean_filter(config_parser, 'graph', 'throughput')
    size_payload_tcp = convert_string_to_boolean_filter(config_parser, 'graph', 'size_payload_tcp')
    size_payload_udp = convert_string_to_boolean_filter(config_parser, 'graph', 'size_payload_udp')
    csv = convert_string_to_boolean_filter(config_parser, 'data', 'csv')

    interval_throughput = config_parser.get('graph', 'interval_throughput')

    client = config_parser.get('addresses', 'src')
    server = config_parser.get('addresses', 'dst')

    return launch_analysis('data/' + filename_data, client, server,
                    filter, size_payload_tcp, size_payload_udp, throughput, interval_throughput, csv)


def convert_string_to_boolean_filter(config_parser, section, filter_name):
    """
    :param config_parser:
    :param section: section in the config file
    :param filter_name: name of the option parameter
    :return: T True or False
    """
    if config_parser.get(section, filter_name) == 'T':
        return True
    else:
        return False


def option_out_data(data, size_payload_tcp_graph, size_payload_udp_graph, throughput_graph, interval_throughput, csv):
    """
    :param size_payload_udp_graph:
    :param size_payload_tcp_graph:
    :param data:
    :param throughput_graph:
    :param interval_throughput:
    :param csv:
    :return:
    """
    interval = int(interval_throughput)
    if throughput_graph:
        timestamp_rate = Throughput([x[0] for x in data], interval)
        throughput_graph = Graph(timestamp_rate.packet_per_second_tuple, 'time' + str(interval) +
                                 ' sec', 'Packets/' + str(interval) + ' sec', 'Throughput', True, 'device 1')
        throughput_graph.create_graph()
        throughput_graph.show_graph()

    if size_payload_tcp_graph:
        size_tcp_graph = Graph(data, 'hhh', 'yy', 'tcp_payload',  False, 'device 1')
        size_tcp_graph.size_payload_graph(TCP)

    if size_payload_udp_graph:
        size_udp_graph = Graph(data, 'hhh', 'yy', 'udp_payload',  False, 'device 1')
        size_udp_graph.size_payload_graph(UDP)

    if csv:
        analysis_data.to_csv_time_size(data)


def launch_analysis(file_name, client, server, filtering,
                    size_payload_tcp_graph, size_payload_udp_graph, throughput_graph, interval_throughput, csv):
    """
    After it will apply the out option to have the results of calculation.

    :param size_payload_udp_graph:
    :param size_payload_tcp_graph:
    :param filtering:
    :param interval_throughput:
    :param csv:
    :param throughput_graph:
    :param str file_name: pcap file for analysis
    :param str client: address ip with port for filtering
    :param str server: address ip with port for filtering
    :return: list of timestamp and tuple (time,tcp payload size) from all filtered packets
    """

    packets = Packets(file_name)
    packets.read_pcap()
    packet_filter = packets.filter(client, server, filtering)

    option_out_data(packet_filter, size_payload_tcp_graph, size_payload_udp_graph,
                    throughput_graph, interval_throughput, csv)

    return packet_filter


if __name__ == '__main__':
    # execute_config('basic.ini', 'camera_light_on_off.pcap')
    # execute_config('c1.ini', 'camera_movement.pcap')

    # mapping_light_camera.graph_light_camera('c3.ini', 'c4.ini', 'camera_light_on_off_room.pcap')
    mapping_light_camera.graph_light_camera('c3.ini', 'c4.ini', 'no_same_room.pcap')

    # databis = execute_config('c2.ini', 'camera_on_off_tcp.pcap')



