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
        page = WebPage.new_from_url(domain)
        return self.Wanalyzer.analyze(page)
