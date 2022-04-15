import re
import traceback

from logement.libs.scrapper.base.request import Request

RE_FIND_DOMAIN = re.compile(r"\w+://(?P<domain>[^/:]+)")
def find_domain(url):
    if isinstance(url, Request):
        url = url.url
    ret = re.findall(RE_FIND_DOMAIN, url or "")
    return ret[0] if ret else None


def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=??
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)





