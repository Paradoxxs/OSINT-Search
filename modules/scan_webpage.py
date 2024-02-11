import re


class social():

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



    async def handle_event(self, event):
        for platform, regex in self.compiled_regexes.items():
            for match in regex.finditer(event.data):
                url = match.group()
                if not url.startswith("http"):
                    url = f"https://{url}"
                profile_name = match.groups()[0]
                self.emit_event(
                    {"platform": platform, "url": url, "profile_name": profile_name}, "SOCIAL", source=event
                )