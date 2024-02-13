from Wappalyzer import Wappalyzer, WebPage

import warnings

warnings.filterwarnings(
    "ignore",
    message="""Caught 'unbalanced parenthesis at position 119' compiling regex""",
    category=UserWarning,
)


class wappalyzer():

    meta = {"description": "Extract technologies from web responses",}
    wappalyzer = Wappalyzer.latest()


    def wappalyze(self, domain):
        page = WebPage.new_from_url(domain)
        return wappalyzer.analyze(page)
