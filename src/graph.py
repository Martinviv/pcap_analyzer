import matplotlib.pyplot as plt
import analysis_packet
import analysis_data
import bimodal_statistics


class Graph:

    def __init__(self, data, leg_x, leg_y, title, is_plot):
        self.data = data
        self.leg_x = leg_x
        self.leg_y = leg_y
        self.is_plot = is_plot
        self.x_val = [x[0] for x in data]
        self.y_val = [x[1] for x in data]
        plt.figure(figsize=(14, 14))
        plt.grid()
        plt.title(title)
        self.plt = plt

    def size_payload_graph(self, protocol):
        """
        :param protocol: TCP or UDP
        :param list[(x,y)] data:  x timestamps that start the interval and y is number of packets for each interval
        :return: set of coordinates where x time and y tcp payload size (no return) and show graph
        """

        # TODO : update with new signature
        y_val_size = [analysis_packet.get_tcp_payload_size(x[1], protocol) for x in self.data]
        self.create_graph()

        # TODO : update with new signature
        # self.create_graph(analysis_data.smooth(self.x_val, 15), analysis_data.smooth(y_val_size, 15))

    def create_graph(self):
        """
        :return: create and show the graph
        """
        if self.is_plot:
            self.plt.plot(self.x_val, self.y_val)
        else:
            self.plt.scatter(self.x_val, self.y_val)
        self.plt.show()

    def create_graph_multiple(self, x_val_bis, y_val_bis):
        """
        :param y_val_bis:
        :param x_val_bis:
        :return: create and show the graph
        """
        if self.is_plot:
            plt.plot(self.x_val, self.y_val)
            plt.plot(x_val_bis, y_val_bis)
        else:
            plt.scatter(self.x_val, self.y_val)
            plt.scatter(x_val_bis, y_val_bis)
        plt.show()

    def multiple_throughput_graph(self, databis):
        """
        :param databis:
        :return: plot graph and show the graph (with the cusum graph)
        """
        x_valBis = [x[0] for x in databis]
        y_valBis = [x[1] for x in databis]
        self.create_graph_multiple(x_valBis, y_valBis)

    def create_graph_with_vertical_line(self, list_vertical):
        """
        :param list_vertical:
        :return: create and show the graph
        """
        if self.is_plot:
            for xv in list_vertical:
                plt.axvline(xv, color='r', linestyle='--')
        else:
            plt.scatter(self.x_val, self.y_val)
        plt.show()
