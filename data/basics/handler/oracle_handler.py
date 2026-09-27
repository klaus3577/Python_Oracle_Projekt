import os
from typing import List, Dict, Any

try:
    import cx_Oracle
except ImportError:  # the rest of the pipeline still runs without Oracle
    cx_Oracle = None


class OracleHandler:
    """Oracle database connection and table management.

    Credentials are passed in by the caller (see app.py, which reads them from
    environment variables). If the Oracle Instant Client is not on the system
    PATH, set ORACLE_CLIENT_LIB_DIR to its folder.
    """

    _client_initialised = False

    def __init__(self, username: str, password: str, dsn: str):
        if cx_Oracle is None:
            raise RuntimeError("cx_Oracle is not installed (pip install cx_Oracle)")

        lib_dir = os.getenv("ORACLE_CLIENT_LIB_DIR")
        if lib_dir and not OracleHandler._client_initialised:
            cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            OracleHandler._client_initialised = True

        self.connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        self.cursor = self.connection.cursor()
    
    def create_tables(self):
        "Táblák létrehozása külső kulcsokkal"
        
        # University tábla (elsődleges kulcs)
        self.cursor.execute("""
            CREATE TABLE universities (
                university_id VARCHAR2(5) PRIMARY KEY,
                name VARCHAR2(200) NOT NULL,
                city VARCHAR2(100) NOT NULL,
                country VARCHAR2(100) NOT NULL,
                founded_year NUMBER(4) NOT NULL,
                ranking NUMBER(5) NOT NULL,
                website VARCHAR2(200)
            )
        """)
        
        # Course tábla (elsődleges kulcs)
        self.cursor.execute("""
            CREATE TABLE courses (
                course_id NUMBER(10) PRIMARY KEY,
                course_code VARCHAR2(20) UNIQUE NOT NULL,
                course_name VARCHAR2(200) NOT NULL,
                credits NUMBER(2) NOT NULL,
                semester VARCHAR2(50) NOT NULL,
                instructor VARCHAR2(100) NOT NULL,
                capacity NUMBER(5) NOT NULL
            )
        """)
        
        # Student tábla (külső kulcs University-re)
        self.cursor.execute("""
            CREATE TABLE students (
                student_id NUMBER(10) PRIMARY KEY,
                university_id VARCHAR2(5) NOT NULL,
                first_name VARCHAR2(100) NOT NULL,
                last_name VARCHAR2(100) NOT NULL,
                email VARCHAR2(200) UNIQUE NOT NULL,
                birth_date DATE NOT NULL,
                enrollment_year NUMBER(4) NOT NULL,
                gpa NUMBER(3,2) NOT NULL,
                major VARCHAR2(100) NOT NULL,
                CONSTRAINT fk_student_university
                    FOREIGN KEY (university_id)
                    REFERENCES universities(university_id)
                    ON DELETE CASCADE
            )
        """)
        
        # Enrollment kapcsolótábla (N:M kapcsolat)
        self.cursor.execute("""
            CREATE TABLE enrollments (
                enrollment_id NUMBER(10) PRIMARY KEY,
                student_id NUMBER(10) NOT NULL,
                course_id NUMBER(10) NOT NULL,
                enrollment_date DATE NOT NULL,
                grade VARCHAR2(5),
                CONSTRAINT fk_enrollment_student
                    FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE,
                CONSTRAINT fk_enrollment_course
                    FOREIGN KEY (course_id)
                    REFERENCES courses(course_id)
                    ON DELETE CASCADE,
                CONSTRAINT unique_enrollment
                    UNIQUE (student_id, course_id)
            )
        """)
        
        self.connection.commit()
        print("Táblák sikeresen létrehozva!")
    
    def drop_tables(self):
        """Táblák törlése (tiszta újrakezdéshez)"""
        tables = ['enrollments', 'students', 'courses', 'universities']
        for table in tables:
            try:
                self.cursor.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
            except cx_Oracle.DatabaseError:
                pass  # Tábla nem létezik
        self.connection.commit()
    
    def insert_universities(self, universities: List[Any]):
        """Egyetemek beszúrása"""
        for uni in universities:
            self.cursor.execute("""
                INSERT INTO universities VALUES 
                (:1, :2, :3, :4, :5, :6, :7)
            """, (uni.university_id, uni.name, uni.city, uni.country,
                  uni.founded_year, uni.ranking, uni.website))
        self.connection.commit()
    
    def insert_courses(self, courses: List[Any]):
        """Kurzusok beszúrása"""
        for course in courses:
            self.cursor.execute("""
                INSERT INTO courses VALUES 
                (:1, :2, :3, :4, :5, :6, :7)
            """, (course.course_id, course.course_code, course.course_name,
                  course.credits, course.semester, course.instructor,
                  course.capacity))
        self.connection.commit()
    
    def insert_students(self, students: List[Any]):
        """Hallgatók beszúrása"""
        for student in students:
            self.cursor.execute("""
                INSERT INTO students VALUES 
                (:1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'), :7, :8, :9)
            """, (student.student_id, student.university_id, 
                  student.first_name, student.last_name, student.email,
                  student.birth_date, student.enrollment_year, 
                  student.gpa, student.major))
        self.connection.commit()
    
    def insert_enrollments(self, enrollments: List[Any]):
        """Beiratkozások beszúrása"""
        for enr in enrollments:
            self.cursor.execute("""
                INSERT INTO enrollments VALUES 
                (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), :5)
            """, (enr.enrollment_id, enr.student_id, enr.course_id,
                  enr.enrollment_date, enr.grade))
        self.connection.commit()
    
    def close(self):
        """Kapcsolat lezárása"""
        self.cursor.close()
        self.connection.close()
