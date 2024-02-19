from Wappalyzer import Wappalyzer, WebPage

import warnings

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
