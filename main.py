import datetime
import requests
import json
from pprint import pprint
from tqdm import tqdm

class VKdownloader:
    def __init__(self, id: str):
        self.id = id       

    def download_photos(self, id, count_photo):
        if count_photo > 0:
            count_photo = count_photo
        else:
            count_photo = 5

        with open('info/token_VK.txt', 'r') as file_object:
            token_VK = file_object.read().strip()
        url = 'https://api.vk.com/method/photos.getAll'
        params = {
            'owner_id': id,
            'access_token': token_VK,
            'photo_sizes': '1',
            'extended': '1',
            'v':'5.131',
            'count': count_photo            
        }
        res = requests.get(url, params=params).json()['response']['items']
        dict_photo = {}
        list_name_photo = []
        photo_information = []
        for item in  res:
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
                    dict_photo[name_photo] = size['url']
        with open('info_photo.json', 'w') as f:
            pass
        with open('info_photo.json', 'a') as f:
            json.dump(photo_information, f, indent=4)
        return dict_photo

class YaUploader:
    def __init__(self, token_YA: str):
        self.token_YA = token_YA
        self.headers = {"Authorization": self.token_YA}

    def new_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        requests.put(
            url,
            headers = self.headers,
            params={'path': folder.split('/')[0]}
        )
        requests.put(
            url,
            headers = self.headers,
            params={'path': folder}            
        )
     
    def upload(self, dict_photo, folder):
        for name_photo, url_photo in tqdm(dict_photo.items()):
            path_photo = folder + '/' + str(name_photo) + '.jpg'
            requests.post(
                'https://cloud-api.yandex.net/v1/disk/resources/upload',
                headers = self.headers,
                params={'path': path_photo, 'url': url_photo}
            )          

if __name__ == '__main__':
    token_YA = input("Введите токен: ")   
    id = input("Введите ID пользователя: ")
    count = int(input('Введите количество фотографий (по умолчанию 5): '))
    folder = 'BackUp/'+ str(id) + '_' + str(datetime.datetime.now().strftime('%y-%m-%d %H-%M-%S'))
    YaUploader(token_YA).new_folder(folder)
    downloader = VKdownloader(id).download_photos(id, count)
    YaUploader(token_YA).upload(downloader)
   