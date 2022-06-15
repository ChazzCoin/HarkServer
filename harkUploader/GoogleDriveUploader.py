from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

gauth = GoogleAuth()
# gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)

temp = []
fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in fileList:
    fileID = file['id']
    temp.append(fileID)

file = None
f"{os.path.join(os.path.dirname(__file__), 'stocks.csv')}"
for x in os.listdir("Users/chazzromeo/"):
    if x.endswith(".pdf"):
        file = x



def upload_pdf(file_path):
    file1 = drive.CreateFile({'title': file_path})
    # file1 = drive.CreateFile({"mimeType": "application/pdf", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
    file1.SetContentFile(file_path)
    file1.Upload() # Upload the file.


upload_pdf(file)
