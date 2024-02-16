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


    async def query(self, domain):
        try:
          page = WebPage.new_from_url("http://{}".format(domain),timeout=2)
          return self.Wanalyzer.analyze(page)
        except ConnectionError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None
