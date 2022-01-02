import requests
import aiohttp
import asyncio

__all__ = (
    'Net', 'NetworkObject',
    'set_proxy', 'clear_proxy'
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
    def __init__(self, proxy=None, trust_env=False) -> None:
        self._proxy = proxy
        self._aiohttp = None # type: aiohttpProxiedSession
        self._trust_env = trust_env

        # This will be disable proxy from environtments
        self._requests = requestsProxiedSession(trust_env=self._trust_env)

    @property
    def proxy(self):
        """Return HTTP/SOCKS proxy, return ``None`` if not configured"""
        return self._proxy

    @proxy.setter
    def proxy(self, proxy):
        if proxy is None:
            self.clear_proxy()
        self.set_proxy(proxy)

    @property
    def trust_env(self):
        """Return ``True`` if http/socks proxy are grabbed from env"""
        return self._trust_env

    @trust_env.setter
    def trust_env(self, yes):
        self._trust_env = yes
        if self.aiohttp:
            self.aiohttp._trust_env = yes
        self._requests.trust_env = yes

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
        if self.aiohttp:
            self.aiohttp.set_proxy(proxy)

    def clear_proxy(self):
        """Remove all proxy from aiohttp/requests"""
        self._proxy = None
        self._requests.proxies.clear()
        if self.aiohttp:
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
        # Check if current asyncio loop is running
        # if running create aiohttp session
        # if not don't create it
        loop = asyncio.get_event_loop()

        # Raise error if using in another thread
        if self._aiohttp and self._aiohttp._loop != loop:
            raise RuntimeError('created aiohttp session cannot be used in different thread')

        if self._aiohttp is None:
            self._aiohttp = aiohttpProxiedSession(self.proxy)

    def close(self):
        """Close requests session only"""
        self._requests.close()
        self._requests = requestsProxiedSession(self._trust_env)

    async def close_async(self):
        """Close aiohttp & requests session"""
        self.close()
        if self._aiohttp.closed:
            await self._aiohttp.close()
        self._aiohttp = None

Net = NetworkObject()

def set_proxy(proxy):
    """Setup HTTP/SOCKS proxy for aiohttp/requests
    
    This is shortcut for :meth:`NetworkObject.set_proxy`. 
    """
    Net.set_proxy(proxy)

def clear_proxy():
    """Remove all proxy from aiohttp/requests
    
    This is shortcut for :meth:`NetworkObject.clear_proxy`. 
    """
    Net.clear_proxy()