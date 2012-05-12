#!/usr/bin/env python
# -*- mode:python; coding:utf-8; indent-tabs-mode:nil -*-
#
# Problem B. Out of Gas
# http://code.google.com/codejam/contest/1781488/dashboard#s=p1
#

import sys
import math


# 前走車の位置情報
class OtherCar:
    def __init__(self, t, x):
        # t秒後に x の場所にいる
        self.t = t
        self.x = x


def solve(D, a, othercar):
    # 家(D)を越える前走車区間
    lasti = [index for index, car in enumerate(othercar) if car.x >= D][0]
    last = othercar[lasti]
    prev = othercar[lasti - 1] if lasti > 0 else None
    # 等速で移動している前走車が D に着く時間
    # 区間内距離 : 区間全体の距離 = 区間内の移動時間 : 区間全体の時間
    # (D - prev.x) / (last.x - prev.x) = (t - prev.t) / (last.t - prev.t)
    best = ((D - prev.x) / (last.x - prev.x) * (last.t - prev.t) + prev.t) if prev else 0.0
    # ※これより早くはなりえない

    # ノーブレーキでスタートから家まで移動するのにかかる時間
    # x = v0 * t + a * (t ** 2) / 2
    # 最初は静止しているので初速度 v0 = 0
    t = math.sqrt(D * 2 / a)
    # スタートから n 秒間動かずにじっとしていて、n 秒後にブレーキを緩めて走り出す → t 秒かけて家に着く
    n = max(0, best - t)
    # ※ n は走り始める時間。常に距離0(出発前の山頂)

    # 前走車の速度が変わるポイントごとに、自車が前走車より後ろにいることを確認
    for index in range(lasti, 0, -1):
        next = othercar[index]
        prev = othercar[index-1]

        # 出発時刻が prev.t 以降 ⇒ その出発時刻でOK
        if n >= prev.t:
            break

        # prev.t 時点での自車の位置
        x = a * ((prev.t - n) ** 2) / 2
        if x > prev.x:
            # 前走車より前にはいられない ⇒ 出発時間をずらして prev.t の時点で prev.x にする
            # a * ((prev.t - n) ** 2) / 2 = prev.x
            # (prev.t - n) ** 2 = prev.x * 2 / a
            # prev.t - n = math.sqrt(prev.x * 2 / a)
            n = prev.t - math.sqrt(prev.x * 2 / a)
        else:
            # prev.t の時点で自車は前走車より後ろにいる
            pass

    # 出発時刻 + 移動時間
    return n + t


def main(INPUT, OUTPUT):
    T = int(INPUT.readline())
    for index in range(T):
        # 進捗表示
        sys.stderr.write('#%d\r' % (index + 1))
        data = INPUT.readline().split()
        # 家までの距離D、前走車の位置情報N、加速度テストケース数A
        D, N, A = float(data[0]), int(data[1]), int(data[2])
        # 前走車の位置情報
        othercar = [OtherCar(*map(float, INPUT.readline().split())) for n in range(N)]
        # 加速度テストケース
        testcase = map(float, INPUT.readline().split())
        OUTPUT.write('Case #%d:\n' % (index + 1))
        for a in testcase:
            OUTPUT.write('%s\n' % solve(D, a, othercar))


def makesample(Nmax, Amax, T=100):
    import random
    print T
    for index in range(T):
        D = random.randint(1, 10**5) / 10.0
        N = random.randint(1, Nmax)
        A = random.randint(1, Amax)
        print D, N, A
        t, x = 0.0, 0.0
        for n in range(N):
            if n < N-1:
                x += random.randint(1, int(D / N * 10)) / 10.0
            else:
                # 最後はD以上
                x += D
            print t, x
            t += random.randint(1, 100) / 10.0
        print ' '.join(str(random.randint(100, 981) / 100.0) for a in range(A))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if ('-makesample', 'small') == tuple(sys.argv[1:]):
            makesample(2, 10)
        elif ('-makesample', 'large') == tuple(sys.argv[1:]):
            makesample(2000, 250)
        else:
            print 'usage: %s [-makesample <small|large>]' % sys.argv[0]
    else:
        main(sys.stdin, sys.stdout)

