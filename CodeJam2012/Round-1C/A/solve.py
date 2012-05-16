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


# サブクラス終端からルートクラスに辿る場合
def solve(classes):
    for cls in classes:
        if not filter(lambda c: cls.no in c.inherits, classes):
            # このクラスを継承しているクラスがない → サブクラスの終端からスタート

            # 祖先リスト
            ascendant = list(cls.inherits)
            index = 0
            while index < len(ascendant):
                # 次に調べるクラスのID
                clsid = ascendant[index]

                # 親クラスをチェック
                for inherit in classes[clsid-1].inherits:
                    if inherit in ascendant:
                        # 既に同じクラスが祖先にいる → Diamond Inheritance 発見
                        return "Yes"
                    # 祖先リストに追加
                    ascendant.append(inherit)

                # 祖先リスト次の項目を調べる
                index += 1

    # 全てのサブクラス終端から始めて一度も同じ祖先に辿り着かなかった
    return "No"


# ルートクラスからサブクラスを列挙する場合
def solve(classes):
    # クラス→スーパークラス のリストから、クラスID→サブクラスIDのリスト を構築する
    subclassmap = dict((cls.no, set()) for cls in classes)
    for cls in classes:
        for clsid in cls.inherits:
            # スーパークラスのサブクラスIDリストに自身のクラスIDを加える
            subclassmap[clsid].add(cls.no)

    # ルートクラスごとに子孫を調べる
    for root in [cls.no for cls in classes if not cls.inherits]:
        descendant = list(subclassmap[root])
        index = 0
        while index < len(descendant):
            # 次に調べるクラスのID
            clsid = descendant[index]
            # サブクラスを列挙
            for subclass in subclassmap[clsid]:
                if subclass in descendant:
                    # 既に同じサブクラスに辿り着いている
                    return "Yes"
                # サブクラスリストに追加
                descendant.append(subclass)
            index += 1

    # 同じサブクラスに辿り着かなかった
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

