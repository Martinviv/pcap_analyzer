from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP


def get_tcp_payload_size(pkt_data, protocol):
    """
    :param protocol: choose protocol (UDP or TCP)
    :param pkt_data: one packet from the file
    :return: packets payload size in byte
    :rtype: int
    """
    ether_pkt = Ether(pkt_data)
    ip_pkt = ether_pkt[IP]
    tcp_pkt = ip_pkt[protocol]
    return len(tcp_pkt.payload)
