#!/usr/bin/python
#
# VersionHeaderForGit.py

import os
import os.path
import string
import sys


# kGitShortHash
# kGitTagHash
# kGitBranch

# Get branch info
fh = os.popen( "/usr/bin/git branch -v" )
line = fh.readline().strip()			# Read it from the process, and strip the newline

#print line
words = line.split()
branch = words[1]


fh = os.popen( "/usr/bin/git describe --always --dirty" )	# Ask Git for the short hash
hash = fh.readline().strip()			# Read it from the process, and strip the newline

#print line


fh = os.popen( "/usr/bin/git describe --always --tags --dirty" )	# Ask Git for the short hash
taghash = fh.readline().strip()			# Read it from the process, and strip the newline

#print line

header = "/* Git Version Header */\n\n"

header += "#define kGitShortHash @\"" + hash + "\"\n"

header += "#define kGitTagHash @\"" + taghash + "\"\n"

header += "#define kGitBranch @\"" + branch + "\"\n"

#print header

destName = "GitVersion.h"

if os.path.isfile( destName ):
	old = open( destName, "r" )
	oldh = old.read()
	if header != oldh:
		print "Writing GitVersion header file because the version has changed"
		dest = open( destName, "w" )
		dest.write(header)
		dest.close()
	else:
		print "Git versions unchanged, header file not re-written"	
else:
	# File does not exist, write it
	print "Writing GitVersion header file because it does not exist"
	dest = open( destName, "w" )
	dest.write(header)
	dest.close()

