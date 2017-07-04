Firstly, compile "solve.cpp" with "-O3" option.

Secondly, if you are a Linux user, modify <code>rescode = os.system('solve.exe')</code> in "Crossflip-urllib.py".

Thirdly, I need to say that I ran it on my VPS but it exhausted the memory and then was killed by system. So I reached only level 567, not 643. So sad :(

Fourthly, the base algorithm is Gaussian elimination, and I design some interesting optimization(time & space) like  which make it five times faster.

Fifthly, an example.

|Rectangle Size|263x263|
|:-:|:-:|
|Time|5 min|
|Memory|576MB|
|CPU|Intel(R) i7-6700HQ 2.60GHz|
|CPU Utilization Rate|about 18%|
