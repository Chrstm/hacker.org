from pyTool import *


url = 'http://www.hacker.org/challenge/misc/past.php'
header = {
    'Cookie': '[... fill in your cookie here ...]',
    'User-Agent': 'NCSA_Mosaic/1.0',

}
print(open_page(url, header))
