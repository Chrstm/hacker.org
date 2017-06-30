import re
import os
import time
from selenium import webdriver

pat = r'FVterrainString\=([\.X]*?)\&.*?FVinsMax\=(.*?)\&.*?FVinsMin\=(.*?)' \
      r'\&.*?FVboardX\=(.*?)\&.*?FVboardY\=(.*?)\&.*?FVlevel\=(.*?)\"'
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
    url1 = url + '&path=' + ans
    driver.get(url1)
    time.sleep(1)
    res = driver.find_elements_by_tag_name('body')
    res = res[0].get_attribute('innerHTML')
    return res, now, level


url = 'http://www.hacker.org/runaway/index.php?name=[...]&spw=[...]'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(1)
res = driver.find_elements_by_tag_name('body')
res = res[0].get_attribute('innerHTML')


maxt = 0
level = -1
lastlevel = -1
while level < 513:
    # print(res)
    res, t, level = work(res)
    maxt = max(maxt, t)
    if lastlevel == level:
        break
    lastlevel = level
print("\n\nMax Time Used:", maxt)
time.sleep(10)