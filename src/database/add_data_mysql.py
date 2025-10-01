import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.mysql_config import create_database_and_tables, get_connection
from mysql.connector import Error

# Create database and tables first
create_database_and_tables()

# Student data
data = {
    "104": {
        "name": "Alamin Rony",
        "major": "Senior Web Developer",
        "starting_year": 2017,
        "total_attendance": 7,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2023-04-09 00:54:34"
    },
    "105": {
        "name": "Saiful",
        "major": "Frontend Developer",
        "starting_year": 2021,
        "total_attendance": 12,
        "standing": "B",
        "year": 1,
        "last_attendance_time": "2023-04-09 00:54:34"
    },
    "106": {
        "name": "Rashed",
        "major": "Tech Lead Officer",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2023-04-09 00:54:34"
    },
    "107": {
        "name": "Jewel",
        "major": "Call center Agent",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2023-04-09 00:54:34"
    },
    "108": {
        "name": "Abrar",
        "major": "Customer Support",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2023-04-09 00:54:34"
    },
    "109": {
        "name": "Faysal C",
        "major": "Flutter App developer",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2023-04-09 00:54:34"
    },
    "110": {
        "name": "Imran",
        "major": "Laravel Developer",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2023-04-09 00:54:34"
    }
}

# Insert data into MySQL
try:
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO students (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        major = VALUES(major),
        starting_year = VALUES(starting_year),
        total_attendance = VALUES(total_attendance),
        standing = VALUES(standing),
        year = VALUES(year),
        last_attendance_time = VALUES(last_attendance_time)
        """
        
        for student_id, info in data.items():
            values = (
                student_id,
                info['name'],
                info['major'],
                info['starting_year'],
                info['total_attendance'],
                info['standing'],
                info['year'],
                info['last_attendance_time']
            )
            cursor.execute(insert_query, values)
        
        connection.commit()
        print(f"✅ Successfully inserted {len(data)} student records into MySQL database")
        
        cursor.close()
        connection.close()
        
except Error as e:
    print(f"❌ Error inserting data: {e}")