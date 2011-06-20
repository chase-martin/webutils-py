#!/usr/bin/env python
import sys, os, time, datetime, glob

def backup_database():
	os.system( "echo begin database backup" )
	t = datetime.datetime.now()
	ts = t.strftime("%Y-%m-%d-%H-%M-%S")
	print ts

	db = dict();
	db['name'] = 'db'
	db['user'] = 'user'
	db['pass'] = 'pass'
	db['backupdir'] = '/var/www/website/scripts/backup/'
	db['backupfile'] = 'db_'+db['name']+"_"+ts
	db['backuppath'] = db['backupdir']+db['backupfile']
	# Set prune to 0 to delete all backup files
	db['prune'] = 30

	print "mysqldump -u %s -p%s %s > %s.sql" % ( db['user'], db['pass'], db['name'], db['backuppath'] 
)
	os.system( "mysqldump -u %s -p%s %s > %s.sql" % ( db['user'], db['pass'], db['name'], db['backuppath'] ) )
	print "compressing sql file"
	os.chdir( db['backupdir'] )
	os.system( "tar -cvzf %s.tar.gz %s.sql" % ( db['backuppath'], db['backupfile'] ) )
	print "removing sql file"
	os.system( "rm -rf %s.sql" % ( db['backuppath'] ) ) 
	print "checking for old directories"
	for f in glob.glob( "%s*.tar.gz" % (db['backupdir']) ):
		a = f.split('_')
		af = a[2].split('.')
		afs = af[0].split('-')
		aft = map(lambda x: int(x), afs)
		ft = datetime.datetime( aft[0], aft[1], aft[2], aft[3], aft[4], aft[5] ) 
		diff = t - ft
		if diff.days >= db['prune']:
			print "Deleting: %s" % ( f )
			os.system( "rm -rf %s" % ( f ) )
	os.system( "ls %s" % ( db['backupdir'] ) )
	return

backup_database()
sys.exit (0)
