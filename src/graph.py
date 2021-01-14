import matplotlib.pyplot as plt
import analysis_packet
import analysis_data


def throughput_graph(data, leg_x, leg_y):
    """
    :param list[int] data: number of packets for each interval where indices correspond of interval number
    :param str leg_x: legend axe x
    :param str leg_y: legend axe y
    :return: plot graph and show the graph
    """
    plt.plot(data)
    plt.ylabel(leg_y)
    plt.xlabel(leg_x)
    plt.show()

    # cusum
    plt.plot(analysis_data.cusum(data))
    plt.ylabel(leg_y)
    plt.xlabel(leg_x)
    plt.show()


def size_payload_graph(data, leg_x, leg_y, protocol):
    """
    :param protocol:
    :param collection.iterable data: (x,y) tuple of coordinates where x is time and y pkt_data
    :param str leg_x: legend axe x
    :param str leg_y: legend axe y
    :return: set of coordinates where x time and y tcp payload size and show graph
    """
    x_val = [x[0] for x in data]
    y_val = [analysis_packet.get_tcp_payload_size(x[1], protocol) for x in data]
    # change quality
    plt.figure(figsize=(14, 14))
    plt.grid()
    # Major ticks every 20, minor ticks every 5
    plt.scatter(x_val, y_val)
    # plt.scatter(x_val, y_val, 'or')
    plt.show()

    # change quality
    plt.figure(figsize=(14, 14))
    plt.grid()
    # Major ticks every 20, minor ticks every 5
    plt.scatter(analysis_data.smooth(x_val, 15), analysis_data.smooth(y_val, 15))
    # plt.scatter(x_val, y_val, 'or')
    plt.show()
