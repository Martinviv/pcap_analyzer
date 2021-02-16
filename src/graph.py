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
        self.plt = plt
        self.plt.figure(figsize=(14, 14))
        self.plt.grid()
        self.plt.title(title)


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

    def add_graph(self, graphic):
        """
        not working
        :param graphic:
        :return: plot graph and show the graph (with the cusum graph)
        """

        if graphic.is_plot:
            self.plt.plot(graphic.x_val, graphic.y_val)
        else:
            self.plt.scatter(graphic.x_val, graphic.y_val)

    def add_data(self, data):
        x_val = [x[0] for x in data]
        y_val = [x[1] for x in data]
        if self.is_plot:
            self.plt.plot(x_val, y_val)
        else:
            self.plt.scatter(x_val, y_val)

    def add_vertical_line(self, list_vertical):
        """
        :param list_vertical:
        :return: create and show the graph
        """
        if self.is_plot:
            for xv in list_vertical:
                plt.axvline(xv, color='r', linestyle='--')
        else:
            plt.scatter(self.x_val, self.y_val)

    def show_graph(self):
        self.plt.show()
