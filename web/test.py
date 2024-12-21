import requests

url = 'http://localhost:8083/upload_image_data'
# image_file = open('test.jpg', 'rb')
data = {'group_id': '0', 'group_index': '2', 'type': 'happy'}

for i in range(100):
    data['group_index'] = str(i+3)
    if i % 33 == 0:
        data['type'] = 'unhappy'
    response = requests.post(url, data=data)


