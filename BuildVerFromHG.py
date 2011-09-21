#!/usr/bin/python
#

"""


"""

import os
import optparse
import os.path
import fnmatch
import string
import getopt
import sys
import re

debug = False

options = None



def main( argv ):
	"""Pull the current Mercurial version and write it to the XCode project's info file as the build version.

	(use option '-h' to get options help)
	"""

	global options, debug

	usage = "%prog [options] <strings file>"

	parser = optparse.OptionParser(usage=usage)

	parser.add_option( "-d", "--dir",
						action="store", type="string", dest="startdir", default=None,
						help="Directory to process.  (default is CD)" )

	parser.add_option( "-n", "--noActions",
						action="store_true", dest="noActions", default=False,
						help="no actions" )

	parser.add_option( "-o", "--outfile",
						action="store", type="string", dest="outfile", default=None,
						help="File to send the output data to" )

	parser.add_option( "-v", "--verbose",
						action="store_const", const=1, dest="verbose", default=1,
						help="verbose [default]" )

	parser.add_option( "-q", "--quiet",
						action="store_const", const=0, dest="verbose",
						help="quiet" )

	parser.add_option( "--noisy",
						action="store_const", const=2, dest="verbose",
						help="noisy" )

	(options, args) = parser.parse_args(argv)

	if options.verbose > 1:
		debug = True
		print options
		print args

	#print config.options.verbose

# 	if len(args) > 1:
# 		fn = args[1]
# 	else:
# 		print "No info file name given."
# 		print main.__doc__
# 		sys.exit(1)



	#
	# Perform the main processing.
	#
	fh = os.popen( "/usr/local/bin/hg id -i" )	# Ask Mercurial for the global version ID
	gv = fh.readline().strip()					# Read it from the process, and strip off the newline
	#print "'%s'" % gv

	# Build the path to the Info plist in the build products directory.
	infoPath = os.path.join( os.environ['BUILT_PRODUCTS_DIR'], os.environ['WRAPPER_NAME'], "Info" )
	print infoPath
	#cmd = "defaults read %s CFBundleVersion" % ( path )
	cmd = "defaults write %s CFBundleVersion %s" % ( infoPath, gv )
	#print cmd
	os.system( cmd )
	
	return 0	# Success



#------------------------------

if __name__ == '__main__':
	sys.exit( main(sys.argv) or 0 )


