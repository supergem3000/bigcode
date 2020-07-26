from io import StringIO
import pylint.lint
from pylint.reporters.text import TextReporter
import numpy as np
from Storage import Storage
from Output import Output
from ProgressBar import ProgressBar
class Preprocesser:

    def __init__(self, storage: Storage):
        super().__init__()
        self.__storage = storage

    def __lint(self, user_id, case_id):
        # 使用pylint检查代码质量
        file_name = '.\\codes\\' + str(user_id) + '\\' + str(case_id) + '\\main.py'
        buff = StringIO()
        reporter = TextReporter(output=buff)
        results = pylint.lint.Run([file_name], reporter=reporter, exit=False)
        try:
            score = results.linter.stats['global_note']
            out_str = buff.getvalue()
            Output.write_code_lint(out_str, user_id, case_id)
            # print(score)
            return score
        except Exception as e:
            # 总有莫名其妙 有得分却没提交记录的人，返回0分
            return 0

    def __too_many_if(self, a, b, c, d):
        delta = d - c
        if delta > 0:
            if ((c - b > delta - 0.02) and (c - b < delta + 0.02) and (b - a > delta - 0.02) and (b - a < delta + 0.02)):
                return True
        return False

    def grouping(self):
        # 用户、题目分为5个组
        case_group = [[], [], [], [], []]
        user_group = [[], [], [], [], []]
        # 字典 —— 根据题目号、用户号找组号
        case_group_dict = {}
        user_group_dict = {}
        data = self.__storage.get_data()
        progressbar = ProgressBar('分组中', 5)
        for user_data in data:
            user_id = user_data['user_id']
            # 5个用户代表5个组，手动抽取的，根据这5个用户找出每个组分的题是什么，谁分到了哪个组
            if user_id in (60636, 60762, 60692, 49823, 58616):
                for case in user_data['cases']:
                    i = len(user_group_dict)
                    case_id = case['case_id']
                    case_type = case['case_type']
                    case_id = case_id + case_type
                    if case_id in case_group_dict:
                        case_group_dict[case_id].append(i)
                    else:
                        case_group_dict[case_id] = [i]
                    case_group[i].append(case_id)
                user_group_dict[user_id] = len(user_group_dict)
                progressbar.progress()
        self.__storage.set_case_group(case_group)
        self.__storage.set_user_group(user_group)
        self.__storage.set_case_group_dict(case_group_dict)
        self.__storage.set_user_group_dict(user_group_dict)
    
    def organize(self):
        data = self.__storage.get_data()
        case_group_dict = self.__storage.get_case_group_dict()
        user_group = self.__storage.get_user_group()
        user_group_dict = self.__storage.get_user_group_dict()
        case_dict = {}
        user_dict = {}
        progressbar = ProgressBar('数据预处理与重新组织', len(data))
        for user_data in data:
            # 做了100道以下的参考意义不大，扰乱数据，舍
            if len(user_data['cases']) < 100:
                progressbar.progress()
                continue
            user_id = user_data['user_id']
            cases = user_data['cases']
            finded_group = False
            user_dict[user_id] = {}
            for case in cases:
                case_id = case['case_id']
                case_type = case['case_type']
                case_id = case_id + case_type

                # 通过查找用户做的题是哪组的题，来确定用户属于的组别
                if not finded_group:
                    if len(case_group_dict[case_id]) == 1:
                        finded_group = True
                        user_group[case_group_dict[case_id][0]].append(user_id)
                        user_group_dict[user_id] = case_group_dict[case_id][0]
                if not (case_id in case_dict):
                    case_dict[case_id] = {
                        'people_num': 0,
                        'type': case_type,
                        'records': [],
                        'avg_times': -1,
                        'scores': []
                    }
                user_dict[user_id][case_id] = {
                    'final_score': case['final_score'],
                    'type': case_type,
                    'record_num': -1,
                    'avg_score': -1,
                    'lint_score': self.__lint(user_id, case_id)
                    # 'lint_score': 10
                }
                case_dict[case_id]['people_num'] += 1
                abnormal = False
                upload_records = case['upload_records']
                num_of_records = len(upload_records)
                if num_of_records >= 4:
                    abnormal = self.__too_many_if(upload_records[num_of_records - 4]['score'],
                                                upload_records[num_of_records - 3]['score'],
                                                upload_records[num_of_records - 2]['score'],
                                                upload_records[num_of_records - 1]['score'])
                if abnormal:
                    case_dict[case_id]['scores'].append(0)
                else:
                    case_dict[case_id]['scores'].append(case['final_score'])
                t_records = []
                for upload_record in upload_records:
                    if abnormal: # 面向用例，都按0分算
                        case_dict[case_id]['records'].append(0)
                        t_records.append(0)
                        user_dict[user_id][case_id]['final_score'] = 0
                    else:
                        case_dict[case_id]['records'].append(upload_record['score'])
                        t_records.append(upload_record['score'])
                user_dict[user_id][case_id]['record_num'] = num_of_records
                a = np.array(t_records)
                user_dict[user_id][case_id]['avg_score'] = a.mean()
            progressbar.progress()
        self.__storage.set_case_dict(case_dict)
        self.__storage.set_user_dict(user_dict)

    def complement(self):
        case_dict = self.__storage.get_case_dict()
        case_group_dict = self.__storage.get_case_group_dict()
        user_group = self.__storage.get_user_group()
        progressbar = ProgressBar('数据补全', len(case_dict))
        for case_id in case_dict.keys():
            avg_times = len(case_dict[case_id]['records']) / case_dict[case_id]['people_num']
            case_dict[case_id]['avg_times'] = avg_times
            groups_of_case = case_group_dict[case_id]
            should_people_num = 0 # 算出这道题本应该有多少人做
            for group in groups_of_case:
                should_people_num += len(user_group[group])
            # 没做本题的人，每人补上平均次数个0分
            for i in range(0, int((should_people_num - case_dict[case_id]['people_num']) * avg_times)):
                case_dict[case_id]['records'].append(0)
            for i in range(0, should_people_num - case_dict[case_id]['people_num']):
                case_dict[case_id]['scores'].append(0)
            case_dict[case_id]['people_num'] = should_people_num
            progressbar.progress()
