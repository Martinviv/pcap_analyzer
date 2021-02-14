import matplotlib.pyplot as plt
import analysis_packet
import analysis_data
import bimodal_statistics


def throughput_graph(data, leg_x, leg_y, title):
    """
    :param title: title of graph
    :param list[(x,y)] data:  x timestamps that start the interval and y is number of packets for each interval
    :param str leg_x: legend axe x
    :param str leg_y: legend axe y
    :return: plot graph and show the graph (with the cusum graph)
    """
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]
    create_graph(x_val, y_val, title, True)

    # cusum
    # create_graph(x_val, analysis_data.cusum(y_val), "Cusum_Throughput", True)
    # bimodal_statistics.bimodal(y_val)


def size_payload_graph(data, leg_x, leg_y, protocol):
    """
    :param protocol: TCP or UDP
    :param list[(x,y)] data:  x timestamps that start the interval and y is number of packets for each interval
    :param str leg_x: legend axe x
    :param str leg_y: legend axe y
    :return: set of coordinates where x time and y tcp payload size (no return) and show graph
    """
    x_val = [x[0] for x in data]
    y_val = [analysis_packet.get_tcp_payload_size(x[1], protocol) for x in data]

    create_graph(x_val, y_val, "Payload size for each packets", False)

    create_graph(analysis_data.smooth(x_val, 15),
                 analysis_data.smooth(y_val, 15), "Smooth value", False)


def create_graph(x_val, y_val, title, is_plot):
    """
    :param x_val: values x
    :param y_val: values y
    :param title: Title that will be show
    :param is_plot: True if plot graph false for scatter (point)
    :return: create and show the graph
    """
    plt.figure(figsize=(14, 14))
    plt.grid()
    # Major ticks every 20, minor ticks every 5
    if is_plot:
        plt.plot(x_val, y_val)
    else:
        plt.scatter(x_val, y_val)
    # plt.scatter(x_val, y_val, 'or')
    plt.title(title)
    plt.show()

def create_graph_multiple(x_val, y_val,x_val_bis, y_val_bis, title, is_plot):
        """
        :param x_val: values x
        :param y_val: values y
        :param title: Title that will be show
        :param is_plot: True if plot graph false for scatter (point)
        :return: create and show the graph
        """
        # change quality
        plt.figure(figsize=(14, 14))
        plt.grid()
        # Major ticks every 20, minor ticks every 5
        if is_plot:
            plt.plot(x_val, y_val)
            plt.plot(x_val_bis,y_val_bis)
        else:
            plt.scatter(x_val, y_val)
            plt.scatter(x_val_bis, y_val_bis)
        # plt.scatter(x_val, y_val, 'or')
        plt.title(title)
        plt.show()


def multiple_throughput_graph(data, databis):
        """
        :param list[(x,y)] data:  x timestamps that start the interval and y is number of packets for each interval

        :return: plot graph and show the graph (with the cusum graph)
        """
        x_val = [x[0] for x in data]
        y_val = [x[1] for x in data]

        x_valBis = [x[0] for x in databis]
        y_valBis = [x[1] for x in databis]
        create_graph_multiple(x_val, y_val, x_valBis, y_valBis, "Throughput multiple", True)


def create_graph_with_vertical_line(data, title, is_plot, list_vertical):
    """
    :param data:
    :param list_vertical:
    :param title: Title that will be show
    :param is_plot: True if plot graph false for scatter (point)
    :return: create and show the graph
    """

    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    plt.figure(figsize=(14, 14))
    plt.grid()
    # Major ticks every 20, minor ticks every 5
    if is_plot:
        plt.plot(x_val, y_val)
        for xv in list_vertical:
            plt.axvline(xv, color='r', linestyle='--')
    else:
        plt.scatter(x_val, y_val)
    # plt.scatter(x_val, y_val, 'or')
    plt.title(title)
    plt.show()


