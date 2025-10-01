# MySQL Setup Guide

## Configuration
- **Database**: face-recognition
- **User**: root
- **Password**: (empty)
- **Host**: localhost

## Files Created
- `mysql_config.py` - MySQL configuration and connection functions
- `AddDatatoDatabase_MySQL.py` - MySQL version of database initialization
- `Main_MySQL.py` - MySQL version of the main application
- `test_mysql_connection.py` - Test MySQL connection

## Usage

### 1. Setup Database
```bash
python AddDatatoDatabase_MySQL.py
```

### 2. Test Connection
```bash
python test_mysql_connection.py
```

### 3. Run Application
```bash
python Main_MySQL.py
```

## Database Schema
```sql
CREATE TABLE students (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(100) NOT NULL,
    starting_year INT NOT NULL,
    total_attendance INT DEFAULT 0,
    standing VARCHAR(5) DEFAULT 'G',
    year INT NOT NULL,
    last_attendance_time DATETIME DEFAULT NULL
);
```

## Key Changes from Firebase
- Local MySQL database instead of Firebase Realtime Database
- Student images loaded from local `Images/` folder
- No cloud storage dependency
- Faster local database queries