from website import mysql

class College:
    __tablename__ = 'college'

    def __init__(self, id=None , name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

    def insert(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (id, name, code) VALUES (%s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(INSERT_SQL, (self.id, self.name, self.code))
        mysql.connection.commit()

    def update(self):
        UPDATE_SQL = f"UPDATE {self.__tablename__} SET name = %s, code = %s WHERE id = %s"
        cur = mysql.connection.cursor()
        cur.execute(UPDATE_SQL, (self.name, self.code, self.id))
        mysql.connection.commit()

    @classmethod
    def get_colleges(cls):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__}"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        colleges = cur.fetchall()
        return colleges

    def delete(self):
        DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id = %s"
        cur = mysql.connection.cursor()
        cur.execute(DELETE_SQL, (self.id,))
        mysql.connection.commit()

    @classmethod
    def is_college_unique(cls, name, code):
        SELECT_UNIQUE_SQL = "SELECT id FROM college WHERE name = %s AND code = %s"
        cur = mysql.connection.cursor()
        cur.execute(SELECT_UNIQUE_SQL, (name, code))
        result = cur.fetchone()
        return result is None
    
    @classmethod
    def search_colleges(cls, query):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__} WHERE name LIKE %s OR code LIKE %s"
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL, (f'%{query}%', f'%{query}%'))
        colleges = cur.fetchall()
        return colleges
