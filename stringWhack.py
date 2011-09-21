#!/usr/bin/python
#
# stringWhack.py
#


"""
Processes a strings file by making the comment for each entry become the value assigned to that entry's key.

"""

import os
import optparse
import os.path
import fnmatch
import string
import getopt
import sys
import re
import ConfigParser
import StringIO
import codecs


debug = False

options = None


def processFile( name ):
	if options.noActions:
		return

	inputfile = codecs.open( name, "r", "utf-16" )
	lines = inputfile.readlines()
	inputfile.close()

	dest = codecs.open( name, "w", "utf-16" )

	comment = None
	for line in lines:
		#line = line[:-1]
		line = line.strip()
		#m = re.match( r'^([a-fA-F0-9]+)\s+([a-fA-F0-9---]+)\s+([a-fA-F0-9---]+)\s+(.*)', line )
		m = re.match( r'\s*/\*\s*(.+?)\s*\*/\s*', line )
		#m = re.match( r'\s*out\s*', line )
		#m = re.match( r'out', line )
		if m:
			comment = m.group(1)
			#print "COMMENT: '%s'" % comment
			#start = string.atoi( m.group(1), 10 )
		else:
			m = re.match( r'\s*(\S+?)\s*=\s*"(.*)"\s*;', line )
			if m:
				#print "STRING: key='%s', value='%s'" % ( m.group(1), m.group(2) )
				if comment:
					print >> dest, "/* %s */" % comment
					print >> dest, '%s = "%s";\n' % ( m.group(1), comment )
					comment = None
				else:
					print "** No comment preceding line: '%s'" % line
					print >> dest, line
			else:
				m = re.match( r'\s*"(.+)"\s*=\s*"(.*)"\s*;', line )
				if m:
					#print "QSTRING: key='%s', value='%s'" % ( m.group(1), m.group(2) )
					if comment:
						print >> dest, "/* %s */" % comment
						print >> dest, '"%s" = "%s";\n' % ( m.group(1), comment )
						comment = None
					else:
						print "** No comment preceding line: '%s'" % line
						print >> dest, line
				else:
					if len(line) > 0:
						print "** Skipped line: '%s'" % line
	dest.close()




def main( argv ):
	"""Process a strings file created by the Mac 'genstrings' tool.

	(use option '-h' to get options help)
	"""

	global options, debug

	usage = "%prog [options] <file>"

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

	if len(args) > 1:
		fn = args[1]
	else:
		print "No strings file name given."
		print main.__doc__
		sys.exit(1)

	#
	# Perform the main processing.
	#
	processFile( fn )

	return 0	# Success



#------------------------------

if __name__ == '__main__':
	sys.exit( main(sys.argv) or 0 )


