# zippyshare-downloader
# utils.py

import re
import math
from .errors import InvalidURL

ALLOWED_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}

# Credit for the evaluate() method: Leodanis Pozo Ramos  https://realpython.com/python-eval-function/
def evaluate(expression):
    """Evaluate a math expression."""

    # Compile the expression
    code = compile(expression, "<string>", "eval")

    # Validate allowed names
    for name in code.co_names:
        if name not in ALLOWED_NAMES:
                raise NameError("The use of '%s' is not allowed. Expression used: %s" % (name, expression))

    return eval(code, {"__builtins__": {}}, ALLOWED_NAMES)

REGEXS_ZIPPYSHARE_URL = [
    # View zippyshare url
    r'https:\/\/www[0-9]{3}\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html',
    r'https:\/\/www[0-9]{2}\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html',
    r'https:\/\/www[0-9]{1}\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html',
    r'https:\/\/www\.zippyshare\.com\/v\/[0-9A-Za-z]{8}\/file\.html',
    # Download Zippyshare url
    r'^https:\/\/www[0-9]{3}\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/',
    r'https:\/\/www[0-9]{2}\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/',
    r'https:\/\/www[0-9]{1}\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/',
    r'https:\/\/www\.zippyshare\.com\/d\/[0-9A-Za-z]{8}\/',
]

def check_valid_zippyshare_url(url):
    for regex in REGEXS_ZIPPYSHARE_URL:
        if re.match(regex, url) is not None:
            return url
    raise InvalidURL('"%s" is not a zippyshare url' % (url))

def getStartandEndvalue(value: str, sub: str, second_sub=None):
    v = value[value.find(sub)+1:]
    if second_sub is not None:
        return v[:v.find(second_sub)]
    else:
        return v[:v.find(sub)]