import json
class Storage:

    def __init__(self, file):
        super().__init__()
        f = open(file, encoding='utf-8')
        res = json.loads(f.read())
        self.__data = res.values()
        self.__case_group = {}
        self.__user_group = {}
        self.__case_group_dict = {}
        self.__user_group_dict = {}
        self.__case_dict = {}
        self.__user_dict = {}
        self.__case_cluster = []
        self.__km_data = []
        self.__label = []
        self.__group_weight = []
        self.__user_result = {}

    def set_data(self, data):
        self.__data = data

    def get_data(self):
        return self.__data

    def set_case_group(self, case_group):
        self.__case_group = case_group

    def get_case_group(self):
        return self.__case_group

    def set_user_group(self, user_group):
        self.__user_group = user_group

    def get_user_group(self):
        return self.__user_group

    def set_case_group_dict(self, case_group_dict):
        self.__case_group_dict = case_group_dict

    def get_case_group_dict(self):
        return self.__case_group_dict

    def set_user_group_dict(self, user_group_dict):
        self.__user_group_dict = user_group_dict

    def get_user_group_dict(self):
        return self.__user_group_dict

    def set_case_dict(self, case_dict):
        self.__case_dict = case_dict

    def get_case_dict(self):
        return self.__case_dict

    def set_user_dict(self, user_dict):
        self.__user_dict = user_dict

    def get_user_dict(self):
        return self.__user_dict

    def set_case_cluster(self, case_cluster):
        self.__case_cluster = case_cluster

    def get_case_cluster(self):
        return self.__case_cluster

    def set_km_data(self, km_data):
        self.__km_data = km_data

    def get_km_data(self):
        return self.__km_data

    def set_label(self, label):
        self.__label = label

    def get_label(self):
        return self.__label

    def set_group_weight(self, group_weight):
        self.__group_weight = group_weight

    def get_group_weight(self):
        return self.__group_weight

    def set_user_result(self, user_result):
        self.__user_result = user_result

    def get_user_result(self):
        return self.__user_result
