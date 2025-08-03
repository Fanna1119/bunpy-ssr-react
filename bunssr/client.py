import pycurl
from io import BytesIO
import json

class UnixSocketHttpClient:
    def __init__(self, socket_path):
        self.socket_path = socket_path

    def request(self, url, method="GET", headers=None, data=None):
        response_buffer = BytesIO()
        curl = pycurl.Curl()

        try:
            curl.setopt(pycurl.UNIX_SOCKET_PATH, self.socket_path)
            curl.setopt(pycurl.URL, f"http://localhost{url}")
            curl.setopt(pycurl.WRITEDATA, response_buffer)
            curl.setopt(pycurl.CUSTOMREQUEST, method)

            if headers:
                formatted_headers = [f"{key}: {value}" for key, value in headers.items()]
                curl.setopt(pycurl.HTTPHEADER, formatted_headers)

            if data:
                if isinstance(data, dict):
                    data = json.dumps(data)
                if isinstance(data, str):
                    data = data.encode("utf-8")
                curl.setopt(pycurl.POSTFIELDS, data)

            curl.perform()

            status_code = curl.getinfo(pycurl.RESPONSE_CODE)
            response_body = response_buffer.getvalue().decode("utf-8")

            return status_code, response_body

        except pycurl.error as e:
            return None, f"cURL error: {e}"

        finally:
            curl.close()
