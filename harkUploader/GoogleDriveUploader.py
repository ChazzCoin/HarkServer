from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)

fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in fileList:
    fileID = file['id']
  # print('Title: %s, ID: %s' % (file['title'], file['id']))
  # # Get the folder ID that you want
  # if(file['title'] == "To Share"):
  #     fileID = file['id']

def upload_pdf(file_path):
    file1 = drive.CreateFile({"mimeType": "application/pdf", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
    file1.SetContentFile(file_path)
    file1.Upload() # Upload the file.