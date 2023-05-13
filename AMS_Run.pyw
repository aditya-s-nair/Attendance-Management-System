import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time
from tkinter import messagebox

# -------------------------------------------------------------------------------------------------------
# Window is our Main frame of system

window = tk.Tk()
window.title("FAMS-Face Recognition Based Attendance Management System")

window.geometry('1280x720')
window.configure(background='#071E3D')

# -------------------------------------------------------------------------------------------------------
# for clearing the text in the entry boxes on the window

def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)

# -------------------------------------------------------------------------------------------------------
# For take images for datasets

def take_img(): # one of the main fuctions of our project

    ''' This function runs whenever we click on the take images button
        1. takes about 200 images of the user
        2. also stores the date and time
        3. links the date and time with the images 
        4. creates an exel file which holds all the data
    '''
    root = Tk()
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        messagebox.showerror("Incomplete details", "Enrollment number field was left empty.")
    elif l2 == '':
        messagebox.showerror("Incomplete details", "Name field was left empty.")
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = img[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img) 
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)
# -------------------------------------------------------------------------------------------------------
# for choose subject and fill attendance

def subjectchoose():

    ''' This function runs whenever we click on the take images button
        1. fills the attendence corresponding to the subject
        2. also stores the date and time
        3. helps to create seperate attendence sheets for all the subjects
        4. creates an exel file which holds all the data
    '''
    def Fillattendances():
        sub=tx.get()
        now = time.time()  ###For calculate seconds of video
        future = now + 20
        if time.time() < future:
            if sub == '':
                messagebox.showerror("Incomplete details", "The Subject Name field was left empty")
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                try:
                    recognizer.read("TrainingImageLabel\Trainner.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notifica.configure(text=e, bg="#071E3D", fg="white", width=33, font=('times', 15, 'bold'))
                    Notifica.place(x=20, y=250)

                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv("StudentDetails\StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name', 'Date', 'Time']
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if (conf <70):
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            tt = str(Id) + "-" + aa
                            En = '15624031' + str(Id)
                            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            Id = 'Unknown'
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)               

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='#071E3D')
                cs = fileName
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=8, height=1, fg="white", font=('times', 15, ' bold '),
                                                  bg="#l071E3D", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)

    ###windo is frame for subject chooser
    windo = tk.Tk()
    windo.iconbitmap('AMS.ico')
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='#071E3D')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                            height=2, font=('times', 15, 'bold'))

    sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg="white", bg="#278EA5", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="#B3C0CC", fg="black", font=('times', 23, ' bold '))
    tx.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="white",command=Fillattendances, bg="#21E6C1", width=20, height=2,
                       activebackground="#1F4287", font=('times', 15, ' bold '))
    fill_a.place(x=250, y=160)
    windo.mainloop()

# -------------------------------------------------------------------------------------------------------
# For train the model

def trainimg():
    
    ''' This function runs whenever we click on the train images button
        1. trains the model for face recognition
        2. creats a trainingimage label folder and stores the images
        3. the created label helps in recognizing the face of the student
    '''
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces,Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l='please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel\Trainner.yml")
    except Exception as e:
        q='Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
# window.iconbitmap('AMS.ico')

def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

# -------------------------------------------------------------------------------------------------------
# main window using tkinter

window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text=" VIT Student Face Attendance Tracker", bg="#278EA5", fg="white", height=2, width=60, font=('times', 30, 'bold'))
message2 = tk.Label(window, text='''VIT BHOPAL UNIVERSITY''', bg="#278EA5", fg="white", width=100, font=('times', 20, 'bold'), height=2, justify="center")

vit_image = Image.open("vit-bhopal-logo.png").resize((150,100), Image.ANTIALIAS)
vit_image = ImageTk.PhotoImage(vit_image)
image_label = Label(image=vit_image)
image_label.image = vit_image
image_label.place(x=50,y=30)

message.place(x=-50,y=0)
message2.place(x=-150, y=90)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                      height=3, font=('times', 17, 'bold'))

lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="white", bg="#278EA5", font=('times', 15, ' bold '))
lbl.place(x=200, y=240)

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

txt = tk.Entry(window, validate="key", width=25, bg="#B3C0CC", fg="black",  font=('times', 25, ' bold '))
txt['validatecommand'] = (txt.register(testVal),'%P','%d')
txt.place(x=480, y=250)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="white", bg="#278EA5", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=340)

txt2 = tk.Entry(window, width=25, bg="#B3C0CC", fg="black", font=('times', 25))
txt2.place(x=480, y=350)

clearButton = tk.Button(window, text="Clear",command=clear,fg="white"  ,bg="#21E6C1"  ,width=10  ,height=1 ,activebackground = "#1F4287" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=250)

clearButton1 = tk.Button(window, text="Clear",command=clear1,fg="white"  ,bg="#21E6C1"  ,width=10 ,height=1, activebackground = "#1F4287" ,font=('times', 15, ' bold '))
clearButton1.place(x=950, y=350)


takeImg = tk.Button(window, text="Take Images",command=take_img,fg="white"  ,bg="#1F4287"  ,width=20  ,height=3, activebackground = "#21E6C1" ,font=('times', 15, ' bold '))
takeImg.place(x=90, y=500)

trainImg = tk.Button(window, text="Train Images",fg="white",command=trainimg ,bg="#1F4287"  ,width=20  ,height=3, activebackground = "#21E6C1" ,font=('times', 15, ' bold '))
trainImg.place(x=490, y=500)

FA = tk.Button(window, text="Automatic Attendace",fg="white", command=subjectchoose ,bg="#1F4287"  ,width=20  ,height=3, activebackground = "#21E6C1" ,font=('times', 15, ' bold '))
FA.place(x=890, y=500)


window.mainloop()