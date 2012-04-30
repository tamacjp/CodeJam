#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Problem C. Recycled Numbers
# http://code.google.com/codejam/contest/1460488/dashboard#s=p2
#

import sys


def solve(A, B):
	# 桁数
	digits = len(str(A))
	# 重複する組み合せを避けるため set で持っておく
	found = set()

	for n in xrange(A, B):		# n=B のケースは検証不要(n < m <= B になりえない)
		for k in range(1, digits):
			# 数字の並びを移動した m を作る
			div = 10 ** k
			m = (n / div) + (n % div) * (10 ** (digits - k))
			if n < m and m <= B:
				# A <= n < m <= B の条件に合致する
				found.add((n, m))
	return len(found)


def main(IN, OUT):
	N = int(IN.readline())
	for index in range(N):
		A, B = map(int, IN.readline().strip().split())
		OUT.write('Case #%d: %d\n' % (index + 1, solve(A, B)))


def makesample(ABmax=2000000, T=50):
	import random
	print T
	for index in range(T):
		A = random.randint(1, ABmax)
		B = random.randint(A, ABmax)
		print A, B


if __name__ == '__main__':
	if '-makesample' in sys.argv[1:]:
		makesample()
	else:
		main(sys.stdin, sys.stdout)

