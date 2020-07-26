import json
import urllib.parse, urllib.request
import os
import zipfile

f = open('test_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)
if not os.path.exists('.\\tmp'):
    os.mkdir('.\\tmp')
if not os.path.exists('.\\codes'):
    os.mkdir('.\\codes')
for user in data.values():
    user_id = user['user_id']
    cases = user['cases']
    if len(cases) < 100:
        continue
    # tmp\user文件夹
    if not os.path.exists('.\\tmp\\' + str(user_id)):
        os.mkdir('.\\tmp\\' + str(user_id))
    for case in cases:
        case_id = case['case_id'] + case['case_type']

        if len(case['upload_records']) == 0: # 莫名奇妙的有分数但没提交记录
            continue

        upload_record = case['upload_records'][len(case['upload_records']) - 1]
        code_zip_name = str(case_id) + '.zip'
        code_url = upload_record['code_url']
        if not os.path.isfile('.\\codes\\' + str(user_id) + '\\'+str(case_id) + '\\' + 'main.py'):
            try:
                urllib.request.urlretrieve(code_url, '.\\tmp\\' + str(user_id) + '\\' + code_zip_name)
                print('下载' + '.\\tmp\\' + str(user_id) + '\\'+code_zip_name)
                # 脑残zip套zip解压
                z = zipfile.ZipFile('.\\tmp\\' + str(user_id) + '\\'+code_zip_name, 'r')
                in_zip_name = z.namelist()[0]
                z.extractall('.\\tmp\\' + str(user_id) + '\\')
                result_z = zipfile.ZipFile('.\\tmp\\' + str(user_id) + '\\' + in_zip_name)
                # 最终解压到data\userid\caseid\main.py
                result_z.extract("main.py", '.\\codes\\' + str(user_id) + '\\' + str(case_id) + '\\')
                print('解压到' + '.\\codes\\' + str(user_id) + '\\' + str(case_id) + '\\')
            except Exception as e:
                print(str(e))
                print('.\\tmp\\' + str(user_id) + '\\' + code_zip_name+'下载失败')
        else:
            print('.\\codes\\'+str(user_id)+'\\'+str(case_id)+'\\'+'main.py'+'已存在')
