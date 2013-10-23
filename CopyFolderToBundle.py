#!/usr/bin/python
#
#

import os
import os.path
import string
import sys



destPath = os.path.join( os.environ['BUILT_PRODUCTS_DIR'], os.environ['WRAPPER_NAME'] )
print "Dest path: %s" % destPath



def processFile( name ):
	print "Copy: %s" % name
	cmd = 'cp "%s"  "%s"' % ( name, destPath )
	os.system( cmd )



def processDirectory( arg, dirname, names ):
	print dirname
	head, tail = os.path.split( dirname )
	if tail.startswith( "." ):
		print "Skipping %s" % dirname
	else:
		for fn in names:
			if not fn.startswith( "." ):
				an = os.path.join( dirname, fn )
				if os.path.isfile( an ):
					processFile( an )


def process( startdir ):
    os.path.walk( startdir, processDirectory, "zot" )







args = sys.argv

if len(args) > 1:
	srcPath = args[1]
else:
	print "Must give a source folder argument"
	sys.exit(1)

process( srcPath )


sys.exit( 0 )	# Success
