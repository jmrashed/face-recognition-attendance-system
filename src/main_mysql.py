import os
import pickle
import cv2
import face_recognition
import cvzone
import numpy as np
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config.mysql_config import get_connection
from mysql.connector import Error

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('../assets/resources/background.png')

# Importing the mode images into a list
folderModePath = '../assets/resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load the encoding file
print("Loading Encode File ...")
file = open('database/EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

def get_student_info(student_id):
    """Get student information from MySQL database"""
    try:
        connection = get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM students WHERE id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result
    except Error as e:
        print(f"Error fetching student info: {e}")
    return None

def update_attendance(student_id):
    """Update student attendance in MySQL database"""
    try:
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            
            # Update attendance count and last attendance time
            update_query = """
            UPDATE students 
            SET total_attendance = total_attendance + 1, 
                last_attendance_time = %s 
            WHERE id = %s
            """
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(update_query, (current_time, student_id))
            connection.commit()
            
            cursor.close()
            connection.close()
            return True
    except Error as e:
        print(f"Error updating attendance: {e}")
    return False

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    if img is None:
        print("Image file not found or cannot be loaded")
        continue
    
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Get student data from MySQL
                studentInfo = get_student_info(id)
                print(studentInfo)
                
                # Load student image from local Images folder
                img_path = f'../assets/images/{id}.png'
                if os.path.exists(img_path):
                    imgStudent = cv2.imread(img_path)
                else:
                    print(f"Student image not found: {img_path}")
                    imgStudent = np.zeros((216, 216, 3), dtype=np.uint8)
                
                if studentInfo:
                    # Check if enough time has passed since last attendance
                    if studentInfo['last_attendance_time']:
                        datetimeObject = datetime.strptime(str(studentInfo['last_attendance_time']), "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    else:
                        secondsElapsed = 999  # First time attendance
                    
                    print(f"Seconds elapsed: {secondsElapsed}")
                    
                    if secondsElapsed > 30:
                        if update_attendance(id):
                            studentInfo['total_attendance'] += 1
                            studentInfo['last_attendance_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3 and studentInfo:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    if imgStudent is not None and imgStudent.size > 0:
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()