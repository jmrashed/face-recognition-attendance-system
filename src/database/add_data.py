import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceauthentication-18484-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref = db.reference('Students')

data = {
    "104":
        {
            "name": "Alamin Rony",
            "major": "Senior Web Developer",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-04-09 00:54:34"
        },
    "105":
        {
            "name": "Saiful",
            "major": "Frontend Developer",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2023-04-09 00:54:34"
        },
    "106":
        {
            "name": "Rashed",
            "major": "Tech Lead Officer",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-04-09 00:54:34"
        },
    "107":
        {
            "name": "Jewel",
            "major": "Call center Agent",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-04-09 00:54:34"
        },
    "108":
        {
            "name": "Abrar",
            "major": "Customer Support",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-04-09 00:54:34"
        },
    "109":
        {
            "name": "Faysal C",
            "major": "Flutter App developer",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-04-09 00:54:34"
        },
    "110":
        {
            "name": "Imran",
            "major": "Laravel Developer",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-04-09 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)