import json
import random
import time
from datetime import datetime

import requests

def test_single_upload():
    url = 'http://localhost:8083/upload_image_data'
    # image_file = open('test.jpg', 'rb')
    data = {'group_id': '2', 'group_index': '0', 'type': 'happy', 'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}

    for i in range(100):
        data['group_index'] = str(i)
        data['type'] = 'normal'
        if random.randint(0, 100) < 20:
            data['type'] = 'happy'
        if random.randint(0, 100) < 10:
            data['type'] = 'angry'
        if random.randint(0, 100) < 10:
            data['type'] = 'sad'
        response = requests.post(url, data=data)
        print(response.text)

def test_group_upload():
    datas = []
    for i in range(100):
        temp_data = {'group_index': str(i), 'type': 'normal', 'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}
        if random.randint(0, 100) < 20:
            temp_data['type'] = 'happy'
        if random.randint(0, 100) < 10:
            temp_data['type'] = 'angry'
        if random.randint(0, 100) < 10:
            temp_data['type'] = 'sad'
        datas.append(temp_data)
        time.sleep(0.1)
    url = 'http://localhost:8083/upload_group_image_data'
    json_data = json.dumps(datas)
    # print(json_data)
    response = requests.post(url, json=json_data)
    print(response.text)

if __name__ == '__main__':
    test_group_upload()