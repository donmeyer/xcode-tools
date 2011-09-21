#!/usr/bin/python
#
# stringCheck.py
#
# Scan source code and the localized strings file and warn about problems such as:
#   Keys in source with no matching entry in the localized strings file
#   Unused localized strings
#   Strings in source that are not localized
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
import ConfigParser
import StringIO
import codecs

debug = False

options = None

stringsFileDict = {}	# Stores keys and LocalizedEntry objects as values from the Localized strings file

sourceStringList = []   # List of SourceString objects representing all of the strings we found in the source files

extensionList = [ '.m', '.c', '.cpp' ]



class LocalizedEntry:
	"""
	value -- string value
	"""
	def __init__( self, value ):
		self.value = value
		self.usedCount = 0

	def bumpUsage( self ):
		self.usedCount += 1

	def __repr__(self):
		return "{ LocalizedEntry: used count=%2d,  value='%s' }" % \
			( self.usedCount, self.value )


class SourceString:
	"""
	key -- string value
	"""
	def __init__( self, key, file, line ):
		self.key = key
		self.file = file
		self.line = line
		#self.usedCount = 0

	def __repr__(self):
		return "{ SourceString: key='%s', file='%s', line=%d }" % \
			( self.key, self.file, self.line )




def loadStringsFile( name ):
	inputfile = codecs.open( name, "r", "utf-16" )
	lines = inputfile.readlines()
	inputfile.close()

	comment = None
	for line in lines:
		line = line[:-1]
		#m = re.match( r'^([a-fA-F0-9]+)\s+([a-fA-F0-9---]+)\s+([a-fA-F0-9---]+)\s+(.*)', line )
		m = re.match( r'\s*(\S+?)\s*=\s*"(.*)"\s*;', line )
		if m:
			#print "STRING: key='%s', value='%s'" % ( m.group(1), m.group(2) )
			addKey( m.group(1), m.group(2) )
		else:
			m = re.match( r'\s*"(.+)"\s*=\s*"(.*)"\s*;', line )
			if m:
				#print "QSTRING: key='%s', value='%s'" % ( m.group(1), m.group(2) )
				addKey( m.group(1), m.group(2) )



def addKey( key, value ):
	if stringsFileDict.has_key( key ):
		print "*** Key '%s' found multiple times in the localized strings file!" % key
	else:
		entry = LocalizedEntry( value )
		stringsFileDict[key] = entry



def processSourceFile( name ):
	if options.noActions:
		return

	inputfile = open( name, "r" )
	lines = inputfile.readlines()
	inputfile.close()

	lnum = 0
	for line in lines:
		lnum += 1
		line = line.strip()
		# Search for the function that converts the localized strings, and make a SourceString entry for it
		# NSLocalizedString( "key", "comment" )
		#m = re.match( r'.*NSLocalizedString\s*\(\s*"(.*)"\s*,\s*"(.*)".*', line )
		pat1 = r'.*%s\s*\(\s*@"(.*?)"(.*)' % "NSLocalizedString"
		m = re.match( pat1, line )
		if m:
			#print "Bingo: %s" % m.group(1)
			# Optional - parse the comment string
			m2 = re.match( r'\s*,\s*@"(.*?)".*', m.group(2) )
			if m2:
				#print "Comment is '%s'" % m2.group(1)
				pass
			ss = SourceString( m.group(1), name, lnum )
			sourceStringList.append( ss )


def matchExtension( name, extlist ):
	for ext in extlist:
		if name.endswith( ext ):
			return True
	return False



def processDirectory( arg, dirname, names ):
    if debug: print "------ " + dirname + " ------"
    for fn in names:
		if matchExtension( fn, extensionList ):
			an = os.path.join( dirname, fn )
			if os.path.isfile( an ):
				processSourceFile( an )



def loadSourceFiles( startdir ):
    os.path.walk( startdir, processDirectory, "zot" )




def generateReport():
	for ss in sourceStringList:
		# Localized string got this source string?
		if stringsFileDict.has_key( ss.key ):
			stringsFileDict[ss.key].bumpUsage()
		else:
			print "No translation for key '%s' at line %d of file '%s'" % ( ss.key, ss.line, ss.file )
	print "\n---------------------------"
	for key in stringsFileDict:
		entry = stringsFileDict[key]
		if entry.usedCount == 0:
			print "Unused Localized String '%s', value of '%s'" % ( key, entry.value )



def main( argv ):
	"""Process a localized strings file and report on problems between it and the localized strings in the source code files.

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

	if len(args) > 1:
		fn = args[1]
	else:
		print "No strings file name given."
		print main.__doc__
		sys.exit(1)

	#
	# Perform the main processing.
	#
	loadStringsFile( fn )
	loadSourceFiles( "." )
	generateReport()

	return 0	# Success



#------------------------------

if __name__ == '__main__':
	sys.exit( main(sys.argv) or 0 )


