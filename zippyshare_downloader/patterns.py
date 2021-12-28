# zippyshare-downloader
# patterns.py

import math
import io
import re
from bs4 import BeautifulSoup
from .errors import *
from .utils import evaluate, getStartandEndvalue

__all__ = (
    'pattern1', 'pattern2', 'pattern3'
    'PATTERNS'
)

# Determine html parser
# use lxml if installed for speed
try:
    import lxml
except ImportError:
    bs4_parser = 'html.parser'
else:
    bs4_parser = 'lxml'

def pattern1(body_string, url):
    # Getting download button javascript code
    parser = BeautifulSoup(body_string, bs4_parser)
    for script in parser.find_all('script'):
        if 'document.getElementById(\'dlbutton\').href' in script.decode_contents():
            scrapped_script = script.decode_contents()
            break
        else:
            scrapped_script = None
    if scrapped_script is None:
        raise ParserError('download button javascript cannot be found')

    # Finding omg attribute value in dlbutton element
    elements = io.StringIO(scrapped_script).readlines()
    omg_element = 'document.getElementById(\'dlbutton\').omg = '
    for element in elements:
        e = element.strip()
        if e.startswith(omg_element):
            omg = e.replace(omg_element, '').replace('"', '').replace(';', '')
            break
        else:
            omg = None
    if omg is None:
        raise ParserError('omg attribute in download button javascript cannot be found')

    # Finding uncompiled Random Number between FileID and Filename
    # http://www.zippyshare.com/d/{FileID}/uncompiled_number/{Filename}
    startpos_init = scrapped_script.find('document.getElementById(\'dlbutton\').href')
    scrapped_init = scrapped_script[startpos_init:]
    endpos_init = scrapped_init.find(';')
    scrapped = scrapped_init[:endpos_init]
    element_value = scrapped.replace('document.getElementById(\'dlbutton\').href = ', '')
    url_download_init = getStartandEndvalue(element_value, '"')
    uncompiled_number = getStartandEndvalue(element_value, '(', ')')
    
    # Finding Random Number variable a in scrapped_script
    variables = io.StringIO(scrapped_script).readlines()
    for var in variables:
        if var.strip().startswith('var a = '):
            a = var.strip().replace('var a = ', '').replace(';', '')
            break
        else:
            a = None
    if a is None:
        raise ParserError('variable a in download button javascript cannot be found')

    # Finding Random Number variable b in scrapped_script
    variables = io.StringIO(scrapped_script).readlines()
    for var in variables:
        if var.strip().startswith('var b = '):
            b = var.strip().replace('var b = ', '').replace(';', '')
            break
        else:
            b = None
    if b is None:
        raise ParserError('variable b in download button javascript cannot be found')

    if omg != 'f':
        random_number = uncompiled_number.replace('a', str(math.ceil(int(a)/3))).replace('b', b)
    else:
        random_number = uncompiled_number.replace('a', str(math.floor(int(a)/3))).replace('b', b)

    

    # Now using self.evaluate() to safely do math calculations
    url_number = str(evaluate(random_number))
    continuation_download_url_init = getStartandEndvalue(element_value, '(')
    continuation_download_url = continuation_download_url_init[continuation_download_url_init.find('"')+1:]
    return url[:url.find('.')] + '.zippyshare.com' + url_download_init + url_number + continuation_download_url

def pattern2(body_string, url):
    # Getting download button javascript code
    parser = BeautifulSoup(body_string, bs4_parser)
    for script in parser.find_all('script'):
        if 'document.getElementById(\'dlbutton\').href' in script.decode_contents():
            scrapped_script = script.decode_contents()
            break
        else:
            scrapped_script = None
    if scrapped_script is None:
        raise ParserError('download button javascript cannot be found')

    # Finding uncompiled Random Number between FileID and Filename
    # http://www.zippyshare.com/d/{FileID}/uncompiled_number/{Filename}
    startpos_init = scrapped_script.find('document.getElementById(\'dlbutton\').href')
    scrapped_init = scrapped_script[startpos_init:]
    endpos_init = scrapped_init.find(';')
    scrapped = scrapped_init[:endpos_init]
    element_value = scrapped.replace('document.getElementById(\'dlbutton\').href = ', '')
    url_download_init = getStartandEndvalue(element_value, '"')
    random_number = getStartandEndvalue(element_value, '(', ')')

    # Now using self.evaluate() to safely do math calculations
    url_number = str(evaluate(random_number))
    continuation_download_url_init = getStartandEndvalue(element_value, '(')
    continuation_download_url = continuation_download_url_init[continuation_download_url_init.find('"')+1:]
    return url[:url.find('.')] + '.zippyshare.com' + url_download_init + url_number + continuation_download_url

def pattern3(body_string, url):
    # Getting download button javascript code
    parser = BeautifulSoup(body_string, bs4_parser)
    for script in parser.find_all('script'):
        if 'document.getElementById(\'dlbutton\').href' in script.decode_contents():
            scrapped_script = script.decode_contents()
            break
        else:
            scrapped_script = None
    if scrapped_script is None:
        raise ParserError('download button javascript cannot be found')
    
    scripts = io.StringIO(scrapped_script).readlines()
    _vars = {}
    init_url = None
    numbers_pattern = None
    file_url = None
    for script in scripts:
        # Finding variables that contain numbers
        re_var = re.compile(r'(var ([a-zA-Z]) = )([0-9%]{1,})(;)')
        found = re_var.search(script)
        if found:
            _name = found.group(2)
            _value = found.group(3)
            _vars[_name] = _value
        # Finding url download button
        if script.strip().startswith('document.getElementById(\'dlbutton\')'):
            string_re_dlbutton = r'(document\.getElementById\(\'dlbutton\'\)\.href = \")' \
                                '(\/[a-zA-Z]\/[a-zA-Z0-9]{1,}\/)\"\+' \
                                '(\([a-zA-Z] \+ [a-zA-Z] \+ [a-zA-Z] - [0-9]\))\+\"(\/.{1,})\";'
            re_dlbutton = re.compile(string_re_dlbutton)
            result = re_dlbutton.search(script)
            if result:
                init_url = result.group(2)
                numbers_pattern = result.group(3)
                file_url = result.group(4)
            else:
                raise ParserError('Invalid regex pattern when finding url dlbutton')
    
    if not _vars:
        raise ParserError('Cannot find required variables in dlbutton script')
    else:
        for var_name, var_value in _vars.items():
            numbers_pattern = numbers_pattern.replace(var_name, var_value)
        final_numbers = str(evaluate(numbers_pattern))
    return url[:url.find('.')] + '.zippyshare.com' + init_url + final_numbers + file_url




PATTERNS = [
    pattern1,
    pattern2,
    pattern3
]