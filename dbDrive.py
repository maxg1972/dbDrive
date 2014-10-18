"""
    dbDrive - database query executer
    =================================
    Utilities to facilitate databases querying. This is accomplished with an object that give you methods to read data
    from database (ex: SELECT queries) ore execute code (ex. INSERT queries) for MySQL, PostgreSQL, MS SQL and SQLite

    Requires
    -----
    All databases python modules or only modules of used databases.

    Usage
    -----
    Import the dbDrive.py file into your project and use the Dates object.

    Authors & Contributors
    ----------------------
        * Massimo Guidi <maxg1972@gmail.com>,

    License
    -------
    This module is free software, released under the terms of the Python
    Software Foundation License version 2, which can be found here:

        http://www.python.org/psf/license/

"""

__author__ = "Massimo Guidi"
__author_email__ = "maxg1972@gmail.com"
__version__ = '1.0'

#----------------------#
# Handling error class #
#----------------------#
class ConnectionError(Exception): pass

# ---------------------- #
# Database quering class #
# ---------------------- #
class dbDrive:
    #Database types (constants)
    DBTYPE_MYSQL = 'mysql'
    DBTYPE_POSTGRESQL = 'postgresql'
    DBTYPE_MSSQL = 'mssql'
    DBTYPE_SQLITE = 'sqllite'

    def __init__(self,dbType,dbName,dbHost='',dbPort='',dbUserName='',dbPassword=''):
        """
        Class constructor (open database connection)

        @param dbType: database type (use one of the defined constants)
        @param dbName: database name to be connected
        @param dbHost: database server name/ip (optional, default '')
        @param dbPort: database connection port (optional, default '')
        @param dbUserName: database login name (opzionale, default '')
        @param dbPassword: database login password (opzionale, default '')
        @raise ConnectionError: Invalid database type
        """
        #set internal variables
        self.__dbType = dbType
        self.__conn = None

        #make right database connection
        if dbType == self.DBTYPE_MYSQL:
            self.__mysql_connect(dbName,dbHost,dbPort,dbUserName,dbPassword)
        elif dbType == self.DBTYPE_POSTGRESQL:
            self.__pg_connect(dbName,dbHost,dbPort,dbUserName,dbPassword)
        elif dbType == self.DBTYPE_MSSQL:
            self.__mssql_connect(dbName,dbHost,dbPort,dbUserName,dbPassword)
        elif dbType == self.DBTYPE_SQLITE:
            self.__sqlite_connect(dbName)
        else:
            raise ConnectionError("Invalid database type!")

    def __del__(self):
        """
        Class destructor (close database connection)
        """
        if self.__conn:
            self.__conn.close()

    def __mysql_connect(self,dbName,dbHost,dbPort,dbUserName,dbPassword):
        """
        Open MySQL database connection (and import right database module)

        @param dbName: database name to be connected
        @param dbHost: mysql database server name/ip
        @param dbPort: database connection port
        @param dbUserName: database login name
        @param dbPassword: database login password
        @raise ConnectionError: MySQL python modules not found
        """
        try:
            import MySQLdb
    
            self.__conn = MySQLdb.connect(db=dbName,host=dbHost,port=dbPort,user=dbUserName,passwd=dbPassword)
        except:
            raise ConnectionError("'MySQLdb' python modules not found")

    def __pg_connect(self, dbName, dbHost, dbPort, dbUserName, dbPassword):
        """
        Open PostgreSql database connection (and import right database module)

        @param dbName: database name to be connected
        @param dbHost: postgresql database server name/ip
        @param dbPort: database connection port
        @param dbUserName: udatabase login name
        @param dbPassword: database login password
        @raise ConnectionError: PostgreSQL python modules not found
        """
        try:
            import psycopg2
    
            self.__conn = psycopg2.connect(database=dbName,host=dbHost,port=dbPort,user=dbUserName,password=dbPassword)
        except:
            raise ConnectionError("'psycopg2' python modules not found")

    def __mssql_connect(self, dbName, dbHost, dbPort, dbUserName, dbPassword):
        """
        Open MS SQL Server database connection (and import right database module)

        @param dbName: database name to be connected
        @param dbHost: MSSQL database server name/ip
        @param dbPort: database connection port
        @param dbUserName: udatabase login name
        @param dbPassword: database login password
        @raise ConnectionError: MSSQL Server python modules not found
        """
        try:
            import pymssql

            self.__conn = pymssql.connect(database=dbName,host=dbHost,port=dbPort,user=dbUserName,password=dbPassword,as_dict=True)
        except:
            raise ConnectionError("'pymssql' python modules not found")

    def __sqlite_connect(self, dbName):
        """
        Open SQLite database connection (and import right database module)

        @param dbName: database name to be connected
        @raise ConnectionError: SQLite python modules not found
        """
        try:
            import sqlite3

            try:
                self.__conn = sqlite3.connect(dbName)
                self.__conn.row_factory=sqlite3.Row
            except:
                raise ConnectionError("Connection error %s" % self.__dbType)
        except:
            raise ConnectionError("'sqlite3' python modules not found")

    def read(self,sql,args=None):
        """
        Execute query and return records (ex. SELECT)

        @param sql: query to be executed
        @param args: optional parameters sequence
        @return: return data as array od dictionary (filed_name, field_value)
        """
        cur = None

        #open database cursor
        if self.__dbType == self.DBTYPE_MYSQL:
            cur = self.__conn.cursor(MySQLdb.cursors.DictCursor)
        elif self.__dbType == self.DBTYPE_POSTGRESQL:
            cur = self.__conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        else:
            cur = self.__conn.cursor()

        #execute query
        cur.execute(sql,args)

        #give back data
        return cur.fetchall()

    def execute(self,sql,args=None):
        """
        Execute query without return records (ex. UPDATE, INSERT, ...)

        @param sql: query to be executed
        @param args: optional parameters sequence
        @return: 'True' for execution without errors, 'False' otherwise
        """
        cur = None

        #open database cursor
        if self.__dbType == self.DBTYPE_MYSQL:
            cur = self.__conn.cursor(MySQLdb.cursors.DictCursor)
        elif self.__dbType == self.DBTYPE_POSTGRESQL:
            cur = self.__conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        else:
            cur = self.__conn.cursor()

        #execute query
        try:
            cur.execute(sql,args)
            self.__conn.commit()
            return True
        except:
            self.__conn.rollback()
            return False