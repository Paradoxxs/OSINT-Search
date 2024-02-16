import re

_dns_name_regex = r"(?:\w(?:[\w-]{0,100}\w)?\.)+(?:[xX][nN]--)?[^\W_]{1,63}\.?"
dns_name_regex = re.compile(_dns_name_regex, re.I)

_email_regex = r"(?:[^\W_][\w\-\.\+']{,100})@" + _dns_name_regex
email_regex = re.compile(_email_regex, re.I)


def extract_emails(s):
    for email in email_regex.findall(s):
        yield email.lower()