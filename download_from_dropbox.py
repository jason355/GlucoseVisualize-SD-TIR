import dropbox 
import datetime
import gzip
import shutil
# 設置 Dropbox API 令牌
TOKEN = input("Enter api key>")

def download_file_from_dropbox(dropbox_path, local_path):
    dbx = dropbox.Dropbox(TOKEN)

    try:
        metadata, res = dbx.files_download(dropbox_path)
        with open(local_path, 'wb') as f:
            f.write(res.content)
        print(f'File downloaded successfully to {local_path}')
    except dropbox.exceptions.ApiError as err:
        print(f'Error downloading file from Dropbox: {err}')


def extract_gz(gz_path, extract_to_path):
    try:
        with gzip.open(gz_path, 'rb') as f_in:
            with open(extract_to_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"File extracted successfully to {extract_to_path}")
    except Exception as e:
        print(f"Error extraction file: {e}")




