from urllib import request
import json
import time
import re
"""
将车次字符串转换成数组
"""
def aoa(train):
    result = []
    if len(train):
        for st in train:
            result.append(st.split('|'))
        return result
    return None
"""
过滤掉时间不合适的车次
3 : 车次信息
8 : 出发时间
9 : 到达时间

"""
def filter_train_by_time(train_arr, start_after = "8:00", start_before = "22:00", arr_after = "5:00", arr_before = '10:00'):
    arrive_time_index = 9
    start_time_index = 8
    def get_min(time_str):
        h, m = time_str.split(':')
        return int(h) * 60 + int(m)
    early = get_min(arr_after)
    late = get_min(arr_before)
    start_early = get_min(start_after)
    start_late = get_min(start_before)
    def is_good(train):
        return  early < get_min(train[arrive_time_index]) < late and start_early < get_min(train[start_time_index]) < start_late
    return filter(is_good, train_arr)

def read_station():
    f = open('./station.json', 'r', encoding='utf-8')
    sts = f.read()
    return json.loads(sts)

start = input('从哪里来:')
to = input('到哪里去:')

start = start or '上海'
to = to or '郑州'
date = '2018-02-13'
stations = read_station()# 车站和车站代码的转换
sites = {"软卧":23,"无座":26,"硬卧":28,"硬座":29,"二等":30,"一等":31,"商务":32}# 数据的索引
sleep = 2# 请求时间间隔
counter = 0
print('%s => %s' %(stations[start], stations[to]))

while True:
    with request.urlopen('https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' + date + '&leftTicketDTO.from_station='+ stations[start]+'&leftTicketDTO.to_station='+stations[to]+'&purpose_codes=ADULT') as f:
        try:
            data = f.read()
        except:
            print('read err')
        stations = read_station()
        print('Status:', f.status, f.reason)
        try: 
            info = json.loads(data.decode('utf-8'))
            trains = aoa(info['data']['result'])
            print('所有车次', len(trains))
            good_trains = filter_train_by_time(trains)
            # print('符合条件的车次',list(map(lambda item : item[3], good_trains)))# 符合时间段的车次信息
            for train in good_trains:
                yw, yz, wz, ed, yd = train[sites['硬卧']], train[sites['硬座']], train[sites['无座']], train[sites['二等']],  train[sites['一等']]
                if re.match(r'有|\d+',yw):
                    print('%s 硬卧有票'%(train[3]))
                    print('\a')
                elif re.match(r'有|\d+',yz):
                    print('%s 硬座有票'%(train[3]))
                    print('\a')
                elif re.match(r'有|\d+', ed):
                    print('%s 二等座有票'%(train[3]))
                    print('\a')
        except json.decoder.JSONDecodeError as e:
            print('err')
        counter += 1
        print('====已查询%d次===='%(counter))
        time.sleep(sleep)