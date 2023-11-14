from website import mysql

class Course:
    __tablename__ = 'course'

    def __init__(self, id=None, course_name=None, course_code=None, college_id=None):
        self.id = id
        self.course_name = course_name
        self.course_code = course_code
        self.college_id = college_id

    def insert(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (course_name, course_code, college_id) VALUES (%s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(INSERT_SQL, (self.course_name, self.course_code, self.college_id))
        mysql.connection.commit()

    def update(self):
        UPDATE_SQL = f"UPDATE {self.__tablename__} SET course_name = %s, course_code = %s, college_id = %s WHERE id = %s"
        cur = mysql.connection.cursor()
        cur.execute(UPDATE_SQL, (self.course_name, self.course_code, self.college_id, self.id))
        mysql.connection.commit()

    def delete(self):
        DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id = %s"
        cur = mysql.connection.cursor()
        cur.execute(DELETE_SQL, (self.id,))
        mysql.connection.commit()

    @classmethod
    def get_courses(cls):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__}"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        courses = cur.fetchall()
        return courses

    @classmethod
    def get_courses_with_college(cls):
        SELECT_SQL = f"""
            SELECT course.*, college.college_name AS college_name, college.college_code AS college_code
            FROM {cls.__tablename__}
            JOIN college ON course.college_id = college.id
        """
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        courses = cur.fetchall()
        return courses

    
    @classmethod
    def get_colleges(cls):
        SELECT_COLLEGES_SQL = "SELECT id, college_name FROM college"
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_COLLEGES_SQL)
        colleges = cur.fetchall()
        return colleges
    
    @classmethod
    def is_course_unique(cls, course_name, course_code, college_id):
        SELECT_UNIQUE_SQL = "SELECT id FROM course WHERE course_name = %s AND course_code = %s AND college_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(SELECT_UNIQUE_SQL, (course_name, course_code, college_id))
        result = cur.fetchone()
        return result is None
    
    @classmethod
    def search_courses(cls, query):
        SELECT_SQL = (
            f"SELECT * FROM {cls.__tablename__} "
            "RIGHT JOIN college ON course.college_id = college.id "
            "WHERE course.course_name LIKE %s OR course.course_code LIKE %s OR college.college_name LIKE %s"
        )
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL, (f'%{query}%', f'%{query}%', f'%{query}%'))
        courses = cur.fetchall()
        return courses
