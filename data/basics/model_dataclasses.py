from dataclasses import dataclass
from typing import List, Dict, Any
from faker import Faker
import random
import string

@dataclass
class University:
    university_id: str
    name: str
    city: str
    country: str
    founded_year: int
    ranking: int
    website: str
    
    @staticmethod
    def get_fields() -> List[str]:
        return ['university_id', 'name', 'city', 'country', 
                'founded_year', 'ranking', 'website']
    
    @staticmethod
    def generate(count: int, 
                 min_ranking: int = 1, 
                 max_ranking: int = 500,
                 countries: List[str] = None) -> List['University']:

        fake = Faker(['hu_HU', 'en_US', 'de_DE'])
        universities = []
        
        if countries is None:
            countries = ['Hungary', 'Germany', 'Austria', 
                        'United Kingdom', 'United States', 
                        'France', 'Netherlands', 'Sweden']
        
        university_types = ['University', 'Institute of Technology', 
                           'College', 'Academy', 'Polytechnic']
        
        for i in range(count):
            country = random.choice(countries)
            city = fake.city()
            uni_type = random.choice(university_types)
            name = f"{city} {uni_type}"
            
            # Random egyetemi kódgenerálás
            university_id = ''.join(random.choices(string.ascii_letters + string.digits, k=5)).upper()
            
            universities.append(University(
                university_id=university_id,
                name=name,
                city=city,
                country=country,
                founded_year=random.randint(1088, 2020),
                ranking=random.randint(min_ranking, max_ranking),
                website=f"https://www.{name.lower().replace(' ', '')}.edu"
            ))
        
        return universities
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'university_id': self.university_id,
            'name': self.name,
            'city': self.city,
            'country': self.country,
            'founded_year': self.founded_year,
            'ranking': self.ranking,
            'website': self.website
        }
    
@dataclass
class Student:
    student_id: int
    university_id: str  # Külső kulcs
    first_name: str
    last_name: str
    email: str
    birth_date: str
    enrollment_year: int
    gpa: float
    major: str
    
    @staticmethod
    def get_fields() -> List[str]:
        return ['student_id', 'university_id', 'first_name', 'last_name',
                'email', 'birth_date', 'enrollment_year', 'gpa', 'major']
    
    @staticmethod
    def generate(count: int,
                 university_ids: List[str],
                 min_gpa: float = 2.0,
                 max_gpa: float = 4.0,
                 majors: List[str] = None) -> List['Student']:
        fake = Faker('hu_HU')
        students = []
        
        if majors is None:
            majors = ['Computer Science', 'Business Administration', 
                     'Engineering', 'Medicine', 'Law', 'Psychology',
                     'Economics', 'Mathematics', 'Physics', 'Biology']
        
        for i in range(count):
            # Születési dátum generálása (18-25 éves hallgatók)
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=25)
            enrollment_year = random.randint(2019, 2024)

            student_id = i + 1   

            # Email az egyetem ID alapján formázva
            uni_id = random.choice(university_ids)
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}.{uni_id}@uni{student_id}.edu"
            
            students.append(Student(
                student_id,
                university_id=uni_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                birth_date=birth_date.strftime('%Y-%m-%d'),
                enrollment_year=enrollment_year,
                gpa=round(random.uniform(min_gpa, max_gpa), 2),
                major=random.choice(majors)
            ))
        
        return students
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'student_id': self.student_id,
            'university_id': self.university_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'birth_date': self.birth_date,
            'enrollment_year': self.enrollment_year,
            'gpa': self.gpa,
            'major': self.major
        }
    
@dataclass
class Course:
    course_id: int
    course_code: str
    course_name: str
    credits: int
    semester: str
    instructor: str
    capacity: int
    
    @staticmethod
    def get_fields() -> List[str]:
        return ['course_id', 'course_code', 'course_name', 'credits',
                'semester', 'instructor', 'capacity']
    
    @staticmethod
    def generate(count: int,
                 min_credits: int = 2,
                 max_credits: int = 6,
                 semesters: List[str] = None) -> List['Course']:

        fake = Faker('en_US')
        courses = []
        
        if semesters is None:
            semesters = ['Fall 2024', 'Spring 2025', 'Fall 2025']
        
        course_subjects = ['Introduction to', 'Advanced', 'Applied',
                          'Fundamentals of', 'Theory of', 'Practical']
        course_topics = ['Programming', 'Data Structures', 'Algorithms',
                        'Database Systems', 'Machine Learning', 'Networking',
                        'Software Engineering', 'Operating Systems',
                        'Computer Architecture', 'Artificial Intelligence']
        
        for i in range(count):
            subject = random.choice(course_subjects)
            topic = random.choice(course_topics)
            course_name = f"{subject} {topic}"
            
            # Kurzus kód formátum: CS101, MATH201, stb.
            dept_code = ''.join([c for c in topic.upper() if c.isalpha()])[:4]
            course_code = f"{dept_code}{random.randint(100, 499)}"
            
            courses.append(Course(
                course_id=i + 1,
                course_code=course_code,
                course_name=course_name,
                credits=random.randint(min_credits, max_credits),
                semester=random.choice(semesters),
                instructor=fake.name(),
                capacity=random.randint(20, 150)
            ))
        
        return courses
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'course_id': self.course_id,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'credits': self.credits,
            'semester': self.semester,
            'instructor': self.instructor,
            'capacity': self.capacity
        }
    
@dataclass
class Enrollment:
    enrollment_id: int
    student_id: int
    course_id: int
    enrollment_date: str
    grade: str
    
    @staticmethod
    def get_fields() -> List[str]:
        return ['enrollment_id', 'student_id', 'course_id', 
                'enrollment_date', 'grade']
    
    @staticmethod
    def generate(student_ids: List[int], 
                 course_ids: List[int],
                 enrollments_per_student: tuple = (3, 8)) -> List['Enrollment']:

        from faker import Faker
        fake = Faker()
        enrollments = []
        grades = ['1', '2', '3', '4', '5']
        
        enrollment_id = 1
        for student_id in student_ids:
            num_courses = random.randint(*enrollments_per_student)
            selected_courses = random.sample(course_ids, 
                                            min(num_courses, len(course_ids)))
            
            for course_id in selected_courses:
                enrollments.append(Enrollment(
                    enrollment_id=enrollment_id,
                    student_id=student_id,
                    course_id=course_id,
                    enrollment_date=fake.date_between(
                        start_date='-1y', end_date='today'
                    ).strftime('%Y-%m-%d'),
                    grade=random.choice(grades)
                ))
                enrollment_id += 1
        
        return enrollments
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'enrollment_id': self.enrollment_id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': self.enrollment_date,
            'grade': self.grade
        }