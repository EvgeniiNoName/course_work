import requests
from pprint import pprint

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""        
        file_name = file_path.split('\\')[-1]  # получаем имя файла из его пути
        headers = {"Authorization": self.token}

        # запрос на создание файла на Яндекс.Диске
        response = requests.get(
            'https://cloud-api.yandex.net/v1/disk/resources/upload',
            headers=headers,
            params={'path': file_name, 'overwrite': True}
        )

        # получаем ссылку для загрузки файла       
        href = response.json()["href"]

        # отправляем файл на Яндекс.Диск 
        response = requests.put(
            href,
            files = {"file": open(path_to_file, 'rb')}            
        )        


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = input("Введите путь до файла")
    token = input("Введите токен")
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)