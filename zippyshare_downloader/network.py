import requests
import aiohttp

__all__ = (
    'Net', 'set_proxy', 'clear_proxy'
)

# Modified requests session class with __del__ handler
# so the session will be closed properly
class requestsProxiedSession(requests.Session):
    def __init__(self, trust_env=True) -> None:
        super().__init__()
        self.trust_env = trust_env

    def __del__(self):
        self.close()

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

class NetworkObject:
    def __init__(self) -> None:
        self._proxy = None
        self._aiohttp = None # type: aiohttpProxiedSession

        # This will be disable proxy from environtments
        self._requests = requestsProxiedSession(trust_env=False)

    @property
    def proxy(self):
        """Return HTTP/SOCKS proxy, return ``None`` if not configured"""
        return self._proxy

    @proxy.setter
    def proxy(self, proxy):
        if proxy is None:
            self.clear_proxy()
        self.set_proxy(proxy)

    def is_proxied(self):
        """Return ``True`` if requests/aiohttp from :class:`NetworkObject`
        are configured using proxy.
        """
        return self.proxy is not None

    def set_proxy(self, proxy):
        """Setup HTTP/SOCKS proxy for aiohttp/requests"""
        self._proxy = proxy
        pr = {
            'http': proxy,
            'https': proxy
        }
        self._requests.proxies.update(pr)
        self.aiohttp.set_proxy(proxy)

    def clear_proxy(self):
        """Remove all proxy from aiohttp/requests"""
        self._proxy = None
        self._requests.proxies.clear()
        self.aiohttp.remove_proxy()

    @property
    def aiohttp(self):
        """Return proxied aiohttp (if configured)"""
        self._create_aiohttp()
        return self._aiohttp

    @property
    def requests(self):
        """Return proxied requests (if configured)"""
        return self._requests

    def _create_aiohttp(self):
        if self._aiohttp is None:
            self._aiohttp = aiohttpProxiedSession(self.proxy)

Net = NetworkObject()

def set_proxy(proxy):
    """Setup HTTP/SOCKS proxy for aiohttp/requests
    
    This is shortcut for :meth:`NetworkObject.set_proxy`
    """
    Net.set_proxy(proxy)

def clear_proxy():
    """Remove all proxy from aiohttp/requests
    
    This is shortcut for :meth:`NetworkObject.clear_proxy`
    """
    Net.clear_proxy()