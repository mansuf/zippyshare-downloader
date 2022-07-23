# zippyshare-downloader
# patterns.py

import math
import io
import re
from bs4 import BeautifulSoup
from .errors import *
from .utils import evaluate, getStartandEndvalue

__all__ = (
    'pattern1', 'pattern2', 'pattern3',
    'pattern4', 'pattern5',
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
        if script.strip().startswith('document.getElementById(\'dlbutton\').href'):
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

def pattern4(body_string, url):
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

    # Emulate .substr() function
    substr_re = r'.substr\((?P<start>[0-9]), (?P<length>[0-9])\)'
    substr = re.search(substr_re, omg)
    if not substr:
        raise ParserError(".substr() function cannot be found")

    substr_start = substr.group('start')
    substr_length = substr.group('length')
    substr_value = re.sub(substr_re, '', omg)[int(substr_start):int(substr_length)]

    scripts = io.StringIO(scrapped_script).readlines()
    _vars = {}
    init_url = None
    math_func = None
    file_url = None
    for script in scripts:
        # Finding variables that contain numbers
        re_var = re.compile(r'(var ([a-zA-Z]) = )([0-9]{1,})(;)')
        found = re_var.search(script)
        if found:
            _name = found.group(2)
            _value = found.group(3)

            if _value.startswith('document'):
                continue

            _vars[_name] = _value

        # Finding url download button
        if script.strip().startswith('document.getElementById(\'dlbutton\').href'):
            string_re_dlbutton = r'(document\.getElementById\(\'dlbutton\'\)\.href = \")(\/[a-zA-Z]\/[a-zA-Z0-9]{1,}\/)\"\+(\(Math\.pow\([a-zA-Z], [0-9]\)\+[a-zA-Z]\))\+\"(\/.{1,})\";'
            re_dlbutton = re.compile(string_re_dlbutton)
            result = re_dlbutton.search(script)
            if result:
                init_url = result.group(2)
                math_func = result.group(3)
                file_url = result.group(4)
            else:
                raise ParserError('Invalid regex pattern when finding url dlbutton')

    re_math_pow = r'\(Math\.pow\((?P<x>[a-zA-Z]), (?P<y>[0-9]{1,})\)\+[a-zA-Z]\)'
    x_y_math_pow = re.search(re_math_pow, math_func)
    if not x_y_math_pow:
        raise ParserError("Math.pow() cannot be found")
    
    x = x_y_math_pow.group('x')
    x = x.replace(x, _vars[x])
    y = x_y_math_pow.group('y')
    b = len(substr_value)

    final_numbers = int(math.pow(int(x), int(y)) + b)

    return url[:url.find('.')] + '.zippyshare.com' + init_url + str(final_numbers) + file_url

def pattern5(body_string, url):
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

    omg_element = parser.find('span', {'id': 'omg'})
    if omg_element is None:
        raise ParserError("Cannot find span element with id='omg'")

    omg_value = omg_element.attrs['class'][0]

    scripts = io.StringIO(scrapped_script).readlines()
    init_url = None
    numbers_pattern = None
    file_url = None
    for script in scripts:
        # Finding url download button
        if script.strip().startswith('document.getElementById(\'dlbutton\').href'):
            string_re_dlbutton = r'(document\.getElementById\(\'dlbutton\'\)\.href = \")' \
                                '(\/[a-zA-Z]\/[a-zA-Z0-9]{1,}\/)\"\+' \
                                '(\([0-9a-zA-Z%+()\/ ]{1,}\))\+\"(\/.{1,})\";'
            re_dlbutton = re.compile(string_re_dlbutton)
            result = re_dlbutton.search(script)
            if result:
                init_url = result.group(2)
                numbers_pattern = result.group(3)
                file_url = result.group(4)
            else:
                raise ParserError('Invalid regex pattern when finding url dlbutton')

    _vars = {}
    re_init_func = r'var (?P<var_name>[a-zA-Z]) = function\(\) \{return (?P<var_value>[0-9]{1,})\};'

    # Find a function with return statement only
    for script in scripts:
        init_func = re.search(re_init_func, script)
        if init_func is None:
            continue

        init_func_value = init_func.group('var_value')
        init_func_name = init_func.group('var_name')
        _vars[init_func_name] = init_func_value

    if not _vars:
        raise ParserError("Cannot find function with return statement only")

    # Find functions with return value "some_func() + some_numbers"
    found_eval_func = False
    re_eval_func = r'var (?P<var_name>[a-zA-Z]) = function\(\) \{return (?P<var_func_name>[a-zA-Z])\(\) (?P<operator>[+-/*]) (?P<var_const_value>[0-9]{1,})\};'
    for script in scripts:
        eval_func = re.search(re_eval_func, script)

        if eval_func is None:
            continue

        var_name = eval_func.group('var_name')
        func_name = eval_func.group('var_func_name')
        const_value = eval_func.group('var_const_value')
        operator = eval_func.group('operator')

        try:
            eval_func_value = _vars[func_name]
        except KeyError:
            # Failed here
            raise ParserError('Failed to find function with return value "some_func() + some_numbers"') from None

        _vars[var_name] = str(evaluate("{0} {1} {2}".format(
            eval_func_value,
            operator,
            const_value
        )))

        found_eval_func = True

    if not found_eval_func:
        # Fail here, do not continue
        raise ParserError('Failed to find function with return value "some_func() + some_numbers"')

    # Find the next var containing omg element
    re_var_omg = r"var (?P<var_name>[a-zA-Z]) = document\.getElementById\('omg'\)"
    found_omg_var = False
    for script in scripts:
        var_omg = re.search(re_var_omg, script)

        if var_omg is None:
            continue

        var_name = var_omg.group('var_name')

        _vars[var_name] = omg_value
        found_omg_var = True
        break

    if not found_omg_var:
        raise ParserError("Failed to find omg variable")

    # Final
    re_eval_var = r'if \((?P<boolean>true|false)\) { (?P<var_name>[a-zA-Z]) = (?P<expression>[a-zA-Z0-9*+/-]{1,});}'
    found_eval_var = False
    for script in scripts:
        eval_var = re.search(re_eval_var, script)

        if eval_var is None:
            continue

        init_bool_value = eval_var.group('boolean')
        var_name = eval_var.group('var_name')
        expression = eval_var.group('expression')

        bool_value = True if init_bool_value == "true" else False
        found_eval_var = True

        if bool_value:
            final_expr = expression.replace(var_name, _vars[var_name])

            _vars[var_name] = str(evaluate(final_expr))

    if not found_eval_var:
        raise ParserError("Failed to find if (true||false) statement")

    for var_name, var_value in _vars.items():
        numbers_pattern = numbers_pattern.replace(var_name, var_value)
    
    numbers_pattern = re.sub(r'[()]', '', numbers_pattern)

    final_numbers = str(int(evaluate(numbers_pattern)))
    return url[:url.find('.')] + '.zippyshare.com' + init_url + final_numbers + file_url

PATTERNS = [
    pattern1,
    pattern2,
    pattern3,
    pattern4,
    pattern5
] 