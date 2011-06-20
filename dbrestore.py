#!/usr/bin/env python

import os, sys

db = dict()
db['name'] = 'db'
db['user'] = 'user'
db['pass'] = 'pass'
db['backupdir'] = '/var/www/backup/scripts/backup/'

if len(sys.argv) != 2: 
	print "Script requires backupfile.tar.gz as an argument"
else:
	print "Extrating archive:"+sys.argv[1]
	restorepath = db['backupdir']+sys.argv[1]
	os.system( 'tar -zxvf %s' % ( restorepath ) )
	print "importing database to mysql"
	sqlfile = sys.argv[1][:-7]
	os.system( "mysql -u %s -p%s %s < %s.sql" % ( db['user'], db['pass'], db['name'], sqlfile ) )
	os.system( "rm -f %s" % ( sqlfile ) )
print "complete"
