from urllib import request
import json
def aoa(arr):
    result = []
    if len(arr):
        for st in arr:
            result.append(st.split('|'))
        return result
def read_station():
    f = open('./station.json', 'r', encoding='utf-8')
    sts = f.read()
    return json.loads(sts)


with request.urlopen('https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-02-10&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=XXF&purpose_codes=ADULT') as f:
    data = f.read()
    stations = read_station()
    print('Status:', f.status, f.reason)
    # for k, v in f.getheaders():
    #     print('%s: %s' % (k, v))
    # print('Data:', data.decode('utf-8'))
    info = json.loads(data.decode('utf-8'))
    k1102 = aoa(info['data']['result'])[2]
    sites = {"软卧":23,"无座":26,"硬卧":28,"硬座":29,"二等":30,"一等":31,"商务":32}
    print(len(k1102))