from urllib import request
import json
import time
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
"""
def filter_train_by_time(train_arr, arr_after_time = "5:00",arr_before_time = '9:00'):
    arrive_time_index = 10
    def get_min(time_str):
        h,m = time_str.split(':')
        return int(h) * 60 + int(m)
    def is_late(train):
        return get_min(train[arrive_time_index]) > get_min(arr_before_time)
    return filter(is_late, train_arr)

def read_station():
    f = open('./station.json', 'r', encoding='utf-8')
    sts = f.read()
    return json.loads(sts)

start = input('从哪里来:')
to = input('到哪里去:')
start = start or '上海'
to = to or '新乡'
stations = read_station()
print('%s => %s' %(stations[start], stations[to]))
while True:
    with request.urlopen('https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-02-10&leftTicketDTO.from_station='+ stations[start]+'&leftTicketDTO.to_station='+stations[to]+'&purpose_codes=ADULT') as f:
        data = f.read()
        stations = read_station()
        print('Status:', f.status, f.reason)
        
        
        # for k, v in f.getheaders():
        #     print('%s: %s' % (k, v))
        # print('Data:', data.decode('utf-8'))
        info = json.loads(data.decode('utf-8'))
        trains = aoa(info['data']['result'])
        print(len(trains))
        print(len(list(filter_train_by_time(trains))))
        sites = {"软卧":23,"无座":26,"硬卧":28,"硬座":29,"二等":30,"一等":31,"商务":32}
        # print('硬卧:%s,硬座:%s,无座:%s'%(k1102[sites["硬卧"]] , k1102[sites["硬座"]] , k1102[sites["无座"]]))
        # if k1102[sites["硬卧"]] != '无':
        #     print('\a\a\a\a')
        time.sleep(3)