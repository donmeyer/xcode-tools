#!/usr/bin/python
#
# Obtain the current Mercurial version for the local repository, and write this to the
# build version of the XCode project this script is run from.
# Also can check the build configuration and generate an error if uncommited changes exist
# and (for example) a Release build is being made.
#
# This script expects to be run as a build phase between Link Binary With Libraries and
# Copy Bundle Resources.
#

import os
import os.path
import string
import sys


# Set this to true to cause the IDs to be shortened to "XXXX" or "XXXX+"
shortenID = 0

# Configurations that allow uncommitted changes.
# If a configuration like "Release" is not in this list, the script will generate an error
# if there are changes that haven't been committed when a release build is attempted.
uncommittedAllowed = [ 'Debug' ]
#uncommittedAllowed = [ 'Debug', 'AdHoc', 'Release' ]

fh = os.popen( "/usr/local/bin/hg id -i" )	# Ask Mercurial for the global version ID
buildVer = fh.readline().strip()			# Read it from the process, and strip the newline
print "Build Version '%s'" % buildVer

if buildVer[-1:] == '+':
	# Plus sign at the end means uncommitted changes
	print "Uncommited changes"
	
	# Check to see if this should cause a build error.
	config = os.environ['CONFIGURATION']
	if not config in uncommittedAllowed:
		# For this configuration, doing a build with uncommitted changes is an error.
		print "ERROR: Uncommitted changes in the repository while doing %s build!" % config
		sys.exit( 1 )

	# Do we want a shorter ID?
	if shortenID:
		buildVer = buildVer[:2] + buildVer[-3:]	# First two chars and the last three chars (plus sign)	
else:
	# Do we want a shorter ID?
	if shortenID:
		buildVer = buildVer[:2] + buildVer[-2:]	# First two chars and the last two chars

# Build the path to the Info plist in the build products directory.
infoPath = os.path.join( os.environ['BUILT_PRODUCTS_DIR'], os.environ['WRAPPER_NAME'], "Info" )
#print infoPath

print "Setting build version of '%s' to PList %s" % ( buildVer, infoPath )

#cmd = "defaults read %s CFBundleVersion" % ( infoPath )
cmd = 'defaults write "%s" CFBundleVersion %s' % ( infoPath, buildVer )
#print cmd
os.system( cmd )

sys.exit( 0 )	# Success
