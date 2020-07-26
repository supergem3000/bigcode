import os
import numpy as np
import matplotlib.pyplot as plt
from ProgressBar import ProgressBar
class Output:
    @staticmethod
    def write_case_cluster(case_cluster):
        if not os.path.exists('.\\output'):
            os.mkdir('.\\output')
        fwrite = open(".\\output\\case_cluster.txt", 'w', encoding='utf-8')
        for i in range(0, len(case_cluster)):
            for j in range(0, len(case_cluster[i]['center'])):
                fwrite.write(str(case_cluster[i]['center'][j]) + ",")
            fwrite.write('\n')
            for j in range(len(case_cluster[i]['cases'])):
                fwrite.write(str(case_cluster[i]['cases'][j]) + ', ')
                if (j % 10 == 0) and (j != 0):
                    fwrite.write('\n')
            fwrite.write('\n\n')
        fwrite.close()

    @staticmethod
    def visualize_case_cluster(km_data, label):
        if not os.path.exists('.\\pics'):
            os.mkdir('.\\pics')
        plt.scatter(km_data[:, 0], km_data[:, 1], c=label)
        plt.savefig('.\\pics\\case_cluster.png')
        plt.close()

    @staticmethod
    def visualize_user_result(user_result):
        progressbar = ProgressBar("生成用户雷达图", len(user_result))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        if not os.path.exists('.\\pics'):
            os.mkdir('.\\pics')
        for user_id in user_result.keys():
            u_data = np.array([user_result[user_id][i] for i in sorted(user_result[user_id])])
            u_label = np.array([i for i in sorted(user_result[user_id])])
            angle = np.linspace(0, 2 * np.pi, len(u_data), endpoint=False) #data里有几个数据，就把整圆360°分成几份
            angles = np.concatenate((angle, [angle[0]])) #增加第一个angle到所有angle里，以实现闭合
            u_data = np.concatenate((u_data, [u_data[0]])) #增加第一个人的第一个data到第一个人所有的data里，以实现闭合
            plt.polar(angles, u_data, 'o-', linewidth=1)
            plt.fill(angles, u_data, alpha=0.25)
            plt.thetagrids(angles * 180 / np.pi, u_label)
            plt.ylim(0, 100)
            plt.title(str(user_id))
            plt.savefig('.\\pics\\' + str(user_id) + '.png')
            plt.close()
            progressbar.progress()

    @staticmethod
    def write_user_result(user_result):
        if not os.path.exists('.\\output'):
            os.mkdir('.\\output')
        fwrite = open(".\\output\\user.txt", 'w', encoding='utf-8')
        for user in user_result.keys():
            fwrite.write(str(user) + '\n')
            for type_key in user_result[user].keys():
                fwrite.write(type_key + ' ' + str(user_result[user][type_key]) + '\n')
        fwrite.close()

    @staticmethod
    def write_code_lint(out_str, user_id, case_id):
        if not os.path.exists('.\\output\\lint\\' + str(user_id)):
            os.makedirs('.\\output\\lint\\' + str(user_id))
        fwrite = open('.\\output\\lint\\' + str(user_id) + '\\' + str(case_id) + '.txt', 'w', encoding='utf-8')
        fwrite.write(out_str)
        fwrite.close()
