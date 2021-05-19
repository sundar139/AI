import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import *
import tkinter.messagebox
import speech_recognition as sr
from gtts import gTTS

root = Tk()
root.geometry(newGeometry="772x621+0+0")
root.config(bg="#3390dc")
root.title('Attendance')
MainFrame=Frame(root,bg="MediumPurple4")
MainFrame.grid()
TitFrame=Frame(MainFrame,bd=1,padx=54,pady=8,bg="DodgerBlue2",relief=RIDGE)
TitFrame.pack(side=TOP)
lblTit=Label(TitFrame,font=('Trebuchet MS',38,'bold'),text="Attendance Cam",bg="DodgerBlue2",fg="SeaGreen3")
lblTit.grid()
bg = PhotoImage(file=r'C:/Users/Rohith Sundar/PycharmProjects/AI/AM.png')
background = Label(MainFrame, image=bg)
background.pack(side=TOP)
ButtonFrame=Frame(MainFrame,bd=1,width=800,height=200,padx=18,pady=10,bg="DodgerBlue2",relief=RIDGE)
ButtonFrame.pack(side=BOTTOM)

def iExit():
    iExit=tkinter.messagebox.askyesno("Attendance Cam","Confirm if you want to exit")
    if iExit>0:
        root.destroy()
        return

def voiceMessage():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        tkinter.messagebox.showinfo("Confirmation", "Say Something")
        print('Say something: ')
        audio = r.listen(source)
        voice_data = r.recognize_google(audio)
        print(voice_data)
        

    if voice_data == 'attendance' or 'Attendance':
        takeAttendance()
    else :
        iExit()

path = r'C:/Users/Rohith Sundar/PycharmProjects/AI/Project/Pics'
images = []
classNames = []
myList = os.listdir(path)
#print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
#print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open(r'C:/Users/Rohith Sundar/PycharmProjects/AI/Project/Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

encodeListKnown = findEncodings(images)
print('Encoding Complete')

def takeAttendance():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if faceDis[matchIndex] < 0.50:
                name = classNames[matchIndex].upper()
                markAttendance(name)
            else:
                name = 'Unknown'
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

btnAttendance=Button(ButtonFrame,text="Take Attendance",font=('Comic Sans MS',18,'normal'),height=1,width=20,bd=4,bg="#CC313D",fg="#F7C5CC",command=takeAttendance)
btnAttendance.grid(row=0,column=3)
btnVoice=Button(ButtonFrame,text="V",font=('Comic Sans MS',18,'normal'),height=1,width=3,bd=4,bg="#CC313D",fg="#F7C5CC",command=voiceMessage)
btnVoice.grid(row=0,column=5)
btnExit=Button(ButtonFrame,text="Exit",font=('Comic Sans MS',18,'normal'),height=1,width=10,bd=4,bg="#CC313D",fg="#F7C5CC",command=iExit)
btnExit.grid(row=1,column=3)

root.mainloop()