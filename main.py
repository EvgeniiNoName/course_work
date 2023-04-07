import datetime
import requests
import json
import os
from tqdm import tqdm

class VKdownloader:
    def __init__(self, id: str):
        self.id = id       

    def download_photos(self, id, YAtoken, count_photo):
        if count_photo > 0:
            count_photo = count_photo
        else:
            count_photo = 5

        with open('info/VKtoken.txt', 'r') as file_object:
            VKtoken = file_object.read().strip()
        url = 'https://api.vk.com/method/photos.getAll'
        params = {
            'owner_id': id,
            'access_token': VKtoken,
            'photo_sizes': '1',
            'extended': '1',
            'v':'5.131',
            'count': count_photo
            
        }
        res = requests.get(url, params=params).json()['response']['items']
        list_name_photo = []
        photo_information = []
        for item in tqdm(res):
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
                    YaUploader(YAtoken).upload(name_photo, f'photo/{name_photo}.jpg')
                    os.remove(f'photo/{name_photo}.jpg')
        with open('info_photo.json', 'w') as f:
            pass
        with open('info_photo.json', 'a') as f:
            json.dump(photo_information, f, indent=4)

class YaUploader:
    def __init__(self, YAtoken: str):
        self.YAtoken = YAtoken
        self.headers = {"Authorization": self.YAtoken}

    # создание папки на Яндекс.Диске
    def new_folder(self):
        # создание папки на Яндекс.Диске
        requests.put(
            'https://cloud-api.yandex.net/v1/disk/resources',
            headers = self.headers,
            params={'path': 'photo'}
        )         

    def upload(self, name_photo, ph):
        # запрос на создание файла на Яндекс.Диске
        response = requests.get(
            'https://cloud-api.yandex.net/v1/disk/resources/upload',
            headers = self.headers,
            params={'path': 'photo/' + str(name_photo) + '.jpg', 'overwrite': True}
        )

        # получаем ссылку для загрузки файла       
        href = response.json()["href"]

        # отправляем файл на Яндекс.Диск 
        response = requests.put(
            href,
            files = {"file": open(ph, 'rb')}            
        )  

if __name__ == '__main__':
    YAtoken = input("Введите токен: ")    
    id = input("Введите ID пользователя: ")
    count = int(input('Введите количество фотографий (по умолчанию 5): '))
    new_folder = YaUploader(YAtoken).new_folder()
    downloader = VKdownloader(id).download_photos(id, YAtoken, count)