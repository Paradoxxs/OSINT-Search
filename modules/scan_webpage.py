import re
import requests

class social:

    meta = {"description": "Look for social media links in webpages"}

    social_media_regex = {
        "linkedin": r"(?:https?://)?(?:www.)?linkedin.com/(?:in|company)/([a-zA-Z0-9-]+)/?",
        "facebook": r"(?:https?://)?(?:www.)?facebook.com/([a-zA-Z0-9.]+)/?",
        "twitter": r"(?:https?://)?(?:www.)?twitter.com/([a-zA-Z0-9_]{1,15})/?",
        "github": r"(?:https?://)?(?:www.)?github.com/([a-zA-Z0-9_-]+)/?",
        "instagram": r"(?:https?://)?(?:www.)?instagram.com/([a-zA-Z0-9_.]+)/?",
        "youtube": r"(?:https?://)?(?:www.)?youtube.com/([a-zA-Z0-9_]+)/?",
        "bitbucket": r"(?:https?://)?(?:www.)?bitbucket.org/([a-zA-Z0-9_-]+)/?",
        "gitlab": r"(?:https?://)?(?:www.)?gitlab.com/([a-zA-Z0-9_-]+)/?",
        "discord": r"(?:https?://)?(?:www.)?discord.gg/([a-zA-Z0-9_-]+)/?",
    }

    compiled_regexes = {k: re.compile(v) for k, v in social_media_regex.items()}



    async def query(self, response):
        SO_profile = []
        try:
            for platform, regex in self.compiled_regexes.items():
                for match in regex.finditer(response.text):
                    url = match.group()
                    if not url.startswith("http"):
                        url = f"https://{url}"
                    SO_profile.append(url)
            #check if SO_profile have at least 1 profile and remove dublicate
            if len(SO_profile) > 0:
                return list(set(SO_profile))
            else:
                return None
        except Exception as e:
            print(e)
            return None


class Find_Google_analytic_id:

    meta = {"description": "Look for social media links in webpages"}

    google_analytic_id_regex = r"UA-[0-9]{4,9}-[0-9]{1,3}"

    compiled_regex = re.compile(google_analytic_id_regex) 



    async def query(self, response):
        try:
            for match in self.compiled_regex.finditer(response.text):
                id = match.group()
                if not id.startswith("UA-"):
                    continue
                return id
        except Exception as e:
            print(e)
            return None


class ScanWebpage():
    

    async def query(self, response):
        social_data =  await social().query(response)
        analytic_id = await Find_Google_analytic_id().query(response)

        return social_data,analytic_id