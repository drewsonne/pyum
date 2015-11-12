__author__ = 'drews'

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

    def _http_request(self, url):
        (path, conn) = self._http_connection(url)
        conn.request('GET', path)
        response = conn.getresponse()
        return response.read()

    def _url_is_reachable(self, url):
        (path, conn) = self._http_connection(url)
        conn.request('HEAD', path)
        response = conn.getresponse()
        return response.status == 200
