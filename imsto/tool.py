#!/usr/bin/env python
# encoding: utf-8
"""
tool.py

Created by liut on 2010-12-24.
Copyright (c) 2010 liut. All rights reserved.
"""

import sys
import os
import getopt
from store import ImSto

help_message = '''
Usage: store.py [options] [filename]

Options:
  -i, --import     Import file to storeage
  -q, --id        get a file by id
  -l, --list       List files
  -m, --meta filename      get a file meta
  -t, --test       test a file
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output

'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hi:q:lm:t:v", ["help", "import=", "id=", "list", "meta", "test", "verbose", "limit=", "start="])
		except getopt.error, msg:
			raise Usage(msg)
		
		#print(opts)
		#print(args)
		action = None
		store_file = None
		limit = 5
		start = 0
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option == "--limit":
				limit = int(value)
			if option == "--start":
				start = int(value)

			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-i", "--import"):
				store_file = value
				print('store file: {0}'.format(store_file))
				action = 'import'
			elif option in ("-l", "--list"):
				action = 'list'
			elif option in ("-t", "--test"):
				action = 'test'
				filename = value
			elif option in ("-m", "--meta"):
				action = 'meta'
				path = value
			elif option in ("-q", "--id"):
				action = 'get'
				id = value
			else:
				pass
		
		if action is None:
			raise Usage(help_message)

		print('action: {}'.format(action))
		if (action == 'list'):
			imsto = ImSto()
			gallery = imsto.browse(limit, start)
			for img in gallery['items']:
				#print(img)
				print("{0[filename]}\t{0[length]:8,d}".format(img))
			return 0
		elif (action == 'get') and id is not None:
			imsto = ImSto()
			if not imsto.exists(id):
				print ('not found')
				return 1
			gf = imsto.get(id)
			#print(gf)
			print ("found: {0.name}\t{0.length}".format(gf))
			return 0
		elif action == 'import':
			if os.access(store_file, os.R_OK):
				imsto = ImSto()
				from _util import guess_mimetype
				ctype = guess_mimetype(store_file)
				with open(store_file) as fp:
					ret = imsto.store(fp, ctype)
					print ret
			else:
				print 'image {} not found or access deny'.format(store_file)
			return 0
		elif action == 'meta':
			print 'meta for path: {}'.format(path)
			imsto = ImSto()
			print imsto.meta(path=path)
		elif (action == 'test'):
			print('filename: %r' % filename)
			fp = open(filename, 'rb')
			h = fp.read(32)
			print(getImageType(h))
			return 0
				

	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		#print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())
