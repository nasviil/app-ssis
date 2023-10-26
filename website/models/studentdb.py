from website import mysql

class Student:
    __tablename__ = 'student'

    def __init__(self, id=None, student_id=None, first_name=None, last_name=None, gender=None, year=None, course_id=None):
        self.id = id
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.year = year
        self.course_id = course_id

    def insert(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (student_id, first_name, last_name, gender, year, course_id ) VALUES (%s, %s, %s, %s, %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(INSERT_SQL, (self.student_id, self.first_name, self.last_name, self.gender, self.year, self.course_id))
        mysql.connection.commit()

    def update(self):
        UPDATE_SQL = f"UPDATE {self.__tablename__} SET student_id = %s, first_name = %s, last_name = %s, gender = %s, year = %s, course_id = %s WHERE id = %s"
        cur = mysql.connection.cursor()
        cur.execute(UPDATE_SQL, (self.student_id, self.first_name, self.last_name, self.gender, self.year, self.course_id, self.id))
        mysql.connection.commit()

    def delete(self):
        DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id = %s"
        cur = mysql.connection.cursor()
        cur.execute(DELETE_SQL, (self.id,))
        mysql.connection.commit()

    @classmethod
    def get_students(cls):
        SELECT_SQL = f"SELECT * FROM {cls.__tablename__}"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        students = cur.fetchall()
        return students

    @classmethod
    def get_students_with_courses(cls):
        SELECT_SQL = f"""
            SELECT student.*, course.name AS course_name, course.code AS course_code, college.code AS college_code
            FROM {cls.__tablename__}
            JOIN course ON student.course_id = course.id
            JOIN college ON course.college_id = college.id
            ORDER by student.id DESC
        """
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        students = cur.fetchall()
        return students

    @classmethod
    def get_courses(cls):
        SELECT_COURSES_SQL = "SELECT id, name FROM course"
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_COURSES_SQL)
        courses = cur.fetchall()
        return courses

    @classmethod
    def is_student_unique(cls, student_id, first_name, last_name, gender, year, course_id):
        SELECT_UNIQUE_SQL = "SELECT id FROM student WHERE student_id = %s AND first_name = %s AND last_name = %s AND gender = %s AND year = %s AND course_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(SELECT_UNIQUE_SQL, (student_id, first_name, last_name, gender, year, course_id))
        result = cur.fetchone()
        return result is None
    
    @classmethod
    def search_students(cls, query):
        SELECT_SQL = f"""
            SELECT student.*, course.name AS course_name, college.code AS college_code
            FROM {cls.__tablename__}
            LEFT JOIN course ON student.course_id = course.id
            LEFT JOIN college ON course.college_id = college.id
            WHERE student.student_id LIKE %s 
                OR student.first_name LIKE %s 
                OR student.last_name LIKE %s 
                OR (student.gender = %s) 
                OR student.year LIKE %s 
                OR course.name LIKE %s
                OR college.code LIKE %s
        """
        cur = mysql.connection.cursor(dictionary=True)
        cur.execute(SELECT_SQL, (f'%{query}%', f'%{query}%', f'%{query}%', query, f'%{query}%', f'%{query}%', f'%{query}%'))
        students = cur.fetchall()
        return students
