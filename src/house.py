from scipy import stats
from distribution import Distribution


class House:

    def __init__(self):
        self.threshold_camera_up = Distribution(None, None, None)
        self.threshold_camera_down = Distribution(None, None, None)
        self.in_same_room = None

    def compare_threshold_up(self, distribution):
        statistics, pvalue = stats.ttest_ind_from_stats(self.threshold_camera_up.mean, self.threshold_camera_up.std,
                                                        self.threshold_camera_up.number_data, distribution.mean,
                                                        distribution.std, distribution.number_data, False)
        return statistics, pvalue

    def compare_threshold_down(self, distribution):
        statistics, pvalue = stats.ttest_ind_from_stats(self.threshold_camera_down.mean, self.threshold_camera_down.std,
                                                        self.threshold_camera_down.number_data, distribution.mean,
                                                        distribution.std, distribution.number_data, False)
        return statistics, pvalue

