from website import mysql

class College:
    __tablename__ = 'college'

    def __init__(self, id=None , college_name=None, college_code=None):
        self.id = id
        self.college_name = college_name
        self.college_code = college_code

    def insert(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (college_name, college_code) VALUES (%s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(INSERT_SQL, (self.college_name, self.college_code))
        mysql.connection.commit()

#rubber ducky

    def update(self):
        UPDATE_SQL = f"UPDATE {self.__tablename__} SET college_name = %s, college_code = %s WHERE id = %s"
        cur = mysql.connection.cursor()
        cur.execute(UPDATE_SQL, (self.college_name, self.college_code, self.id))
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
    def is_college_unique(cls, college_name, college_code):
        SELECT_UNIQUE_SQL = "SELECT id FROM college WHERE college_name = %s AND college_code = %s"
        cur = mysql.connection.cursor()
        cur.execute(SELECT_UNIQUE_SQL, (college_name, college_code))
        result = cur.fetchone()
        return result is None
    
    @classmethod
    def search_colleges(cls, query):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__} WHERE college_name LIKE %s OR college_code LIKE %s"
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL, (f'%{query}%', f'%{query}%'))
        colleges = cur.fetchall()
        return colleges
