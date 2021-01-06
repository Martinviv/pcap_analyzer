from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
import constants


def filter_address_src(pkt_data, server_ip, client_ip):
    """
    :param pkt_data:
    :param server_ip:
    :param client_ip:
    :return:
    :rtype: bool
    """
    ether_pkt = Ether(pkt_data)
    ip_pkt = ether_pkt[IP]
    return (ip_pkt.src == server_ip) or (ip_pkt.src == client_ip)


def filter_address_dst(pkt_data, server_ip, client_ip):
    """
    :param pkt_data:
    :param server_ip:
    :param client_ip:
    :return:
    :rtype: bool
    """
    ether_pkt = Ether(pkt_data)
    ip_pkt = ether_pkt[IP]
    return (ip_pkt.dst == server_ip) or (ip_pkt.dst == client_ip)


def filter_port_src(pkt_data, client_port, server_port):
    """
    :param pkt_data:
    :param client_port:
    :param server_port:
    :return:
    :rtype: bool
    """
    ether_pkt = Ether(pkt_data)
    ip_pkt = ether_pkt[IP]
    tcp_pkt = ip_pkt[TCP]
    return (tcp_pkt.sport == int(server_port)) or (tcp_pkt.sport == int(client_port))


def filter_port_dst(pkt_data, client_port, server_port):
    """
    :param pkt_data:
    :param client_port:
    :param server_port:
    :return:
    :rtype: bool
    """
    ether_pkt = Ether(pkt_data)
    ip_pkt = ether_pkt[IP]
    tcp_pkt = ip_pkt[TCP]
    return (tcp_pkt.dport == int(server_port)) or (tcp_pkt.dport == int(client_port))


def filter_syn(pkt_data):
    """
    :param pkt_data:
    :return: true if we have a SYN packet
    :rtype: bool
    """
    ether_pkt = Ether(pkt_data)
    ip_pkt = ether_pkt[IP]
    tcp_pkt = ip_pkt[TCP]
    return tcp_pkt.flags == constants.SYN


def filter_pcap(pkt_data):
    """

    :param pkt_data:
    :param server_ip:
    :param client_ip:
    :param server_port:
    :param client_port:
    :return: combination of others filters
    :rtype: bool
    """
    return filter_ipv4(pkt_data) and \
           filter_tcp(pkt_data)# and \
           #filter_syn(pkt_data)
           # filter_address_dst(pkt_data, server_ip, client_ip) and \
           # filter_address_src(pkt_data, server_ip, client_ip) and \
           # filter_port_src(pkt_data, client_port, server_port) and \
           # filter_port_dst(pkt_data, client_port, server_port)


# disregard non-IPv4 packets
def filter_ipv4(pkt_data):
    """
    :param pkt_data:
    :return: true if we have IPv4
    :rtype: bool
    """
    ether_pkt = Ether(pkt_data)
    return ether_pkt.type == constants.IPV4


def filter_tcp(pkt_data):
    """
    :param pkt_data:
    :return: true if we have tcp
    :rtype: bool
    """
    ether_pkt = Ether(pkt_data)
    ip_pkt = ether_pkt[IP]
    return ip_pkt.proto == constants.TCP
