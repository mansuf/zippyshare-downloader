Command Line Interface (CLI) Usage
===================================

App names
----------

There is few app names in zippyshare-downloader:

- ``zippyshare-dl``
- ``zippyshare-downloader``

.. note::

    If none of above doesn't work use this

    .. code-block:: shell

        # For Windows
        py -3 -m zippyshare_downloader

        # For Linux
        python3 -m zippyshare_downloader


Options
-------

Global options
~~~~~~~~~~~~~~~

- ``ZIPPYSHARE_URL or FILE``     Zippyshare URL or file containing zippyshare urls
- ``--no-download``              No download file
- ``--verbose``, ``-v``          Enable verbose
- ``--replace``, ``-r``          Replace file if exist
- ``--silent``                   No output

File / Folder related
~~~~~~~~~~~~~~~~~~~~~~

- ``--folder FOLDER``            Store downloaded file in given folder
- ``--filename FILENAME``        Rewrite filename. Will be ignored if using multiple urls

Zip and unzip
~~~~~~~~~~~~~~

- ``--zip FILENAME``, ``-z FILENAME`` Zip all downloaded files
- ``--unzip``, ``-uz`` Unzip all downloaded files, one by one

.. warning:: 
    
    Option ``--unzip`` or ``-uz`` will only work if you are using multiple zippyshare urls

    For example:

    .. code-block:: shell

        # This will work
        $ zippyshare-dl "urls.txt" --unzip

        # This will NOT work
        $ zippyshare-dl "https://www.zippyshare.com/v/..." --unzip

Download related
~~~~~~~~~~~~~~~~~

- ``--async`` Run zippyshare-downloader in asynchronous mode
- ``--fast`` Enable fast download

.. note::

    When you using ``--async`` option, the download is faster than without using
    ``--async`` one.

.. warning::

    ``--fast`` option require ``--async``. It will throw error if you specified
    ``--fast`` without ``--async`` option.

    For example:

    .. code-block:: shell

        # This will work
        $ zippyshare-dl "https://www.zippyshare.com/v/..." --async --fast

        # This will NOT work
        $ zippyshare-dl "https://www.zippyshare.com/v/..." --fast

