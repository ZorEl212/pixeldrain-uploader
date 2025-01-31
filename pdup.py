import os
import requests
from tqdm import tqdm
import argparse
from base64 import b64encode
import urllib3
from urllib3.util.ssl_ import create_urllib3_context

BASE_URL = "https://pixeldrain.com/api"
FILE_URL = "https://pixeldrain.com"

# Custom HTTPS Adapter to set SNI
class SNIAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, sni_hostname, *args, **kwargs):
        self.sni_hostname = sni_hostname
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs["ssl_context"] = context
        kwargs["server_hostname"] = self.sni_hostname
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs["ssl_context"] = context
        kwargs["server_hostname"] = self.sni_hostname
        return super().proxy_manager_for(*args, **kwargs)


def upload_file_to_pixeldrain(file_name, api_key, sni_hostname):
    """
    Uploads a file to Pixeldrain using the recommended PUT method with authentication.
    """
    file_size = os.path.getsize(file_name)
    headers = {
        "Authorization": "Basic " + b64encode(f":{api_key}".encode()).decode()
    }

    # Configure requests with SNI bughost. Pixeldrain is blocked in some regions.
    session = requests.Session()
    adapter = SNIAdapter(sni_hostname=sni_hostname)
    session.mount("https://", adapter)

    with open(file_name, "rb") as file:
        with tqdm(
            total=file_size, unit="B", unit_scale=True, desc="Uploading"
        ) as t:
            # A generator to read the file in chunks. To properly update status.
            def file_chunk_reader():
                for chunk in iter(lambda: file.read(1024 * 1024), b""):  # 1 MB chunks
                    t.update(len(chunk))
                    yield chunk

            response = session.put(
                f"{BASE_URL}/file/{os.path.basename(file_name)}",
                headers=headers,
                data=file_chunk_reader(),
                stream=True,
            )

    if response.status_code == 200 or response.status_code == 201:
        resp = response.json()
        print(f"File uploaded successfully: {FILE_URL}/u/{resp['id']}")
    else:
        print("ERROR: Upload failed!")
        print(f"Status Code: {response.status_code}")
        print(response.text)


def main():
    parser = argparse.ArgumentParser(description="Upload local files to Pixeldrain with API key authentication.")
    parser.add_argument(
        "file_name",
        help="Name of the local file to upload",
    )
    
    parser.add_argument(
        "api_key",
        help="""Your Pixeldrain API key (get it from your Pixeldrain account).
        You can also set the environment variable 'PDUP_API_KEY' instead of passing it as an argument.""",
    )
    parser.add_argument(
        "--sni-hostname",
        default="pixeldrain.net",
        help="The hostname to send in the SNI field (default: t.me).",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.file_name):
        print(f"ERROR: File '{args.file_name}' does not exist.")
        return

    api_key = args.api_key if args.api_key else os.getenv("PDUP_API_KEY")
    upload_file_to_pixeldrain(args.file_name, api_key, args.sni_hostname)


if __name__ == "__main__":
    main()
