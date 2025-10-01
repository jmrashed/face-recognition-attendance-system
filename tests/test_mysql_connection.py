import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.mysql_config import get_connection
from mysql.connector import Error

def test_connection():
    """Test MySQL connection and display student data"""
    try:
        connection = get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Test query
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            
            print("✅ MySQL Connection Successful!")
            print(f"📊 Total students in database: {len(students)}")
            print("\n📋 Student Records:")
            print("-" * 80)
            
            for student in students:
                print(f"ID: {student['id']} | Name: {student['name']} | Major: {student['major']} | Attendance: {student['total_attendance']}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ MySQL Connection Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()