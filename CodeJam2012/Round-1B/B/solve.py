#!/usr/bin/env python
# -*- mode:python; coding:utf-8; indent-tabs-mode:nil -*-
#
# Problem B. Tide Goes In, Tide Goes Out
# http://code.google.com/codejam/contest/1836486/dashboard#s=p1
#

import sys


class Square:
    def __init__(self, ceiling, floor, H):
        # 天井の高さ
        self.ceiling = ceiling
        # 床の高さ
        self.floor = floor
        # ここに入る条件水位
        h = self.ceiling - 50
        if self.floor > h:
            # 天井が低すぎて絶対に入れない
            self.time = None
        else:
            # ここに入れるのは何秒後?
            self.time = max((H - h) / 10.0, 0.0)

    def enter(self, prev):
        if prev.time is None:
            # そもそも元の場所に入れない
            return False
        if self.ceiling - prev.floor < 50:
            # 元の場所の床が高すぎる
            return False
        if prev.ceiling - self.floor < 50:
            # 元の場所の天井が低すぎる
            return False
        return True


def solve(H, N, M, squares):
    # 各 square に到達する最短時間
    timemap = [[None] * len(row) for row in squares]
    timemap[0][0] = 0.0  # squares[0][0].time
    # チェックキュー
    queue = [(0, 0)]

    while queue:
        x, y = queue.pop()
        current = squares[y][x]
        time = timemap[y][x]

        # どの方角へ進む?
        to = []
        if y > 0:
            # 北へ
            to.append((x, y - 1))
        if x > 0:
            # 西へ
            to.append((x - 1, y))
        if y < N - 1:
            # 南へ
            to.append((x, y + 1))
        if x < M - 1:
            # 東へ
            to.append((x + 1, y))

        # 候補の方角へ
        for newx, newy in to:
            next = squares[newy][newx]
            # ここから進める?
            if next.enter(current):
                # ここまでの最短時間 or 次のsquareに入れる時間
                wait = max(time, next.time)
                if wait > 0:
                    # 水位
                    h = H - 10 * wait
                    # 現在地の水位が20cm以上あればkayakで進める
                    wait += 1 if h - current.floor >= 20 else 10
                if timemap[newy][newx] is None or timemap[newy][newx] > wait:
                    # 新しく移動経路が見つかった or より短い経路が見つかった
                    timemap[newy][newx] = wait
                    # この場所からまた調べてください
                    queue.append((newx, newy))

    # ゴール(南東)に到達する最短時間
    return timemap[-1][-1]


def main(INPUT, OUTPUT):
    T = int(INPUT.readline())
    for index in range(T):
        # 進捗表示
        sys.stderr.write('#%d\r' % (index + 1))
        H, N, M = map(int, INPUT.readline().strip().split())
        ceiling = [map(int, INPUT.readline().strip().split()) for n in range(N)]
        floor = [map(int, INPUT.readline().strip().split()) for n in range(N)]
        squares = [[Square(c, f, H) for c, f in zip(C, F)] for C, F in zip(ceiling, floor)]
        OUTPUT.write('Case #%d: %s\n' % (index + 1, solve(H, N, M, squares)))


if __name__ == '__main__':
    main(sys.stdin, sys.stdout)

