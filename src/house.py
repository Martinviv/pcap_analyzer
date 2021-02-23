from scipy import stats


class House:

    def __init__(self):
        self.threshold_camera_up = None
        self.threshold_camera_down = None
        self.in_same_room = 0
        self.first = True

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

    def check_with_last_threshold(self, distribution_1, distribution_2):

        if self.threshold_camera_down is None:
            if abs(distribution_1.mean < distribution_2.mean):
                self.threshold_camera_down = distribution_1
                self.threshold_camera_up = distribution_2
            else:
                self.threshold_camera_down = distribution_2
                self.threshold_camera_up = distribution_1
                print('register distribution')

        elif abs(distribution_1.mean - self.threshold_camera_down.mean) < abs(distribution_2.mean -
                                                                              self.threshold_camera_down.mean) :
            stat_1, pval_1 = self.compare_threshold_down(distribution_1)
            stat_2, pval_2 = self.compare_threshold_up(distribution_2)
            print('-----------------------')
            print(distribution_2.mean)
            print(self.threshold_camera_up.mean)
            print(distribution_1.mean)
            print(self.threshold_camera_down.mean)
            print(pval_2)
            print(pval_1)
            print('-----------------------')
            return self.test_h0_bivalue(pval_1, pval_2)

        else:
            stat_1, pval_1 = self.compare_threshold_up(distribution_1)
            stat_2, pval_2 = self.compare_threshold_down(distribution_2)
            print('-----------------------')
            print(distribution_1.mean)
            print(self.threshold_camera_up.mean)
            print(distribution_2.mean)
            print(self.threshold_camera_down.mean)
            print(pval_2)
            print(pval_1)
            print('-----------------------')
            return self.test_h0_bivalue(pval_1, pval_2)

    def test_h0_bivalue(self, pval_1, pval_2):
        alpha = 0.05
        if pval_1 and pval_2 > alpha / 2:
            print('H0 accepted ->pattern recognized')
            return True
        else:
            print('H0 rejected')
            return False

    def pattern_compare(self, distribution_1, distribution_2):
        is_recognize = self.check_with_last_threshold(distribution_1, distribution_2)

        if is_recognize:
            if distribution_1.mean < distribution_2.mean:
                self.threshold_camera_down = distribution_1
                self.threshold_camera_up = distribution_2
            else:
                self.threshold_camera_down = distribution_2
                self.threshold_camera_up = distribution_1
            self.in_same_room = self.in_same_room + 1
            print('increase')
            return True
        else:
            if self.first:
                self.first = False
            elif self.in_same_room > 1:
                self.in_same_room = self.in_same_room - 1
            else:
                self.threshold_camera_down = None
                self.threshold_camera_up = None
                self.first = True
                self.in_same_room = 0
                print('reset threshold')
            print('not in same room' + str(self.in_same_room))
            return False
