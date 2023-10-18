from website import mysql

class College:
    __tablename__ = 'college'

    def __init__(self, name=None, code=None, id=None):
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
