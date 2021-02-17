import analysis_data
import configparser
from filter import Filter
from throughput import Throughput
from graph import Graph
from packets import Packets
import mapping_light_camera
from scapy.layers.inet import UDP, TCP


def execute_single_config(filename_config, filename_data):
    """
    Read the config file and launch the analysis with the parameters chose

    :param filename_config: file with config
    :param filename_data: file with the data
    :return:
    """
    filtering, interval_throughput, size_payload_tcp, size_payload_udp, throughput = config_analysis(
        filename_config)

    packets = Packets('data/'+filename_data)
    packets.read_pcap()
    packet_filter = packets.filter(filtering)

    option_out_data(packet_filter, size_payload_tcp, size_payload_udp,
                    throughput, interval_throughput)

    return packet_filter


def execute_multiple_config(filename_config_1,filename_config_2, filename_data):
    filtering_1, interval_throughput_1, size_payload_tcp_1, size_payload_udp_1, throughput_1 = config_analysis(
        filename_config_1)
    filtering_2, interval_throughput_2, size_payload_tcp_2, size_payload_udp_2, throughput_2 = config_analysis(
        filename_config_2)

    packets_1 = Packets('data/' + filename_data)
    packets_1.read_pcap()

    packet_filter_1 = packets_1.filter(filtering_1)
    packet_filter_2 = packets_1.filter(filtering_2)

    option_out_data(packet_filter_1, size_payload_tcp_1, size_payload_udp_1,
                    throughput_1, interval_throughput_1)
    option_out_data(packet_filter_2, size_payload_tcp_2, size_payload_udp_2,
                    throughput_2, interval_throughput_2)

    return packet_filter_1, packet_filter_2


def config_analysis(filename_config):
    config_parser = configparser.RawConfigParser()
    config_parser.read('config/' + filename_config)
    tcp = convert_string_to_boolean_filter(config_parser, 'filter', 'TCP')
    udp = convert_string_to_boolean_filter(config_parser, 'filter', 'UDP')
    syn = convert_string_to_boolean_filter(config_parser, 'filter', 'SYN')
    ipv4 = convert_string_to_boolean_filter(config_parser, 'filter', 'IPv4')

    throughput = convert_string_to_boolean_filter(config_parser, 'graph', 'throughput')
    size_payload_tcp = convert_string_to_boolean_filter(config_parser, 'graph', 'size_payload_tcp')
    size_payload_udp = convert_string_to_boolean_filter(config_parser, 'graph', 'size_payload_udp')
    interval_throughput = config_parser.get('graph', 'interval_throughput')
    client = config_parser.get('addresses', 'src')
    server = config_parser.get('addresses', 'dst')

    filtering = Filter(ipv4, tcp, udp, syn, client, server)
    return filtering, interval_throughput, size_payload_tcp, size_payload_udp, throughput


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


def option_out_data(data, size_payload_tcp_graph, size_payload_udp_graph, throughput_graph, interval_throughput):
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


if __name__ == '__main__':
    # execute_config('basic.ini', 'camera_light_on_off.pcap')
    # execute_config('c1.ini', 'camera_movement.pcap')

    # mapping_light_camera.graph_light_camera('c3.ini', 'c4.ini', 'camera_light_on_off_room.pcap')
    mapping_light_camera.graph_light_camera('c3.ini', 'c4.ini', 'no_same_room.pcap')

    # databis = execute_config('c2.ini', 'camera_on_off_tcp.pcap')
