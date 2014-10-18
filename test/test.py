
from dbDrive import dbDrive

db = dbDrive(dbDrive.DBTYPE_SQLITE,'test.db')

data = db.read('SELECT * FROM test')

for row in data:
    print "a=%s, b=%s" % (row['a'],row['b'])