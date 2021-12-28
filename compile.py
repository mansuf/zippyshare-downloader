# An easy to use compiling zippyshare-downloader
# Using PyInstaller
# DO NOT IMPORT FROM ANOTHER PYTHON SCRIPT
import re
import subprocess
from pathlib import Path

# Base path
base = Path(__name__).parent

# Find version without importing it
script = (base / 'zippyshare_downloader' / '__init__.py').read_text()
regex = re.compile(r'[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}')
version = regex.search(script).group()

# Compile for one-file bundled executable.
subprocess.run([
    'pyinstaller',
    'zippyshare_downloader/__main__.py',
    '-F',
    '--name',
    'zippyshare-dl_%s_packed_x64' % version,
    '--clean'
], shell=False)

# Compile for one-folder bundle containing an executable
subprocess.run([
    'pyinstaller',
    'zippyshare_downloader/__main__.py',
    '--name',
    'zippyshare-dl_%s_x64' % version,
    '--clean'
], shell=False)