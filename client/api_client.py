import time
import requests

class APIClient:
    def __init__(self, base_url, max_tries=1):
        self.base_url = base_url
        self.max_tries = max_tries

    def send_data(self, payload, path="post"):
        attempt = 0
        while attempt <= self.max_tries:
            try:
                response = requests.post(f"{self.base_url}/{path}", json=payload, timeout=5)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Achtung Fehler: Status Code ist {response.status_code}")

            except requests.exceptions.Timeout:
                if attempt == self.max_tries:
                    raise Exception("Alle Versuche fehlgeschlagen")
                else:
                    time.sleep(1)
            attempt +=1

    def get_status(self, status="status"):
        try:
            response = requests.get(f"{self.base_url}/{status}", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Statusfehler: {response.status_code}")
        except requests.exceptions.Timeout:
            raise Exception("Timeout beim Abrufen des Status")




