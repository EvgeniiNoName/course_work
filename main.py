import datetime
import requests
from pprint import pprint
import json


with open('info/VKtoken.txt', 'r') as file_object:
    VKtoken = file_object.read().strip()

id = 8147359

# def save_info_photo(name_photo, size):
#     photo_information = []
#     photo_information.append({
#         'file_name': str(name_photo) + '.jpg',
#         'size': size
#     })
#     with open('info_photo.json', 'a') as f:
#         json.dump(photo_information, f, indent=4) 


def download_photos(id, VKtoken):
    url = 'https://api.vk.com/method/photos.getAll'
    params = {
        'owner_id': id,
        'access_token': VKtoken,
        'photo_sizes': '1',
        'extended': '1',
        'v':'5.131'
    }
    res = requests.get(url, params=params).json()['response']['items']
    list_name_photo = []
    photo_information = []
    for item in res:
        name_photo = item['likes']['count']
        if name_photo in list_name_photo:
            date = datetime.date.fromtimestamp(item['date'])
            name_photo = f'{name_photo}_{date}'
        for size in item['sizes']:
            if size['type'] == 'z':
                list_name_photo.append(name_photo)
                photo_information.append({
                    'file_name': str(name_photo) + '.jpg',
                    'size': size['type']
                })
                with open(f'photo/{name_photo}.jpg', 'wb') as ph:
                    ph.write(requests.get(size['url']).content)
    with open('info_photo.json', 'a') as f:
        json.dump(photo_information, f, indent=4)

download_photos(id, VKtoken)