from Wappalyzer import Wappalyzer, WebPage
from utils.helpers import get_env_var
import warnings
import requests

warnings.filterwarnings(
    "ignore",
    message="""Caught 'unbalanced parenthesis at position 119' compiling regex""",
    category=UserWarning,
)


class wappalyzer:

    meta = {"description": "Extract technologies from web responses",}
    Wanalyzer = Wappalyzer.latest()


    async def query(self, response):
        try:
          page = WebPage.new_from_response(response)
          tech = self.Wanalyzer.analyze(page)
          #varify set have at least 1 technology
          if len(tech) > 0:
            return tech
          else:
            return None   
        except ConnectionError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None

class spyonweb:
   
    def __init__(self, access_token):
        self.access_token = get_env_var("spyonweb_api")
        self.base_url = "https://api.spyonweb.com/v1/analytics/"

    def query(self, analytics_code):
        url = f"{self.base_url}{analytics_code}?access_token={self.access_token}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "found":
                analytics_result = data.get("result", {}).get("analytics", {})
                if analytics_result:
                    items = analytics_result.get(analytics_code, {}).get("items")
                    return items
        else:
            print(f"Error: {response.status_code}")
            return None


