from scapy.utils import RawPcapReader
import graph
import analysis_data
import configparser
from filter import Filter
import constants
from scapy.layers.inet import UDP, TCP


def execute_config(filename_config, filename_data):
    """
    :param filename_config:
    :param filename_data:
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

    launch_analysis('data/' + filename_data, 'null', 'null',
                    filter, size_payload_tcp, size_payload_udp, throughput, interval_throughput, csv)


def convert_string_to_boolean_filter(config_parser, section, filter_name):
    """
    :param config_parser:
    :param section: section in the config file
    :param filter_name: name of the option parameter
    :return:
    """
    if config_parser.get(section, filter_name) == 'T':
        return True
    else:
        return False


def option_out_data(timestamp, tcp_payloads, size_payload_tcp_graph, size_payload_udp_graph, throughput_graph, interval_throughput, csv):
    """
    :param timestamp:
    :param tcp_payloads:
    :param throughput_graph:
    :param interval_throughput:
    :param csv:
    :return:
    """
    interval = int(interval_throughput)
    print(throughput_graph)
    if throughput_graph:
        timestamp = analysis_data.time_interval(interval, timestamp)
        graph.throughput_graph(timestamp, 'time' + str(interval) + ' sec', 'Packets/' + str(interval) + ' sec')
    if size_payload_tcp_graph:
        graph.size_payload_graph(tcp_payloads, "hh", "yy", TCP)
    if size_payload_udp_graph:
        graph.size_payload_graph(tcp_payloads, "hh", "yy", UDP)

    if csv:
        analysis_data.to_csv_time_size(tcp_payloads)


def option_filter(pkt_data, client, server, filter):
    """
    :param filter:
    :param pkt_data:
    :param client:
    :param server:
    :return:
    """

    if filter.IPv4:
        if not filter.ipv4(pkt_data):
            return False
        if filter.UDP:
            if filter.protocol(pkt_data, constants.UDP):
                return True
            if not filter.TCP:
                return False
        if filter.TCP:
            if not filter.protocol(pkt_data, constants.TCP):
                return False
            if filter.SYN:
                if not filter.syn(pkt_data):
                    return False
    return True


def launch_analysis(file_name, client, server, filter,
                    size_payload_tcp_graph, size_payload_udp_graph, throughput_graph, interval_throughput, csv):
    """
    :param size_payload_udp_graph:
    :param size_payload_tcp_graph:
    :param filter:
    :param interval_throughput:
    :param csv:
    :param throughput_graph:
    :param str file_name: pcap file for analysis
    :param str client: address ip with port for filtering
    :param str server: address ip with port for filtering
    :return: list of timestamp and tuple (time,tcp payload size) from all filtered packets
    """

    first_pkt_ordinal = 0
    first_pkt_timestamp = 0
    last_pkt_ordinal = 0
    last_pkt_timestamp = 0
    count = 0
    interesting_packet_count = 0
    timestamp = []
    tuple_pkt_data_time = []

    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        count += 1

        if option_filter(pkt_data, client, server, filter):

            interesting_packet_count += 1
            if interesting_packet_count == 1:
                first_pkt_timestamp = [pkt_metadata.sec, pkt_metadata.usec]
                first_pkt_ordinal = count
            timestamp.append(pkt_metadata.sec)
            tuple_pkt_data_time.append((pkt_metadata.sec, pkt_data))
            last_pkt_timestamp = [pkt_metadata.sec, pkt_metadata.usec]
            last_pkt_ordinal = count

    option_out_data(timestamp, tuple_pkt_data_time, size_payload_tcp_graph, size_payload_udp_graph,
                    throughput_graph, interval_throughput, csv)

    print('{} contains {} packets ({} interesting)'.format(file_name, count, interesting_packet_count))
    print('First packet in connection: Packet #{} {}'.format(first_pkt_ordinal, first_pkt_timestamp))
    print(' Last packet in connection: Packet #{} {}'.format(last_pkt_ordinal, last_pkt_timestamp))


if __name__ == '__main__':
    # client = '192.168.137.1:1900'
    # server = '192.168.137.16:51575'
    execute_config('c1.ini', 'camera_light_on_off.pcap')
    # execute_config('c1.ini', 'camera_movement.pcap')
