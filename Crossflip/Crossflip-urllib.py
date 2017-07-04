import re
import os
import time
import urllib.request
import urllib.parse


url = "http://www.hacker.org/cross/index.php"
account = 'name=JHSN&spw=[...]'


def open_page(url, data):
    req = urllib.request.Request(url=url, data=data.encode())
    res = urllib.request.urlopen(req).read().decode(errors='replace')
    try:
        return re.findall('<script>.*?"([\d,]*)";var.*?(\d*);</script>', res)[0]
    except Exception:
        print(res)
        exit(0)

data = open_page(url, account)
while True:
    map = data[0].split(',')
    level = data[1]
    n = len(map)
    m = len(map[0])
    print("Level: %s   Size: (%d, %d)" % (level, n, m))

    f = open('in.txt', 'w')
    f.write("%d %d\n" % (n, m))
    for i in range(n):
        f.write(map[i] + '\n')
    f.close()
    if n * m < 100:
        print(map)

    t = time.time()
    rescode = os.system('solve.exe')
    print('Return', rescode)
    if rescode != 0:
        exit(0)
    print("Time: %.4f sec" % (time.time() - t))
    f = open('ans.txt', 'r')
    ans = f.read()
    if n * m < 100:
        print(ans)
    print()
    flag = 1
    data = account + '&lvl=%s&sol=%s' % (level, ans)
    while 0 < flag < 5:
        try:
            data = open_page(url, data)
            flag = 0
        except Exception:
            print("Failed to connect.\n")
            flag += 1
            time.sleep(3)
    if flag >= 5:
        data = open_page(url, data)
