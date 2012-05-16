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


class Found(Exception):
    pass


class Checker:
    def __init__(self, classes, leaf):
        self.classes = classes
        self.roots = set()
        self.walk(leaf)

    def walk(self, clsid):
        cls = self.classes[clsid-1]
        if cls.inherits:
            # スーパークラスに進む(再帰)
            for inherit in cls.inherits:
                self.walk(inherit)
        else:
            # ルートクラス
            if clsid in self.roots:
                # 同じ親クラスにつながる経路2つめ発見! → 大域脱出に例外を使う(!)
                raise Found()
            self.roots.add(clsid)


def solve(classes):
    try:
        for cls in classes:
            if not filter(lambda c: cls.no in c.inherits, classes):
                # このクラスを継承しているクラスがない → サブクラスの終端からスタート
                Checker(classes, cls.no)
    except Found, e:
        # Diamond Inheritance 発見
        return "Yes"
    return "No"


def main(INPUT, OUTPUT):
    sys.setrecursionlimit(1100)
    T = int(INPUT.readline())
    for index in range(T):
        # 進捗表示
        sys.stderr.write('#%d\r' % (index + 1))
        N = int(INPUT.readline())
        classes = [Class(n+1, map(int, INPUT.readline().split())[1:]) for n in range(N)]
        OUTPUT.write('Case #%d: %s\n' % (index + 1, solve(classes)))

if __name__ == '__main__':
    main(sys.stdin, sys.stdout)

