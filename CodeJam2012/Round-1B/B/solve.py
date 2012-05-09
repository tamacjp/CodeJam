#!/usr/bin/env python
# -*- mode:python; coding:utf-8; indent-tabs-mode:nil -*-
#
# Problem B. Tide Goes In, Tide Goes Out
# http://code.google.com/codejam/contest/1836486/dashboard#s=p1
#

import sys


# 必要な高さ
REQUIRE_HEIGHT = 50
# 水位の下がる速度
WATERDROP_SPEED = 10.0
# kayakで進むのに必要な水位
REQUIRE_WATER = 20
# kayakで進む速度
KAYAK_SPEED = 10
# 歩いて進む速度
WALK_SPEED = 1


class Square:
    def __init__(self, ceiling, floor, H):
        # 天井の高さ
        self.ceiling = ceiling
        # 床の高さ
        self.floor = floor
        # ここに入る条件水位
        h = self.ceiling - REQUIRE_HEIGHT
        if self.floor > h:
            # 天井が低すぎて絶対に入れない
            self.time = None
        else:
            # ここに入れるのは何秒後?
            self.time = max((H - h) / WATERDROP_SPEED, 0.0)

    def enter(self, prev):
        if self.time is None:
            # この場所には入れない
            return False
        if self.ceiling - prev.floor < REQUIRE_HEIGHT:
            # 元の場所の床が高すぎる
            return False
        if prev.ceiling - self.floor < REQUIRE_HEIGHT:
            # 元の場所の天井が低すぎる
            return False
        return True


def solve(H, N, M, squares):
    start = (0, 0)

    # 各 square に到達する最短時間
    timemap = {}
    timemap[start] = squares[start].time
    # チェックキュー
    queue = set()
    queue.add(start)

    while queue:
        # キューからチェックする座標を取得
        x, y = queue.pop()
        # チェックするsquareとそこに来るまでの最短時間
        current = squares[(x, y)]
        time = timemap[(x, y)]

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
            square = squares[(newx, newy)]
            # ここから進める?
            if square.enter(current):
                # ここまでの最短時間 or 次のsquareに入れる時間
                wait = max(time, square.time)
                if wait > 0:
                    # 水位
                    h = H - WATERDROP_SPEED * wait
                    # 現在地の水位が20cm以上あればkayakで進める
                    wait += WALK_SPEED if h - current.floor >= REQUIRE_WATER else KAYAK_SPEED
                if (newx, newy) not in timemap or timemap[(newx, newy)] > wait:
                    # 新しく移動経路が見つかった or より速い経路が見つかった
                    timemap[(newx, newy)] = wait
                    # この場所を調べ直すべくキューに入れる
                    queue.add((newx, newy))

    # ゴール(南東)に到達する最短時間 ※必ず経路があるはず…
    return timemap[(M - 1, N - 1)]


def main(INPUT, OUTPUT):
    T = int(INPUT.readline())
    for index in range(T):
        # 進捗表示
        sys.stderr.write('#%d\r' % (index + 1))
        # 水位, マップの高さと幅
        H, N, M = map(int, INPUT.readline().split())
        # 天井の高さ
        ceiling = [map(int, INPUT.readline().split()) for n in range(N)]
        # 床の高さ
        floor = [map(int, INPUT.readline().split()) for n in range(N)]
        # squareマップ構成
        squares = dict(((x, y), Square(c, f, H))
                       for y, (C, F) in enumerate(zip(ceiling, floor))
                       for x, (c, f) in enumerate(zip(C, F)))
        OUTPUT.write('Case #%d: %s\n' % (index + 1, solve(H, N, M, squares)))


if __name__ == '__main__':
    main(sys.stdin, sys.stdout)

