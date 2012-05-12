#!/usr/bin/env python
# -*- mode:python; coding:utf-8; indent-tabs-mode:nil -*-
#
# Problem A. Diamond Inheritance
# http://code.google.com/codejam/contest/1781488/dashboard#s=p0
#

import sys


class Class:
    def __init__(self, no, inherits):
        self.no = no
        self.inherits = inherits


def solve(classes):
    found = set()

    for index, cls in enumerate(classes):
        # index → no
        no = index + 1
        if not filter(lambda c: no in c.inherits, classes):
            # このクラスを継承しているクラスがない(サブクラスの終端)

            # 再帰すると Large で死ぬのでループで回す
            # (クラス, 親クラス走査イテレータ) のペアをリストする
            route = [(cls, iter(cls.inherits))]
            while route:
                cls, it = route[-1]

                if not cls.inherits:
                    # ルートクラス
                    key = (route[0][0].no, route[-1][0].no)
                    if key in found:
                        # サブクラス&ルートクラスペアが既にある = 2つの経路が見つかった
                        return "Yes"
                    # サブクラス&ルートクラスペアを保持
                    found.add(key)
                    # このルートクラスを取り除いてひとつ上の経路へ
                    route.pop()

                else:
                    try:
                        # 次のクラス
                        nextno = it.next()
                        cls = classes[nextno-1]
                        # 敬称ルートに積む
                        route.append((cls, iter(cls.inherits)))
                    except StopIteration:
                        # このクラスの継承走査は終わった → ひとつ上の次へ
                        route.pop()

    # サブクラス&ルートクラスペアの重複がなかった
    return "No"


def main(INPUT, OUTPUT):
    T = int(INPUT.readline())
    for index in range(T):
        # 進捗表示
        sys.stderr.write('#%d\r' % (index + 1))
        N = int(INPUT.readline())
        classes = [Class(n+1, map(int, INPUT.readline().split())[1:]) for n in range(N)]
        OUTPUT.write('Case #%d: %s\n' % (index + 1, solve(classes)))

if __name__ == '__main__':
    main(sys.stdin, sys.stdout)

