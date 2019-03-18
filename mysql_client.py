from mysql.connector import connection
from mysql.connector import pooling

class MysqlClients:
    def __init__(self,**kwargs):
        self.pool = pooling.MySQLConnectionPool(pool_name           =   kwargs["pool_name"],
                                                pool_size           =   kwargs["pool_size"],
                                                host                =   kwargs["host"],
                                                port                =   kwargs["port"],
                                                database            =   kwargs["database"],
                                                user                =   kwargs["user"],
                                                password            =   kwargs["password"],
                                                charset             =   "utf8",
                                                pool_reset_session  =   True)

        self.config = kwargs

    def execute(self,sql):
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary = True)
        cursor.execute(sql)

    def execute_many(self,sql,data):
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary = True)
        cursor.executemany(sql,data)

    def query(self,sql):
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary = True)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

class MysqlClient:
    def __init__(self,**kwargs):
        self.config = kwargs
        self.conn = connection.MySQLConnection(user      =   kwargs["user"], 
                                               password  =   kwargs["password"],
                                               host      =   kwargs["host"],
                                               port      =   kwargs["port"],
                                               database  =   kwargs["database"],
                                               charset   =   "utf8")
        self.cursor = self.conn.cursor(dictionary = True)
    
    def reconnect(self):
        self.close()
        self.conn = connection.MySQLConnection(user      =   self.config["user"], 
                                               password  =   self.config["password"],
                                               host      =   self.config["host"],
                                               port      =   self.config["port"],
                                               database  =   self.config["database"],
                                               charset   =   "utf8")
        self.cursor = self.conn.cursor(dictionary = True)   
    

    def execute(self,sql,params=None):
        try:
            self.cursor.execute(sql,params)
        except Exception as e:
            if "Lost connection" in str(e):
                self.reconnect()
                self.cursor.execute(sql,params)

    def execute_many(self,sql,data):
        try:
            self.cursor.executemany(sql,data)
        except Exception as e:
            if "Lost connection" in str(e):
                self.reconnect()
                self.cursor.executemany(sql,data)

    def query(self,sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            if "Lost connection" in str(e):
                self.reconnect()
                self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
    
    def close(self):
        self.cursor.close()
        self.conn.close()

