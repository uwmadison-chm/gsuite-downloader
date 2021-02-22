import pickle
import io
import os.path
from pathlib import Path
import argparse
import coloredlogs
import logging
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

def init_service():
    """
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Cache discovery has troubles sometimes
    return build('drive', 'v3', credentials=creds, cache_discovery=False)

def search_named(service, pattern):
    page_token = None
    files = []
    while True:
        results = service.files().list(
            q=f"name contains '{pattern}'",
            pageSize=20, fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token).execute()
        for f in results.get('files', []):
            files.append((f.get('id'), f.get('mimeType'), f.get('name')))

        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break

    return files

def download_file(service, file_id, mime_type, name, path, include_dates=False):
    if include_dates:
        now = datetime.datetime.now()
        output_path = path / (name + f" - {now:%Y%m%d_%H_%M}.xlsx")
    else:
        output_path = path / (name + ".xlsx")
    if "google-apps.spreadsheet" in mime_type:
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    logging.info(f"Attempting to download {name} ({file_id}) to {output_path} using mimeType {mime_type}")
    request = service.files().export_media(fileId=file_id, mimeType=mime_type)
    fh = io.FileIO(output_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        logging.debug(f"Download {int(status.progress() * 100)}% complete")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', help='Pattern of files to download')
    parser.add_argument('-v', '--verbose', action='count')
    parser.add_argument('-d', '--dates', action='store_true', help='Modify file name to include date')
    parser.add_argument('-o', '--output', default='.', help='Path to store downloads in')
    args = parser.parse_args()

    if args.verbose:
        if args.verbose > 1:
            coloredlogs.install(level='DEBUG')
        elif args.verbose > 0:
            coloredlogs.install(level='INFO')
    else:
        coloredlogs.install(level='WARN')

    service = init_service()
    to_download = search_named(service, args.pattern)
    output = Path(args.output)
    for file_id, mime_type, name in to_download:
        download_file(service, file_id, mime_type, name, output, include_dates=args.dates)

if __name__ == '__main__':
    main()
