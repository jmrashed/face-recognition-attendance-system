import mysql.connector
from mysql.connector import Error

# MySQL configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'database': 'face-recognition',
    'user': 'root',
    'password': ''
}

def create_database_and_tables():
    """Create database and required tables"""
    try:
        # Connect without database first
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS `face-recognition`")
        print("✅ Database 'face-recognition' created successfully")
        
        # Use the database
        cursor.execute("USE `face-recognition`")
        
        # Create students table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            major VARCHAR(100) NOT NULL,
            starting_year INT NOT NULL,
            total_attendance INT DEFAULT 0,
            standing VARCHAR(5) DEFAULT 'G',
            year INT NOT NULL,
            last_attendance_time DATETIME DEFAULT NULL
        )
        """
        cursor.execute(create_table_query)
        print("✅ Students table created successfully")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error: {e}")

def get_connection():
    """Get MySQL connection"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        return connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None