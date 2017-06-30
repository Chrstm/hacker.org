from pyTool import *


proxy_support = urllib.request.ProxyHandler({'http': 'localhost:1080'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

url = 'http://www.hacker.org/challenge/chal.php?id=38&answer=http://whitehouse.gov&id=38&go=Submit'
header = {
    'Cookie': '[... fill in your cookie here ...]',
    'Referer': 'http://whitehouse.gov',
}
print(open_page(url, header))
