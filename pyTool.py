import urllib.request
import urllib.parse


def open_page(url, headers=None, data=None, return_header=True):
    '''open a webpage

    :param url: url
    :param headers: {'...': ..., }
    :param data: {'...': ..., }
    :return: text + respose_headers
    '''
    if data:
        data = urllib.parse.urlencode(data).encode()
    if headers:
        req = urllib.request.Request(url=url, headers=headers, data=data)
    else:
        req = urllib.request.Request(url=url, data=data)
    res = urllib.request.urlopen(req)
    if return_header:
        return res.read().decode(errors='replace') + '\n\n\n' + str(res.info())
    else:
        return res.read().decode(errors='replace')
