#!/usr/bin/env python
# -*- mode:python; coding:utf-8; indent-tabs-mode:nil -*-
#
# Problem B. Kingdom Rush
# http://code.google.com/codejam/contest/1645485/dashboard#s=p1
#

import sys


class Level:
    def __init__(self, requires):
        self.star1, self.star2 = requires
        self.left = 2


def solve(levels):
    #print [(level.star1, level.star2) for level in levels]
    star = 0
    step = 0

    while levels:
        begin = star

        # 1. 2 stars 取れるものがあれば
        for level in sorted(filter(lambda level: level.left == 2, levels), key=lambda level: level.star2):
            if level.star2 <= star:
                step += 1
                star += level.left
                #print '%d clear +%d => %d' % (level.star2, level.left, star)
                levels.remove(level)
            else:
                break

        # 2. すでに 1 star 取っているレベルで残りの star を取れるなら
        for level in sorted(filter(lambda level: level.left == 1, levels), key=lambda level: level.star2):
            if level.star2 <= star:
                step += 1
                star += level.left
                #print '%d clear +%d => %d' % (level.star2, level.left, star)
                levels.remove(level)
            else:
                break

        if star > begin:
            # ここまでにスターが増えていたらもう一度最初から
            continue

        # 3. 1 star しか取れないもったいないケース
        level = sorted(filter(lambda level: level.left == 2 and level.star1 <= star, levels),
                       key=lambda level: level.star2, reverse=True)
        if level:
            step += 1
            star += 1
            #print '%d clear +%d => %d' % (level[0].star1, 1, star)
            level[0].left -= 1
        else:
            # 1つも star を取れなかった
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

