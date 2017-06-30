from pyTool import *


s = open_page(url="https://www.ietf.org/rfc/rfc3280.txt", return_header=False).lower()
s = re.findall(r'\b[a-zA-Z]{9}\b', s)
m = 0
for x in s:
    k = s.count(x)
    if k > m:
        print(x, k)
        m = k
        
'''
Challenge '3280' [Coding]

What's the most common 9-letter word in RFC 3280?
'''