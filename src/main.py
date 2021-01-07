from scapy.utils import RawPcapReader
import graph
import analysis_packet
import analysis_data
import configparser
import filter


def execute_config(filename_config, filename_data):
    """
    :param filename_config:
    :param filename_data:
    :return:
    """
    config_parser = configparser.RawConfigParser()
    config_parser.read('config/'+filename_config)
    TCP = config_parser.get('filter', 'TCP')
    UDP = config_parser.get('filter', 'UDP')
    SYN = config_parser.get('filter', 'SYN')
    IPv4 = config_parser.get('filter', 'IPv4')

    interval_throughput = config_parser.get('graph', 'interval_throughput')
    size_payload = config_parser.get('graph', 'size')
    throughput = config_parser.get('graph', 'throughput')
    csv = config_parser.get('data', 'csv')

    launch_analysis('data/'+filename_data, 'null', 'null',
                    TCP, UDP, SYN, IPv4, size_payload, throughput, interval_throughput, csv)


def option_out_data(timestamp, tcp_payloads, size_payload_graph, throughput_graph, interval_throughput, csv):
    """
    :param timestamp:
    :param tcp_payloads:
    :param size_payload_graph:
    :param throughput_graph:
    :param interval_throughput:
    :param csv:
    :return:
    """
    interval = int(interval_throughput)
    print(throughput_graph)
    if throughput_graph == 'T':
        timestamp = analysis_data.time_interval(interval, timestamp)
        graph.throughput_graph(timestamp, 'time' + str(interval) + ' sec', 'Packets/' + str(interval) + ' sec')
    if size_payload_graph == 'T':
        graph.size_payload_graph(tcp_payloads, "hh", "yy")
    if csv == 'T':
        analysis_data.to_csv_time_size(tcp_payloads)


def option_filter(pkt_data, client, server, TCP, UDP, SYN, IPv4):
    """
    :param pkt_data:
    :param client:
    :param server:
    :param TCP:
    :param UDP:
    :param SYN:
    :param IPv4:
    :return:
    """
    if IPv4 == 'T':
        if not filter.ipv4(pkt_data):
            return False
        if TCP == 'T':
            if not filter.tcp(pkt_data):
                return False
            if SYN == 'T':
                if not filter.syn(pkt_data):
                    return False
    return True


def launch_analysis(file_name, client, server, TCP, UDP, SYN, IPv4,
                    size_payload_graph, throughput_graph, interval_throughput, csv):
    """
    :param interval_throughput:
    :param csv:
    :param IPv4:
    :param SYN:
    :param UDP:
    :param TCP:
    :param size_payload_graph:
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
    tcp_payloads = []

    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        count += 1

        if option_filter(pkt_data, client, server, TCP, UDP, SYN, IPv4):

            interesting_packet_count += 1
            if interesting_packet_count == 1:
                first_pkt_timestamp = [pkt_metadata.sec, pkt_metadata.usec]
                first_pkt_ordinal = count
            timestamp.append(pkt_metadata.sec)
            tcp_payloads.append((pkt_metadata.sec, analysis_packet.get_tcp_payload_size(pkt_data)))
            last_pkt_timestamp = [pkt_metadata.sec, pkt_metadata.usec]
            last_pkt_ordinal = count

    option_out_data(timestamp, tcp_payloads, size_payload_graph, throughput_graph, interval_throughput,csv)

    print('{} contains {} packets ({} interesting)'. format(file_name, count, interesting_packet_count))
    print('First packet in connection: Packet #{} {}'.format(first_pkt_ordinal, first_pkt_timestamp))
    print(' Last packet in connection: Packet #{} {}'.format(last_pkt_ordinal,last_pkt_timestamp))
    print(tcp_payloads)


if __name__ == '__main__':
    # client = '192.168.137.1:1900'
    # server = '192.168.137.16:51575'
    execute_config('c1.ini', 'light_on_off.pcap')

