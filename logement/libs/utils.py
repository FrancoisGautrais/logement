import re
import traceback

from django.conf import settings
from django.http import HttpRequest, HttpResponseRedirect

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



def need_auth(fct):

    def wrapper(req : HttpRequest,  *args, **kwargs):
        print(req.user.is_authenticated)
        if req.user.is_authenticated:
            return fct(req, *args, **kwargs)
        else:
            return HttpResponseRedirect(f"{settings.LOGIN_URL}?redirect={req.path}")

    return wrapper

