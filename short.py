from __future__ import with_statement
import contextlib

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import sys

def shorten(url):
    request_url = ('http://tinyurl.com/api-create.php?' + 
    urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')


def main():
    for shortyurl in map(shorten, sys.argv[1:]):
        print(shortyurl)




if __name__ == '__main__':
    main()
