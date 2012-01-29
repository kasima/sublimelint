# sass.py - sublimelint package for checking coffee-script files

import subprocess, os

def check(codeString, filename):
    info = None
    if os.name == 'nt':
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE

    process = subprocess.Popen(
        ('sass', '--check', '--scss', '--stdin'),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        startupinfo=info
    )
    result = process.communicate(codeString)[1]
    return result

import re
__all__ = ['run', 'language']
language = 'SASS'

# Syntax error: Invalid CSS after "": expected selector, was ""
#         on line 12 of standard input
#   Use --trace for backtrace.

compile_err  = re.compile('^Syntax error: (.*)$')
compile_line = re.compile('^\s+on line ([0-9]+) .*')

def run(code, view, filename='untitled'):
    # print ">>> Checking SASS"

    errors = check(code, filename)
    # print ">>> Errors: %s" % errors

    lines = set()
    underline = [] # leave this here for compatibility with original plugin

    errorMessages = {}
    def addMessage(lineno, message):
        message = str(message)
        if lineno in errorMessages:
            errorMessages[lineno].append(message)
        else:
            errorMessages[lineno] = [message]

    error_lines = errors.splitlines()
    if error_lines:
        match = compile_err.match(error_lines[0])
        if match:
            print "line>> %s" % errors
            error = match.groups()[0]
            match = compile_line.match(error_lines[1])
            line = match.groups()[0]

        print "Found: %s, %s" % (line, error)
        lineno = int(line) - 1
        lines.add(lineno)
        addMessage(lineno, error)

    return underline, lines, errorMessages, True

if __name__ == '__main__':
    import sys
    print run(open(sys.argv[1]).read(), 'bah')
