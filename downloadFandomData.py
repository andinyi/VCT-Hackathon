import requests
import gzip
import shutil
import os
from io import BytesIO

S3_BUCKET_URL = "https://vcthackathon-data.s3.us-west-2.amazonaws.com"

FOLDER = "fandom"

def download_gzip_and_write_to_xml(file_name):
    if os.path.isfile(f"{file_name}.xml"):
        return False

    remote_file = f"{S3_BUCKET_URL}/{file_name}.xml.gz"
    response = requests.get(remote_file, stream=True)

    if response.status_code == 200:
        gzip_bytes = BytesIO(response.content)
        with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
            with open(f"{file_name}.xml", 'wb') as output_file:
                shutil.copyfileobj(gzipped_file, output_file)
            print(f"{file_name}.xml written")
        return True
    elif response.status_code == 404:
        # Ignore
        return False
    else:
        print(response)
        print(f"Failed to download {file_name}")
        return False


def download_fandom_files():
    directory = f"{FOLDER}"

    if not os.path.exists(directory):
        os.makedirs(directory)

    fandom_files = ["valorant_esports_pages", "valorant_pages"]
    for file_name in fandom_files:
        download_gzip_and_write_to_xml(f"{directory}/{file_name}")

if __name__ == "__main__":
    download_fandom_files()
