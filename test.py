from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io


def services_func():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'C:/Users/Admin/Desktop/supra/tBOt/op1.json'


    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service

def list_file():
    pp = pprint.PrettyPrinter(indent=4)

    service = services_func()
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()

    pp.pprint(results['files'])

    drive_list = ''
    for i in results['files']:
        drive_list += i['name'] + '\n'
            
    return drive_list


def download_file():
    service = services_func() # подключение к базе

    file_id = '1PwHSXKjDhVhqo5AVT_382fbP8W2afgZZ9FYg5yDG6hI' # id файла
    request = service.files().export_media(fileId=file_id,
                            mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') # подключение к файлу
    filename = 'Teet.xlsx'
    fh = io.FileIO(filename, 'wb') 

    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk() # скачивание файла по кусочкам
        print ("Download %d%%." % int(status.progress() * 100))

def dwl_file():
    pp = pprint.PrettyPrinter(indent=4)
    service = services_func()
    folder_id = '1ilt5P9s5JWBT9h3KOIi3u8EpxgK_vx2p'
    name = 'create_db.py'
    file_path = 'create_db.py'
    file_metadata = {
                    'name': name,
                    'parents': [folder_id]
                }
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    pp.pprint(r)

if __name__ == '__main__':
    dwl_file()