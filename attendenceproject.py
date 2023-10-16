import tkinter
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import Text, Scrollbar
import tkinter as tk
from tkinter import ttk
from tkinter import font
from threading import Thread
from tkinter import PhotoImage
import pygame
from skimage import io
# Initialize pygame.mixer and load the sound
pygame.mixer.init()
sound = pygame.mixer.Sound("C:\\Users\\shaur\\PycharmProjects\\pythonProject2\\1697374090775v7ww4i99-voicemaker.in-speech.mp3")

# Function to play the sound
def play_sound():
    sound.play()

path='C:\\Users\\shaur\\PycharmProjects\\pythonProject2\\ImagesBasic'
images=[]
classNames=[]
myList=os.listdir(path)

for cl in myList:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList=[]
    for img in images:
        img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('attendenc.csv.py','r+') as f:
        myDataList=f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now=datetime.now()
            dtString=now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

    print(myDataList)

def open_attendance_data():
    with open('attendenc.csv.py', 'r') as f:
        data = f.read()
        print(data)

    data_window = tk.Tk()
    data_window.title("Attendance Data")
    data_window.geometry("450x750")
    data_window.configure(bg="black")

    text_widget = Text(data_window, wrap="none", bg="black", fg="green", font=("Courier New", 12))
    text_widget.pack(fill="both", expand=True)

        # Insert the formatted header
    text_widget.insert("1.0", "Name\t\tTime\n")
    text_widget.insert("2.0", "-" * 30 + "\n")

        # Split and format the data
    entries = data.strip().split('\n')
    for entry in entries:
        if ',' in entry:  # Check if there is a comma in the entry
            name, time = entry.split(',')  # Split based on the comma delimiter
            text_widget.insert(tk.END, f"{name.strip()}\t\t{time}\n")


    text_widget.config(state="disabled")

    data_window.mainloop()


def face_recognition_function():
    encodeListKnown=findEncodings(images)
    print('Encoding Complete')

    cap=cv2.VideoCapture(0)

    while True:
        success, img= cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame=face_recognition.face_locations(imgS)
        encodesCurFrame=face_recognition.face_encodings(imgS,facesCurFrame)


        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            print(faceDis)
            matchIndex=np.argmin(faceDis)

            if matches[matchIndex]:
                name=classNames[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1= y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),1)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_ITALIC,1,(255,255,255),2)
                markAttendance(name)
        cv2.imshow('webcam',img)
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

    cap.release()
    cv2.destroyAllWindows()



def display_help():
    help_text = """
       Welcome to the Face Recognition App Help Guide:

    1. Click the "Start Face Recognition" button to initiate the face recognition process.
    2. The webcam will open, and the app will attempt to recognize faces.
    3. Detected faces will be highlighted with a green rectangle, and the name will be displayed.
    4. The app will automatically mark the attendance for recognized individuals.
    5. Click the "Open Attendance Data" button to view attendance records.
    6. Click the "About" button to learn more about the app and its developer.
    7. To exit the app, click the "Exit Program" button.

    Please ensure the webcam is connected and functional for the best experience.

    If you encounter any issues or have questions, feel free to contact the developer.

    Developed by Dhairya Sarswat
    Version 1.0
    """
    display_info("Help", help_text)

def display_about():
    about_text = """
  Face Recognition App
    Developed by Dhairya Sarswat

    Version: 1.0

    Developer:
    - Name: Dhairya Sarswat
    - Education: Pursuing B.Tech in Computer Science and Engineering
    - University: Dr. A.P.J. Abdul Kalam Technical University (AKTU)
    - College: Moradabad Institute of Technology

    Thank you for using the Face Recognition App. For any questions or feedback, please feel free to contact the developer.
    """
    display_info("About", about_text)


def display_contact_us():
    contact_us_text = """
    For any questions, feedback, or inquiries, please feel free to contact us at the following email address:

    Email: dhairyasarswatwork2005@gmail.com

    We value your input and are here to assist you.
    """
    display_info("Contact Us", contact_us_text)

def display_info(title, info_text):
    info_window = tk.Tk()
    info_window.title(title)
    info_window.geometry("850x400")
    info_window.configure(bg="light green")

    text_widget = Text(info_window, wrap="word", bg="black", fg="green", font=("Courier New", 12))
    text_widget.pack(fill="both", expand=True)

    text_widget.insert("1.0", info_text)
    text_widget.config(state="disabled")

    info_window.mainloop()




def start_face_recognition():
    recognition_thread = Thread(target=face_recognition_function)
    recognition_thread.start()

import tkinter as tk

button_style = {
    "font": ("Courier New", 12),
    "bg": "black",
    "fg": "light green",
    "width": 22,
    "height": 1,
    "borderwidth": 6,
    "relief": "raised",
    "compound": "center",

}
label_style = {
    "font": ("Courier New", 15),
    "bg": "black",
    "fg": "light green",
    "width": 39,
    "height": 1,
    "borderwidth": 6,
    "relief": "raised",
    "compound": "center",


}

label_made_by_style = {
    "font": ("Courier New", 15),
    "bg": "black",
    "fg": "light green",
    "width": 30,
    "height": 1,
    "borderwidth": 6,
    "relief": "raised",
    "compound": "center",

}





window = tk.Tk()
window.title("Face Recognition")
window.configure(bg="light green")
window.geometry("900x900")



image_path=PhotoImage(file="C:\\Users\\shaur\\Downloads\\schtgJ.png")
bg_image=tkinter.Label(window,image=image_path)
bg_image.place(relheight=1,relwidth=1)


button_frame = tk.Frame(window, bg="light green")
button_frame.pack(pady=20)

label = tk.Label(window, text="Advance Face Recognition System", **label_style)
label.pack(side="bottom", pady=20)
label.bind("<Button-1>", lambda event: play_sound())



label_made_by = tk.Label(window, text="Made By: Dhairya Sarswat",**label_made_by_style)
label_made_by.pack(side="bottom", pady=20)
start_button = tk.Button(button_frame, text="Start Face Recognition", command=start_face_recognition, **button_style)
start_button.pack(side="left", padx=10)

open_data_button = tk.Button(button_frame, text="Open Attendance Data", command=open_attendance_data, **button_style)
open_data_button.pack(side="left", padx=10)

help_button = tk.Button(button_frame, text="Help", command=display_help, **button_style)
help_button.pack(side="left", padx=10)

about_button = tk.Button(button_frame, text="About", command=display_about, **button_style)
about_button.pack(side="left", padx=10)

contact_us_button = tk.Button(button_frame, text="Contact Us", command=display_contact_us, **button_style)
contact_us_button.pack(side="left", padx=10)




def close_window():
    window.destroy()




exit_button = tk.Button(button_frame, text="Exit Program", command=close_window, **button_style)
exit_button.pack(side="left", padx=10)





window.mainloop()



