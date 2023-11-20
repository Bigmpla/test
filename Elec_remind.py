import json
import datetime
import requests
from bs4 import BeautifulSoup


Corp_id = "ww989a7dcf4297db97"
Secret = "H1L8q7P5Kt7N_qivtK8kc9PhPs0Qmev1U98_E0nlt_8"


"""

获取宿舍用电信息

"""
def get_left_electricity():
    url = 'http://192.168.84.3:9090/cgcSims/selectList.do'

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding':'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '173',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=CD3F89ABD4C2CB9AF711994CE9BF4CC7',
        'Host': '192.168.84.3:9090',
        'Origin': 'http://192.168.84.3:9090',
        'Referer': 'http://192.168.84.3:9090/cgcSims/selectList.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
    }

    data = {
        'hiddenType': '',
        'isHost': '0',
        'beginTime': '',
        'endTime': '',
        'type': '2',
        'client': '192.168.84.87',
        'roomId': '19126',
        'roomName': '1413',
        'building': ''
    }

    today = datetime.date.today();
    yesterday = today - datetime.timedelta(days=1)
    data['beginTime'],data['endTime'] = yesterday,today

    respond = requests.post(url=url, data=data, headers=headers)
    soup = BeautifulSoup(respond.text, "html.parser")
    td_contents = [td.get_text(strip=True) for td in soup.select('td[align="center"]')]
    header = td_contents[:6]
    rows = [td_contents[i:i + 6] for i in range(6, len(td_contents), 6)]

    # print(rows)
    # print(header)

    return rows
# def get_access_token():
#     get_act_url="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(Corp_id,Secret)
#     act_res=requests.get(url=get_act_url).json()
#
#     access_token=act_res["access_token"]
#     return access_token

"""

发送消息

"""

def send_message(message):
    # url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token
    url ="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=3d14b29e-78d6-4281-b129-3334b25ac9f8"
    header = {
        "Content-Type": "application/json"
    }

    if(float(message[0][3]) < 10):
        message1 = f'SOS!!!!!!!!!!!!!!!   宿舍{message[0][2]}于{message[1][0]}剩余电量{message[0][3]},不足20度电，速度充电！！！'
    else:
        message1 = f'宿舍{message[0][2]}于{message[1][0]}剩余电量{message[0][3]}'

    data1 ={
            "msgtype": "text",
            "text": {
                "content": message1,
                "mentioned_list": ["@all"],
            }
    }
    print(message1)
    respond = requests.post(url = url, data = json.dumps(data1).encode('utf-8'),headers= header)
    print(respond.text)

    if respond.status_code != 200:
        print("request failed!")
        return
    return json.loads(respond.content)

if __name__ == "__main__":
    message = get_left_electricity()
    send_message(message)



