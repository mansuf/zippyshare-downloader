import requests
import aiohttp

class ProxyObject:
    def __init__(self, proxy=None):
        self.proxy = None

_proxy = ProxyObject()

# Modified requests session class with __del__ handler
# so the session will be closed properly
class requestsProxiedSession(requests.Session):
    def __del__(self):
        self.close()

# requests session with trust_env disabled
# this will disable proxies from enviroments
_requests_session = requestsProxiedSession()
_requests_session.trust_env = False

# Because aiohttp doesn't support proxy from session
# we need to subclass it to proxy each requests without
# add "proxy" parameter to each requests
class aiohttpProxiedSession(aiohttp.ClientSession):
    def __init__(self, proxy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = proxy

    def set_proxy(self, proxy):
        self.proxy = proxy
    
    def remove_proxy(self):
        self.proxy = None

    async def _request(self, *args, **kwargs):
        kwargs.update(proxy=self.proxy)
        return await super()._request(*args, **kwargs)

_aiohttp_session = aiohttpProxiedSession(proxy=None, trust_env=False)

def get_proxy():
    """Return configured HTTP/SOCKS proxy"""
    return _proxy.proxy

def is_proxied():
    """Check if aiohttp/requests are configured to connect with proxy"""
    return _proxy.proxy is not None

def set_proxy(proxy):
    """Set HTTP/SOCKS proxy to requests/aiohttp"""
    pr = {
        'http': proxy,
        'https': proxy
    }
    _requests_session.proxies.update(pr)
    _aiohttp_session.set_proxy(proxy)
    _proxy.proxy = proxy

def remove_proxy():
    """Remove proxy from requests/aiohttp"""
    _requests_session.proxies.clear()
    _aiohttp_session.remove_proxy()
    _proxy.proxy = None

def get_proxied_requests():
    """Return proxied requests session"""
    return _requests_session

def get_proxied_aiohttp():
    """Return proxied aiohttp session"""
    return _aiohttp_session