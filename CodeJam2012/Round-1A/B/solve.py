#!/usr/bin/env python
# -*- mode:python; coding:utf-8; indent-tabs-mode:nil -*-
#
# Problem B. Kingdom Rush
# http://code.google.com/codejam/contest/1645485/dashboard#s=p1
#

import sys


class Level:
    def __init__(self, requires):
        # 1つ星条件、2つ星条件
        self.star1, self.star2 = requires
        # 残っている星の数
        self.left = 2


def solve(levels):
    # 獲得した星
    star = 0
    # ステップ数
    step = 0

    # 2つ星条件が小さい順にソートしておく
    levels.sort(key=lambda level: level.star2)

    # ステージが残っている間
    while levels:
        # ループ開始時の星の数
        begin = star

        # 2つ星条件をクリアできる
        while levels and levels[0].star2 <= star:
            # このステージの残っている星を加算(2つ星取ってこのステージは終わるのでリストから削除)
            star += levels.pop(0).left
            step += 1

        if not levels:
            # ステージが無くなった → 終了!
            break

        # 1つ星条件しか満たしていないケース
        weaks = filter(lambda level: level.left == 2 and level.star1 <= star, levels)
        if weaks:
            # 2つ星条件が大きいものから使っていく
            level = sorted(weaks, key=lambda level: level.star2, reverse=True)[0]
            # 星を1つだけ加算
            star += 1
            # 残り星を減らす
            level.left -= 1
            step += 1
        else:
            # 星を取れなくなった
            return 'Too Bad'

    return step


def main(INPUT, OUTPUT):
    T = int(INPUT.readline())
    for index in range(T):
        # 進捗表示
        sys.stderr.write('#%d\r' % (index + 1))
        N = int(INPUT.readline())
        levels = [Level(map(int, INPUT.readline().strip().split())) for n in range(N)]
        OUTPUT.write('Case #%d: %s\n' % (index + 1, solve(levels)))


def makesample(Nmax, T=100):
    import random
    print T
    for index in range(T):
        N = random.randint(1, Nmax)
        print N
        for n in range(N):
            a = random.randint(0, N + 1)
            b = random.randint(a, N + 1)
            print a, b


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if ('-makesample', 'small') == tuple(sys.argv[1:]):
            makesample(10)
        elif ('-makesample', 'large') == tuple(sys.argv[1:]):
            makesample(1000)
        else:
            print 'usage: %s [-makesample <small|large>]' % sys.argv[0]
    else:
        main(sys.stdin, sys.stdout)

