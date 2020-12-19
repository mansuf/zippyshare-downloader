import pathlib
from setuptools import setup
from zippyshare_downloader import __VERSION__

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
  name = 'zippyshare-downloader',         
  packages = ['zippyshare_downloader'],   
  version = __VERSION__,
  license='MIT',
  description = 'Download file from zippyshare directly from python',
  long_description= README,
  long_description_content_type= 'text/markdown',
  author = 'Rahman Yusuf',              
  author_email = 'danipart4@gmail.com',
  url = 'https://github.com/trollfist20/zippyshare-downloader',  
  download_url = 'https://github.com/trollfist20/zippyshare-downloader/archive/%s.tar.gz' % (__VERSION__),
  keywords = ['zippyshare', 'zippyshare-download'], 
  install_requires=[           
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
  ],
  python_requires='>=3'
)
