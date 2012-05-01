#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Problem A. Password Problem
# http://code.google.com/codejam/contest/1645485/dashboard#s=p0
#

import sys


def solve(length, correctly):
	inputed = len(correctly)

	# N文字目で間違ってる可能性
	wrong = []
	left = 1
	for rate in correctly:
		wrong.append(left - left * rate)
		left *= rate

	def typecount(bs):
		# backspaceをbs回タイプ + bs文字入力し直し + 残り文字 + [Enter]
		return bs + bs + (length - inputed) + 1

	expected = []
	# backspace入力回数
	for backspace in range(inputed + 1):
		# 全て正しく入力していた場合
		count = [(typecount(backspace), left)]
		#print count[-1]
		# pos文字目で間違っている場合
		for pos, rate in enumerate(wrong):
			if pos < (inputed - backspace):
				# 間違いを訂正できない
				count.append((typecount(backspace) + length + 1, rate))
			else:
				count.append((typecount(backspace), rate))
			#print pos, count[-1]
		# 平均
		expected.append(sum(cnt * rate for cnt, rate in count))
		#print '#' * 5, backspace, expected[-1]
	# このまま [Enter] して入力し直す
	expected.append(1 + length + 1)

	return min(expected)


def main(INPUT, OUTPUT):
	T = int(INPUT.readline())
	for index in range(T):
		A, B = map(int, INPUT.readline().strip().split())
		correctly = map(float, INPUT.readline().strip().split())
		OUTPUT.write('Case #%d: %f\n' % (index + 1, solve(B, correctly)))


def makesample(Amax=3, Bmax=100, T=20):
	import random
	print T
	for index in range(T):
		A = random.randint(1, Amax)
		B = random.randint(A, Bmax)
		print A, B
		print ' '.join('%f' % (random.randint(0, 100) / 100.0) for n in range(A))


if __name__ == '__main__':
	if '-makesample' in sys.argv[1:]:
		makesample()
	else:
		main(sys.stdin, sys.stdout)

