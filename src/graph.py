import matplotlib.pyplot as plt
import analysis_packet
import analysis_data


class Graph:

    def __init__(self, data, leg_x, leg_y, title, is_plot, legend):
        self.data = data
        self.leg_x = leg_x
        self.leg_y = leg_y
        self.legend = legend
        self.is_plot = is_plot
        self.x_val = [x[0] for x in data]
        self.y_val = [x[1] for x in data]
        self.plt = plt
        # figsize 14,14 for better quality
        self.fig = self.plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()
        self.plt.title(title)

    def size_payload_graph(self, protocol):
        """
        :param protocol: TCP or UDP
        :param list[(x,y)] data:  x timestamps that start the interval and y is number of packets for each interval
        :return: set of coordinates where x time and y tcp payload size (no return) and show graph
        """
        # TODO : update with new signature
        self.y_val = [analysis_packet.get_tcp_payload_size(x[1], protocol) for x in self.data]
        self.create_graph()
        self.show_graph()

        # TODO : update with new signature
        self.ax.scatter(analysis_data.smooth(self.x_val, 15), analysis_data.smooth(self.y_val, 15))
        self.show_graph()

    def create_graph(self):
        """
        :return: create and show the graph
        """
        if self.is_plot:
            self.ax.plot(self.x_val, self.y_val, label=self.legend)
        else:
            self.ax.scatter(self.x_val, self.y_val, label=self.legend)

    def add_data(self, data, legend):
        x_val = [x[0] for x in data]
        y_val = [x[1] for x in data]
        if self.is_plot:
            self.ax.plot(x_val, y_val, label=legend)
        else:
            self.ax.scatter(x_val, y_val, label=legend)

    def add_vertical_line(self, list_vertical, legend):
        """
        :param legend:
        :param list_vertical:
        :return: create and show the graph
        """
        for xv in list_vertical:
            self.ax.axvline(xv, color='r', linestyle='--')

    def show_graph(self):
        self.fig.legend(loc="upper left")
        self.plt.show()
