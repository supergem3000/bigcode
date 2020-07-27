import numpy as np
from sklearn.cluster import KMeans
from Storage import Storage
from Output import Output
from ProgressBar import ProgressBar
class Analyser:

    def __init__(self, storage: Storage):
        super().__init__()
        self.__storage = storage

    def __cluster_sort(self, case_cluster):
        return sorted(case_cluster, key=lambda x: x['center'][0])

    def kmeans(self):
        km_name = []
        km_data = []
        case_dict = self.__storage.get_case_dict()
        progressbar = ProgressBar('计算题目难度', 1)
        for case_id in case_dict.keys():
            km_name.append(case_id)
            records = np.array(case_dict[case_id]['records'])
            scores = np.array(case_dict[case_id]['scores'])
            km_data.append([records.mean(), case_dict[case_id]['avg_times'], records.std(), scores.std(), scores.mean()])
        km_data = np.array(km_data)
        km = KMeans(n_clusters=5)
        label = km.fit_predict(km_data)
        centers = km.cluster_centers_
        case_cluster = [{'center': centers[i], 'cases': []} for i in range(0, 5)]
        for i in range(0, len(km_name)):
            case_cluster[label[i]]['cases'].append(km_name[i])
        case_cluster = self.__cluster_sort(case_cluster)
        progressbar.progress()
        self.__storage.set_case_cluster(case_cluster)
        self.__storage.set_km_data(km_data)
        self.__storage.set_label(label)

    def calc_total_weight(self):
        weight = [2, 1.5, 1, 0.8, 0.5]
        group_weight = [{}, {}, {}, {}, {}]
        case_dict = self.__storage.get_case_dict()
        case_group_dict = self.__storage.get_case_group_dict()
        case_cluster = self.__storage.get_case_cluster()
        progressbar = ProgressBar('计算各组总难度权重', len(case_dict))
        for case_id in case_dict.keys():
            group_list = case_group_dict[case_id]
            case_type = case_dict[case_id]['type']
            case_weight = -1
            for i in range(0, 5):
                if case_id in case_cluster[i]['cases']:
                    case_weight = weight[i]
                    break
            for group in group_list:
                if not (case_type in group_weight[group]):
                    group_weight[group][case_type] = 0
                group_weight[group][case_type] += case_weight
            progressbar.progress()
        self.__storage.set_group_weight(group_weight)

    def calc_user_result(self):
        types = ['字符串', '线性表', '数组', '查找算法', '排序算法', '数字操作', '树结构', '图结构']
        weight = [2, 1.5, 1, 0.8, 0.5]
        group_weight = self.__storage.get_group_weight()
        user_dict = self.__storage.get_user_dict()
        case_dict = self.__storage.get_case_dict()
        user_group_dict = self.__storage.get_user_group_dict()
        case_cluster = self.__storage.get_case_cluster()
        user_result = {}
        progressbar = ProgressBar('计算用户得分结果', len(user_dict))
        for user_id in user_dict.keys():
            user = {}
            cases = user_dict[user_id]
            for case_id in cases.keys():
                case_type = cases[case_id]['type']
                final_score = cases[case_id]['final_score']
                if not case_type in user:
                    user[case_type] = []
                case_weight = -1
                for i in range(0, 5):
                    if case_id in case_cluster[i]['cases']:
                        case_weight = weight[i]
                        break
                a = np.array(case_dict[case_id]['records'])
                # 用户在这题的提交平均分和所有人在这题的提交平均分之差
                score_d = (cases[case_id]['avg_score'] - a.mean()) * 0.5
                # 所有人在这题的提交平均提交次数和用户在这题的提交次数之差
                times_d = case_dict[case_id]['avg_times'] - cases[case_id]['record_num']
                # 以本题final_score为主要依据，根据上述两个差对得分进行浮动
                score = final_score + (min(15, score_d) if score_d >= 0 else max(-15, score_d))
                score = score + (min(5, times_d) if times_d >= 0 else max(-5, times_d))
                score = score + cases[case_id]['lint_score']
                # 得分区间在[0,100]内，再乘以权重
                score = min(100, max(0, score /1.3)) * case_weight
                user[case_type].append(score)
            user_result[user_id] = {}
            group_id = user_group_dict[user_id]
            for case_type in user.keys():
                total_score = 0
                total_weight = group_weight[group_id][case_type]
                for score in user[case_type]:
                    total_score += score
                user_result[user_id][case_type] = total_score / total_weight
            for ty in types:
                if ty not in user_result[user_id]:
                    user_result[user_id][ty] = 0
            progressbar.progress()
        self.__storage.set_user_result(user_result)
