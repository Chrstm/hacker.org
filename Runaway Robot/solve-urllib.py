import re
import urllib.request
import urllib.parse
import os
import time


pat = r'FVterrainString\=([\.X]*?)\&FVinsMax\=(.*?)\&FVinsMin\=(.*?)' \
      r'\&FVboardX\=(.*?)\&FVboardY\=(.*?)\&FVlevel\=(.*?)\"'
def work(res):
    map, maxstep, minstep, x, y, level = re.findall(pat, res)[0]
    maxstep = int(maxstep)
    minstep = int(minstep)
    x = int(x)
    y = int(y)
    level = int(level)
    f = open('in.txt'.format(level), 'w')
    print("level-{}: {} {} {} {}".format(level, x, y, minstep, maxstep))
    f.write("{} {} {} {}\n".format(x, y, minstep, maxstep))
    for i in range(x):
        f.write(map[i * y: (i + 1) * y] + '\n')
    f.close()

    print(r"B-hacker.exe<in.txt>ans.txt".format(level, level))
    now = time.time()
    os.system(r"B-hacker.exe<in.txt>ans.txt".format(level, level))
    now = time.time() - now
    print("Time: %.4fsec" % now)
    f = open('ans.txt'.format(level), 'r')
    ans = f.readline()[:-1]
    f.close()
    print("Answer is", ans)
    print()
    req = urllib.request.Request(url=url + '&path=' + ans)
    res = urllib.request.urlopen(req).read().decode()
    return res, now, level


proxy_support = urllib.request.ProxyHandler({'http': 'localhost:1080'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
url = 'http://www.hacker.org/runaway/index.php?name=[...]&spw=[...]'
req = urllib.request.Request(url=url)
res = urllib.request.urlopen(req).read().decode()

maxt = 0
level = 0
lastlevel = 1
while level < 513:
    res, t, level = work(res)

    maxt = max(maxt, t)
    if lastlevel == level:
        break
    lastlevel = level
print("\n\nMax Time Used:", maxt)
