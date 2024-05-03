import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool


class Database:
    host = "localhost"
    user = "root"
    password = ""
    database = "odds_finder"
    pool = None

    @classmethod
    def get_connection(cls):
        if cls.pool is None:
            cls.pool = MySQLConnectionPool(
                pool_name="sql_pool",
                pool_size=5,
                host=cls.host,
                user=cls.user,
                password=cls.password,
                database=cls.database
            )
        return cls.pool.get_connection()

    @classmethod
    def execute_query(cls, query, params=None):
        with cls.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cls.__requires_commit(query):
                    conn.commit()
                result = cursor.fetchall()

        return result

    @classmethod
    def __requires_commit(cls, query):
        dml_keywords_which_need_commit = ['INSERT', 'UPDATE', 'DELETE']

        # Check if the query is a DML statement
        return cls.__get_query_type(query) in dml_keywords_which_need_commit

    @classmethod
    def __get_query_type(cls, query):
        parts = query.split()
        if parts:
            return parts[0]
        else:
            return None
