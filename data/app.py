import os
import sys
from pathlib import Path

# Add parent directory to sys.path BEFORE imports
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from data.basics.model_dataclasses import University, Student, Course, Enrollment
from data.basics.handler import CSVHandler, JSONHandler, XLSXHandler
from data.basics.handler.oracle_handler import OracleHandler
from data.extra.analytics import DataAnalytics

def main():    
    # 1. Adatok generálása Faker-rel
    print("\n1. Adatok generálása...")
    
    universities = University.generate(
        count=10,
        min_ranking=1,
        max_ranking=500,
        countries=['Hungary', 'Germany', 'Austria', 'United Kingdom', 'USA', 'Canada']
    )
    print(f"    {len(universities)} egyetem generálva")
    
    courses = Course.generate(
        count=30,
        min_credits=2,
        max_credits=6,
        semesters=['Fall 2024', 'Spring 2025']
    )
    print(f"    {len(courses)} kurzus generálva")
    
    university_ids = [u.university_id for u in universities]
    students = Student.generate(
        count=200,
        university_ids=university_ids,
        min_gpa=2.0,
        max_gpa=4.0
    )
    print(f"    {len(students)} hallgató generálva")
    
    student_ids = [s.student_id for s in students]
    course_ids = [c.course_id for c in courses]
    enrollments = Enrollment.generate(
        student_ids=student_ids,
        course_ids=course_ids,
        enrollments_per_student=(3, 8)
    )
    print(f"    {len(enrollments)} beiratkozás generálva")
    
    # 2. CSV formátum
    print("\n2. CSV fájlok írása...")
    os.makedirs('output/csv', exist_ok=True)
    
    CSVHandler.write(universities, 'output/csv/universities.csv', 
                     University.get_fields())
    CSVHandler.write(students, 'output/csv/students.csv', 
                     Student.get_fields())
    CSVHandler.write(courses, 'output/csv/courses.csv', 
                     Course.get_fields())
    CSVHandler.write(enrollments, 'output/csv/enrollments.csv', 
                     Enrollment.get_fields())
    print("    CSV fájlok létrehozva")
    
    # 3. JSON formátum
    print("\n3. JSON fájlok írása...")
    os.makedirs('output/json', exist_ok=True)
    
    JSONHandler.write(universities, 'output/json/universities.json')
    JSONHandler.write(students, 'output/json/students.json')
    JSONHandler.write(courses, 'output/json/courses.json')
    JSONHandler.write(enrollments, 'output/json/enrollments.json')
    print("    JSON fájlok létrehozva")
    
    # 4. XLSX formátum
    print("\n4. XLSX fájl írása...")
    os.makedirs('output/xlsx', exist_ok=True)
    
    XLSXHandler.write({
        'Universities': (universities, University.get_fields()),
        'Students': (students, Student.get_fields()),
        'Courses': (courses, Course.get_fields()),
        'Enrollments': (enrollments, Enrollment.get_fields())
    }, 'output/xlsx/data.xlsx')
    print("    XLSX fájl létrehozva")
    
    # 5. Oracle adatbázis
    print("\n5. Oracle adatbázis műveletek...")
    
    try:
        oracle = OracleHandler(
            username='U_YRHEOD',
            password='Kulazabalo0101',
            dsn='codd.inf.unideb.hu:1521/ora21cp.inf.unideb.hu'
        )
        
        
        oracle.drop_tables()
        

        oracle.create_tables()
        
        # Adatok beszúrása
        print("   Adatok feltöltése...")
        oracle.insert_universities(universities)
        oracle.insert_courses(courses)
        oracle.insert_students(students)
        oracle.insert_enrollments(enrollments)

        
        oracle.close()
        
    except Exception as e:
        print(f"   Oracle hiba: {e}")
        print("   (Folytatás Oracle nélkül...)")
    
    # 6. EXTRA: Adatelemzés és vizualizáció
    print("\n6. EXTRA: Adatelemzési jelentés generálása...")
    
    analytics = DataAnalytics(students, universities, courses, enrollments)
    analytics.generate_analytics_report('output/analytics_report.xlsx')

    
    # 7. Visszaolvasás tesztelése
    print("\n7. Fájlok visszaolvasásának tesztelése...")
    
    # CSV olvasás
    read_universities = CSVHandler.read('output/csv/universities.csv', 
                                        University)
    print(f"    CSV: {len(read_universities)} egyetem visszaolvasva")
    
    # JSON olvasás
    read_students = JSONHandler.read('output/json/students.json', Student)
    print(f"    JSON: {len(read_students)} hallgató visszaolvasva")
    
    # XLSX olvasás
    read_data = XLSXHandler.read(
        'output/xlsx/data.xlsx',
        ['Universities', 'Students', 'Courses', 'Enrollments'],
        {
            'Universities': University,
            'Students': Student,
            'Courses': Course,
            'Enrollments': Enrollment
        }
    )
    print(f"    XLSX: {len(read_data['Universities'])} egyetem visszaolvasva")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()