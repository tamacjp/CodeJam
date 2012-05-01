#!/usr/bin/env python
# -*- mode:python; coding:utf-8; indent-tabs-mode:nil -*-
#
# Problem A. Password Problem
# http://code.google.com/codejam/contest/1645485/dashboard#s=p0
#

import sys


def solve(length, correctly):
    inputed = len(correctly)

    # N文字目でミスタイプする確率
    wrong = []
    left = 1    # 残り
    for rate in correctly:
        # ミスタイプする確率
        wrong.append(left * (1 - rate))
        # 正しく入力して次の文字へ進む確率
        left *= rate

    # backspace入力回数別期待値
    expected = []
    for bs in range(inputed + 1):
        # backspaceをbs回タイプ + bs文字入力し直し + 残り文字 + [enter]
        count = bs + bs + (length - inputed) + 1
        # backspaceで消せなかったミスタイプがある確率
        misstype = sum(wrong[:inputed - bs])
        expected.append(
            # backspace で戻ってもミスが残ったままでもう一度入力し直す場合
            (count + length + 1) * misstype
            # backspace で戻って入力し直すと正解する場合
            + count * (1 - misstype))

    # このまま [enter] して入力し直す
    expected.append(1 + length + 1)

    # 最小の期待値を回答
    return min(expected)


def main(INPUT, OUTPUT):
    T = int(INPUT.readline())
    for index in range(T):
        # 進捗表示
        sys.stderr.write('#%d\r' % (index + 1))
        A, B = map(int, INPUT.readline().strip().split())
        correctly = map(float, INPUT.readline().strip().split())
        OUTPUT.write('Case #%d: %f\n' % (index + 1, solve(B, correctly)))


def makesample(Amax, Bmax, T=20):
    import random
    print T
    for index in range(T):
        A = random.randint(1, Amax)
        B = random.randint(A, Bmax)
        print A, B
        print ' '.join('%f' % (random.randint(0, 100) / 100.0) for n in range(A))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if ('-makesample', 'small') == tuple(sys.argv[1:]):
            makesample(3, 100)
        elif ('-makesample', 'large') == tuple(sys.argv[1:]):
            makesample(99999, 100000)
        else:
            print 'usage: %s [-makesample <small|large>]' % sys.argv[0]
    else:
        main(sys.stdin, sys.stdout)

