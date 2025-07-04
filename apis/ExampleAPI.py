import requests, json
from apis.Utils  import api_call, api_class

@api_class(api_name="ExampleAPI")
class ExampleAPI():

    def __init__(self):
        self.base_url = "http://localhost:5000"



    @api_call
    def call_get_data(self, key_path=None):
        try:
            if key_path:
                url = f"{self.base_url}/data/{key_path}"
            else:
                url = f"{self.base_url}/data"
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()
            print(f"Status Code: {response.status_code}")
            print(f"Response Data: {json.dumps(data, indent=2)}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching all data: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response Content: {e.response.text}")
            return None
        

@api_class(api_name="APIleDugma")
class DugmaAPI():

    def __init__(self):
        self.base_url = "http://localhost:5000"



    @api_call
    def call_tavi_akol(self, key_path=None):
        try:
            if key_path:
                url = f"{self.base_url}/data/{key_path}"
            else:
                url = f"{self.base_url}/data"
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()
            print(f"Status Code: {response.status_code}")
            print(f"Response Data: {json.dumps(data, indent=2)}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching all data: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response Content: {e.response.text}")
            return None
        
