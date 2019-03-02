import io
import json
import os

from apiclient import discovery
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import requests


class Drive:
    def __init__(self):
        self.directory_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
        self.DRIVE = None
        self.authenticate()
        self._get_drive_id()

    def load_file(self):
        self._get_file_id()
        data = self.download_file()
        self.delete_file()
        return data

    def upload_file(self):
        file_metadata = {'name': 'annotations.json', 'parents': [self.team_drive_id]}
        media = MediaFileUpload(self.directory_path + 'annotations.json')
        file = self.DRIVE.files().create(body=file_metadata,
                                         media_body=media,
                                         fields='id',
                                         supportsTeamDrives=True).execute()
        print('File ID: %s' % file.get('id'))

    def authenticate(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage(self.directory_path+'storage.json')
        creds = store.get()
        if not creds or creds.invalid or creds.access_token_expired:
            client_id = self.directory_path + 'client_id.json'
            flow = client.flow_from_clientsecrets(client_id, SCOPES)
            creds = tools.run_flow(flow, store)
        self.DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
        self.token = creds.access_token

    def _get_drive_id(self):
        response = self.DRIVE.teamdrives().list().execute()
        for drive in response.get('teamDrives', []):
            if drive['name'] == "Captions":
                self.team_drive_id = drive['id']

    def _get_file_id(self):
        response = self.DRIVE.files().list(includeTeamDriveItems=True,
                                           teamDriveId=self.team_drive_id,
                                           corpora='teamDrive',
                                           supportsTeamDrives=True).execute()
        for file in response.get('files', []):
            if file['name'] == "annotations.json":
                self.file_id = file['id']
                return True
        raise FileNotFoundError("File is in use now. Please make sure whether one of your team is using it or not")

    def download_file(self):
        request = self.DRIVE.files().get_media(fileId=self.file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        my_json = fh.getvalue().decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        with open(self.directory_path + 'annotations.json', 'w') as outfile:
            json.dump(data, outfile)
        return data

    def delete_file(self):
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        params = {'supportsTeamDrives': True}
        data = '{}'
        response = requests.delete('https://www.googleapis.com/drive/v3/files/' + self.file_id, headers=headers,
                                   data=data, params=params)
        if response.status_code != 204:
            return False
        return True


# try:
#     d = Drive()
#     # d.load_file()
#     d.upload_file()
# except FileNotFoundError as error:
#     print(error)
