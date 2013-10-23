#!/usr/bin/python
#
# Obtain the current Git version for the local repository, and write this to the
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


# Configurations that allow uncommitted changes.
# If a configuration like "Release" is not in this list, the script will generate an error
# if there are changes that haven't been committed when a release build is attempted.
uncommittedAllowed = [ 'Debug' ]
#uncommittedAllowed = [ 'Debug', 'AdHoc', 'Release' ]

# Configurations for which we do NOT set the bundle version to our Git version ID.
inhibitBundleVersionConfigs = [ 'Release' ]


fh = os.popen( "/usr/bin/git describe --always --dirty" )	# Ask Git for the short hash
buildVer = fh.readline().strip()			# Read it from the process, and strip the newline
print "Build Version '%s'" % buildVer

# Build config - typically 'Debug', 'Release', etc.
config = os.environ['CONFIGURATION']

if buildVer[-5:] == 'dirty':
	# Uncommitted changes
	print "Uncommited changes"
	
	# Check to see if this should cause a build error.
	if not config in uncommittedAllowed:
		# For this configuration, doing a build with uncommitted changes is an error.
		print "ERROR: Uncommitted changes in the repository while doing %s build!" % config
		sys.exit( 1 )

	buildVer = buildVer[:-6] + "+"	# Remove the "-dirty" and add a plus sign


# Is this a config that we want to set the bundle version in?
if not config in inhibitBundleVersionConfigs:
	# Build the path to the Info plist in the build products directory.
	infoPath = os.path.join( os.environ['BUILT_PRODUCTS_DIR'], os.environ['WRAPPER_NAME'], "Info" )
	#print infoPath
	
	print "Setting build version of '%s' to PList %s" % ( buildVer, infoPath )
	
	#cmd = "defaults read %s CFBundleVersion" % ( infoPath )
	cmd = 'defaults write "%s" CFBundleVersion %s' % ( infoPath, buildVer )
	#print cmd
	os.system( cmd )
else:
	print "Configuration %s: Build version unchanged." % config

sys.exit( 0 )	# Success
