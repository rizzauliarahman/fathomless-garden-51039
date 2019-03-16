import pickle
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import matplotlib.pyplot as plt


SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", mode="rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server()

        with open("token.pickle", mode="wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v2", credentials=creds)

    folder_id = "1tN8U5L1pspnhZuCoJht7yW7FTRsE5-WJ"

    results = service.children().list(folderId=folder_id).execute()
    items = results.get("items", [])

    if not items:
        print("No files")
    else:
        print("Files:")
        for item in items:
            print("File Id: %s" % item['id'])

    for item in items:
        file = service.files().get(fileId=str(item['id'])).execute()
        print("\nTitle: %s" % file['title'])
        print("File ID: %s" % file['id'])
        print("MIME Type: %s" % file['mimeType'])

    # request = service.files().get_media(fileId=str(items[0]['id']))
    # svfile = open(file['title'], mode="wb")
    # media_request = MediaIoBaseDownload(svfile, request)
    #
    # while True:
    #     try:
    #         download_progress, done = media_request.next_chunk()
    #     except errors.HttpError:
    #         print('An error occurred')
    #         return
    #
    #     img = plt.imread(file['title'])
    #
    #     plt.imshow(img)
    #     plt.show()
    #
    #     return


if __name__ == '__main__':
    main()
