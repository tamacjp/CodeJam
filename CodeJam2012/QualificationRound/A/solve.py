#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Problem A. Speaking in Tongues
# http://code.google.com/codejam/contest/1460488/dashboard#s=p0
#

import sys
import string

# 問題文の Sample より
INPUT = '''
ejp mysljylc kd kxveddknmc re jsicpdrysi
rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd
de kr kd eoya kw aej tysr re ujdr lkgc jv
'''.strip()
OUTPUT = '''
our language is impossible to understand
there are twenty six factorial possibilities
so it is okay if you want to just give up
'''.strip()


class Table(dict):
	TARGET = string.ascii_lowercase

	def translate(self, msg):
		# 対象文字(TARGET)なら変換、それ以外(スペース)はそのまま出力
		return ''.join((self[c] if c in self.TARGET else c) for c in msg)

	@classmethod
	def maketable(cls, src, dst):
		table = cls()
		srcchars = set(cls.TARGET)
		dstchars = set(cls.TARGET)

		def setletter(googlerese, english):
			if googlerese in table:
				if table[googlerese] != english:
					# 以前の対応と異なる ⇒ エラー(何か異常?)
					raise Exception('BAD MAPPING "%s" => "%s"/"%s"' % (googlerese, table[googlerese], english))
			else:
				# 対応を保持しておく
				table[googlerese] = english
				srcchars.remove(googlerese)
				dstchars.remove(english)

		# 問題文にあった対応
		setletter('y', 'a')
		setletter('e', 'o')
		setletter('q', 'z')

		# 入力と出力を対応付ける
		for s, d in zip(src, dst):
			if s in cls.TARGET:
				setletter(s, d)

		# 残りの文字を対応付ける
		if len(srcchars) == len(dstchars) == 1:
			table[srcchars.pop()] = dstchars.pop()
		return table


def main():
	# 変換テーブルを作る
	table = Table.maketable(INPUT, OUTPUT)
	N = int(sys.stdin.readline())
	for index in range(N):
		# 入力を変換して出力
		line = sys.stdin.readline().strip()
		print 'Case #%d:' % (index + 1), table.translate(line)


if __name__ == '__main__':
	main()

