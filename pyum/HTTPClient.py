import gzip
import socket
import gzip
import io
import zlib
from pyum import cache

__author__ = 'drews'

from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse
import http.client


class HTTPClient(object):
    def _http_connection(self, url):
        o = urlparse(url)
        if o.scheme == 'http':
            connection_func = http.client.HTTPConnection
        elif o.scheme == 'https':
            connection_func = http.client.HTTPSConnection
        else:
            raise TypeError("unexpected scheme '{0}'".format(o.scheme))
        path = o.path
        if o.query != '':
            path = "{0}?{1}".format(path, o.query)
        return (path, connection_func(o.netloc))

    @cache.opts(keys=('url', 'decode'), lifetime=3600)
    def _http_request(self, url, decode='utf-8'):
        (path, conn) = self._http_connection(url)
        conn.request('GET', path)
        response = conn.getresponse()

        content_type = response.getheader('Content-Type', None)
        if content_type is not None:
            if (content_type in ['application/x-gzip']) or url.endswith('.gz') or url.endswith('.tgz'):
                result = gzip.decompress(response.read())
                if decode is not None:
                    return result.decode(decode)
                else:
                    return result

        return response.read()

    @cache.opts(keys=['url'])
    def _url_is_reachable(self, url):
        (path, conn) = self._http_connection(url)
        try:
            conn.request('HEAD', path)
        except socket.gaierror:
            return False
        response = conn.getresponse()
        return response.status == 200
