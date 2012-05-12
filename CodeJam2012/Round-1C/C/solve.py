#!/usr/bin/env python
# -*- mode:python; coding:utf-8; indent-tabs-mode:nil -*-
#
# Problem C. Box Factory
# http://code.google.com/codejam/contest/1781488/dashboard#s=p2
#

import sys


class Box:
    def __init__(self, count, kind):
        self.count = count
        self.kind = kind

    @classmethod
    def create(cls, datas):
        return [cls(count, kind) for count, kind in zip(datas[::2], datas[1::2])]


class Toy(Box):
    pass


def solve(boxes, toyes):
    # 調査キャッシュ
    cache = {}
    # (bindex, bused, tindex, tused) をキーに、その先作れる最大数をキャッシュする

    def walk(bindex, bused, tindex, tused):
        key = (bindex, bused, tindex, tused)
        if key in cache:
            # キャッシュを返す
            return cache[key]

        # 対象の box と toy
        box = boxes[bindex]
        toy = toyes[tindex]
        cnt = 0

        # box と toy が同じタイプ
        while box.kind == toy.kind:
            # どっちか少ない方の残りを作る
            made = min(box.count - bused, toy.count - tused)
            cnt += made

            # box 使いきったら次の box へ
            bused += made
            if bused >= box.count:
                bindex += 1
                if bindex >= len(boxes):
                    return cnt
                box = boxes[bindex]
                bused = 0

            # toy 使いきったら次の toy へ
            tused += made
            if tused >= toy.count:
                tindex += 1
                if tindex >= len(toyes):
                    return cnt
                toy = toyes[tindex]
                tused = 0

        found = set((cnt, ))

        # 次の toy に進めてみる
        if tindex + 1 < len(toyes):
            # 進めた toy はまだ1コも使っていないので tused = 0
            found.add(cnt + walk(bindex, bused, tindex + 1, 0))

        # 次の box に進めてみる
        if bindex + 1 < len(boxes):
            # 進めた box はまだ1コも使っていないので bused = 0
            found.add(cnt + walk(bindex + 1, 0, tindex, tused))

        # この先最大これだけ作れます!をキャッシュする
        cache[key] = max(found)
        return cache[key]

    return walk(0, 0, 0, 0)


def main(INPUT, OUTPUT):
    T = int(INPUT.readline())
    for index in range(T):
        # 進捗表示
        sys.stderr.write('#%d\r' % (index + 1))
        N, M = map(int, INPUT.readline().split())
        boxes = Box.create(map(int, INPUT.readline().split()))
        toyes = Toy.create(map(int, INPUT.readline().split()))
        OUTPUT.write('Case #%d: %s\n' % (index + 1, solve(boxes, toyes)))


def makesample(Nmax, Mmax, T=100):
    import random
    print T
    for index in range(T):
        N = random.randint(1, Nmax)
        M = random.randint(1, Mmax)
        print N, M
        print ' '.join('%d %d' % (random.randint(1, 10**16), random.randint(1, 100)) for n in range(N))
        print ' '.join('%d %d' % (random.randint(1, 10**16), random.randint(1, 100)) for m in range(M))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if ('-makesample', 'small') == tuple(sys.argv[1:]):
            makesample(3, 100)
        elif ('-makesample', 'large') == tuple(sys.argv[1:]):
            makesample(100, 100)
        else:
            print 'usage: %s [-makesample <small|large>]' % sys.argv[0]
    else:
        main(sys.stdin, sys.stdout)

