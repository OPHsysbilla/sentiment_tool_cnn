#!/usr/bin/env python
# coding=utf-8
# Python使用的是2.7，缩进可以使用tab、4个空格或2个空格，但是只能任选其中一种，不能多种混用
a = []
while 1:
    s = input()
    # raw_input()里面不要有任何提示信息
    if s != "":
        for x in s.split():
            if x.isnumeric():
                a.append(int(x))
            else:
                a.append(str(x))
    else:
        break
for s in a:


        # for i in range(len(a)):
#