.. currentmodule:: zippyshare_downloader

API Documentation
===================

.. autofunction:: extract_info

.. autofunction:: download

.. autofunction:: extract_info_coro

.. autofunction:: download_coro

.. autofunction:: download_stdout

.. autoclass:: File
    :members:

Proxy related
~~~~~~~~~~~~~~~

Usage:

.. code-block:: python3

    from zippyshare_downloader.network import Net, set_proxy, clear_proxy

    # Http proxy
    Net.set_proxy('http://user:pass@address:port')

    # socks
    Net.set_proxy('socks5://user:pass@address:port')

    # Shortcut (if you're lazy af)
    set_proxy('http://user:pass@address:port')
    set_proxy('socks5://user:pass@address:port')

.. autoclass:: NetworkObject
    :members:

.. autofunction:: set_proxy

.. autofunction:: clear_proxy