
from dbDrive import dbDrive

#--- SQLLITE Test ---#
db = dbDrive(dbDrive.DBTYPE_SQLITE,'test.db')

# select query without parameters
data = db.read('SELECT * FROM test')

print "select without parameters:"
for row in data:
    print "a=%s, b=%s" % (row['a'],row['b'])

# select with parameters
t = (1,)
data = db.read('SELECT * FROM test WHERE a = ?', t)

print "\nselect with parameters:"
for row in data:
    print "a=%s, b=%s" % (row['a'],row['b'])

# update
t = (1,1,)
result = db.execute('UPDATE test SET b=10 WHERE a = ? and b = ?', t)

if result:
    t = (1,)
    data = db.read('SELECT * FROM test WHERE a = ?', t)
    print "\nselect after update:"
    for row in data:
        print "a=%s, b=%s" % (row['a'],row['b'])

# insert
t = (1,5,)
result = db.execute('INSERT INTO test (a,b) VALUES (?,?)', t)

if result:
    t = (1,)
    data = db.read('SELECT * FROM test WHERE a = ?', t)
    print "\nselect after insert:"
    for row in data:
        print "a=%s, b=%s" % (row['a'],row['b'])

# delete
t = (1,5,)
result = db.execute('DELETE FROM test WHERE a = ? and b = ?', t)

if result:
    t = (1,)
    data = db.read('SELECT * FROM test WHERE a = ?', t)
    print "\nselect after delete:"
    for row in data:
        print "a=%s, b=%s" % (row['a'],row['b'])