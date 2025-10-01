#!/usr/bin/env python3
"""
Face Recognition Attendance System - Entry Point
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point"""
    print("Face Recognition Attendance System")
    print("1. Run with Firebase (original)")
    print("2. Run with MySQL (local)")
    print("3. Setup MySQL database")
    print("4. Test MySQL connection")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        os.system("python src/main.py")
    elif choice == "2":
        os.system("python src/main_mysql.py")
    elif choice == "3":
        os.system("python src/database/add_data_mysql.py")
    elif choice == "4":
        os.system("python tests/test_mysql_connection.py")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()