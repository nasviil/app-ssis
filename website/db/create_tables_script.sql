CREATE TABLE IF NOT EXISTS college (
    id INT AUTO_INCREMENT PRIMARY KEY,
    college_name VARCHAR(256) UNIQUE NOT NULL,
    college_code VARCHAR(16) UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(256) UNIQUE NOT NULL,
    course_code VARCHAR(16) UNIQUE NOT NULL,
    college_id INT,
    FOREIGN KEY (college_id) REFERENCES college(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(16) UNIQUE NOT NULL,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    gender VARCHAR(16) NOT NULL,
    year INT NOT NULL,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE,
    cloudinary_url VARCHAR(255)
);
