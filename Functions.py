from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
from PIL import ImageTk, Image, ImageDraw
import cv2 as cv
from face_recognition import *
import sqlite3 as db


def raise_page(page):
    page.tkraise()


def define_face_register(name_entry, page):
    # Check if the name is not empty field
    if name_entry.get() == "":
        messagebox.showerror("Error", "Please enter your name")
        return

    # Append face paths to list
    face_paths = []
    face_names = []

    # Check if the name already exists in the database
    conn = db.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    data_base = c.fetchall()
    for data in data_base:
        if name_entry.get() == data[0]:
            messagebox.showerror("Error", "Error, name already exists")
            return
        face_names.append(data[0])
        face_paths.append("DefinedFaces/" + data[0] + ".png")
    conn.commit()
    conn.close()
    # Encoding Faces
    encoding_faces = []
    for face_path in face_paths:
        face = cv.imread(face_path)
        encode = face_encodings(face)[0]
        encoding_faces.append(encode)

    state = 0
    cam = cv.VideoCapture(0)  # Webcam
    while True:
        ret, frame = cam.read()
        face_loc = face_locations(frame)  # Face Location
        if face_loc:
            y1, x2, y2, x1 = face_loc[0]
            font_size = 1.25 - (1 / (x2 - x1)) * 100
            if font_size < 0.60:
                font_size = 0.60
            current_face_encoding = face_encodings(frame)[0]
            face_cmp = compare_faces(encoding_faces, current_face_encoding, 0.55)
            face_dis = face_distance(encoding_faces, current_face_encoding)
            try:
                match_index = np.argmin(face_dis)
                if face_cmp[match_index]:
                    state = 0
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv.rectangle(frame, (x1 - 1, y1 - 30), (x2 + 1, y1), (0, 0, 255), cv.FILLED)
                    cv.putText(frame, str(face_names[match_index]).title(), (x1 + 6, y1 - 6), cv.FONT_HERSHEY_COMPLEX,
                               font_size, (255, 255, 255), 1)
                else:
                    state += 1
                    if state == 5:
                        cv.imwrite("DefinedFaces/" + name_entry.get() + ".png", frame)
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv.rectangle(frame, (x1 - 1, y1 - 30), (x2 + 1, y1), (0, 255, 0), cv.FILLED)
                    cv.putText(frame, str(name_entry.get()).title(), (x1 + 6, y1 - 6), cv.FONT_HERSHEY_COMPLEX,
                               font_size,
                               (255, 255, 255), 1)
            except ValueError:
                pass

        cv.imshow('Register', frame)
        if cv.waitKey(1) == 27 or state == 5:
            if not face_loc:
                state = 0
                messagebox.showerror("Error", "Couldn't find any faces")
                continue
            elif state == 5:
                messagebox.showinfo("Info", "Your face has been defined successfully")

            # Writing data to the database
            conn = db.connect("data.db")
            c = conn.cursor()
            c.execute("INSERT INTO addresses VALUES(:name)",
                      {
                          'name': name_entry.get()
                      }
                      )
            conn.commit()
            conn.close()
            break
    cam.release()
    cv.destroyAllWindows()

    name_entry.delete(0, END)
    raise_page(page)


def detecting_facial_features_start(values):
    facial_features = [
        'chin',
        'left_eye',
        'right_eye',
        'left_eyebrow',
        'right_eyebrow',
        'nose_bridge',
        'nose_tip',
        'top_lip',
        'bottom_lip']
    selected = []
    i = 0
    for val in values:
        if values[-1] == 1:
            selected.extend(facial_features)
            break
        elif val == 1:
            selected.append(facial_features[i])
        i += 1

    cam = cv.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        frame = cv.flip(frame, 1)
        face_landmarks_list = face_landmarks(frame)
        if face_landmarks_list:
            for face_landmark in face_landmarks_list:
                for facial_feature in selected:
                    x = []
                    y = []
                    for coordinate in face_landmark[facial_feature]:
                        x.append(coordinate[0])
                        y.append(coordinate[1])
                    x1 = min(x)
                    y1 = min(y)
                    x2 = max(x)
                    y2 = max(y)
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv.putText(frame, facial_feature, (x1 - 5, y1 - 5), cv.FONT_HERSHEY_COMPLEX, 0.3, (0, 0, 255), 1)
        cv.imshow("Detecting Facial Features", frame)
        key = cv.waitKey(1)
        if key == 27:
            break
    cam.release()
    cv.destroyAllWindows()


def recognizing_faces():
    face_paths = []
    face_names = []
    conn = db.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    data_base = c.fetchall()
    for data in data_base:
        face_names.append(data[0])
        face_paths.append("DefinedFaces/" + data[0] + ".png")
    conn.commit()
    conn.close()
    # Encoding Faces
    encoding_faces = []

    for face_path in face_paths:
        face = cv.imread(face_path)
        encode = face_encodings(face)[0]
        encoding_faces.append(encode)

    cam = cv.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        face_locs = face_locations(frame)  # Face Location
        current_face_encodings = face_encodings(frame)

        if current_face_encodings:
            for i in range(len(current_face_encodings)):
                y1, x2, y2, x1 = face_locs[i]
                font_size = 1.25 - (1 / (x2 - x1)) * 100
                if font_size < 0.60:
                    font_size = 0.60
                face_cmp = compare_faces(encoding_faces, current_face_encodings[i], 0.55)
                face_dis = face_distance(encoding_faces, current_face_encodings[i])
                match_index = np.argmin(face_dis)
                if face_cmp[match_index]:
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv.rectangle(frame, (x1 - 1, y1 - 30), (x2 + 1, y1), (0, 255, 0), cv.FILLED)
                    cv.putText(frame, str(face_names[match_index]).title(), (x1 + 6, y1 - 6),
                               cv.FONT_HERSHEY_COMPLEX, font_size, (255, 255, 255), 1)
                else:
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv.rectangle(frame, (x1 - 1, y1 - 30), (x2 + 1, y1), (0, 0, 255), cv.FILLED)
                    cv.putText(frame, "Unknown", (x1 + 6, y1 - 6), cv.FONT_HERSHEY_COMPLEX,
                               font_size, (255, 255, 255), 1)
        cv.imshow('Recognizing Faces', frame)
        if cv.waitKey(1) == 27:
            break
    cam.release()
    cv.destroyAllWindows()


def select_picture(page):
    filetypes = (
        ('PNG files', '*.png'),
        ('JPG files', '*.jpg'),
        ('JPEG files', '*.jpeg'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename != '':
        messagebox.showinfo(
            title='Selected File',
            message=filename
        )
    else:
        messagebox.showerror(
            title='Error',
            message='You did not select an image'
        )
        return
    image = load_image_file(filename)

    facial_features = [
        'chin',
        'left_eyebrow',
        'right_eyebrow',
        'nose_bridge',
        'nose_tip',
        'left_eye',
        'right_eye',
        'top_lip',
        'bottom_lip']

    face_landmarks_list = face_landmarks(image)
    img_obj = Image.fromarray(image)

    for face_landmark in face_landmarks_list:
        drawing = ImageDraw.Draw(img_obj)
        for facial_feature in facial_features:
            if facial_feature == 'top_lip' or facial_feature == 'bottom_lip':
                drawing.line(face_landmark[facial_feature], width=5, fill="red")
            elif facial_feature == "chin":
                drawing.line(face_landmark[facial_feature], width=5, fill="blue")
            else:
                drawing.line(face_landmark[facial_feature], width=5, fill="green")

    img_obj.save("drawn_face_features.png")

    image = Image.open("drawn_face_features.png")
    resize_image = image.resize((175, 159))
    img = ImageTk.PhotoImage(resize_image)

    img_label = Label(page, image=img)
    img_label.image = img
    img_label.place(x=386, y=151)


def detecting_faces():
    cam = cv.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        face_locs = face_locations(frame)
        if face_locs:
            for face_loc in face_locs:
                y1, x2, y2, x1 = face_loc
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv.imshow('Detecting Faces', frame)
        if cv.waitKey(1) == 27:
            break
    cam.release()
    cv.destroyAllWindows()

current_sign_in_name = ''


def define_face_sign_in(page):
    global current_sign_in_name
    # Append face paths to list
    face_paths = []
    face_names = []
    conn = db.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    data_base = c.fetchall()
    for data in data_base:
        face_names.append(data[0])
        face_paths.append("DefinedFaces/" + data[0] + ".png")
    conn.commit()
    conn.close()
    # Encoding Faces
    encoding_faces = []
    for face_path in face_paths:
        face = cv.imread(face_path)
        encode = face_encodings(face)[0]
        encoding_faces.append(encode)
    verification_counter = 0

    cam = cv.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        face_loc = face_locations(frame)  # Face Location
        if face_loc:
            y1, x2, y2, x1 = face_loc[0]
            font_size = 1.25 - (1 / (x2 - x1)) * 100
            if font_size < 0.60:
                font_size = 0.60
            current_face_encoding = face_encodings(frame)[0]
            face_cmp = compare_faces(encoding_faces, current_face_encoding, 0.55)
            face_dis = face_distance(encoding_faces, current_face_encoding)
            match_index = np.argmin(face_dis)
            if face_cmp[match_index]:
                verification_counter += 1
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv.rectangle(frame, (x1 - 1, y1 - 30), (x2 + 1, y1), (0, 255, 0), cv.FILLED)
                cv.putText(frame, str(face_names[match_index]).title(), (x1 + 6, y1 - 6), cv.FONT_HERSHEY_COMPLEX,
                           font_size,
                           (255, 255, 255), 1)
                if verification_counter == 5:
                    current_sign_in_name = face_names[match_index]
                    messagebox.showinfo("Info", "Welcome " + str(face_names[match_index]).title())
                    name_label = Label(page, text="Welcome "+str(face_names[match_index]).title(),
                                       bg="white", fg="#5F5F5F", font=("ReadexPro-bold", 14))
                    name_label.place(x=206, y=110)
                    break

            else:
                verification_counter = 0
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv.rectangle(frame, (x1 - 1, y1 - 30), (x2 + 1, y1), (0, 0, 255), cv.FILLED)
                cv.putText(frame, "Unknown", (x1 + 6, y1 - 6), cv.FONT_HERSHEY_COMPLEX,
                           font_size, (255, 255, 255), 1)
        cv.imshow('Sign In', frame)
        if cv.waitKey(1) == 27:
            break
    cam.release()
    cv.destroyAllWindows()
    raise_page(page)


def redefine_face():
    state = 0
    # Append face paths to list
    face_paths = []
    face_names = []

    # Check if the name already exists in the database
    conn = db.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM addresses")
    data_base = c.fetchall()
    for data in data_base:
        face_names.append(data[0])
        face_paths.append("DefinedFaces/" + data[0] + ".png")
    conn.commit()
    conn.close()

    defined_face = load_image_file("DefinedFaces/" + current_sign_in_name + ".png")
    defined_face_encode = face_encodings(defined_face)[0]

    cam = cv.VideoCapture(0)  # Webcam
    while True:
        ret, frame = cam.read()
        face_loc = face_locations(frame) # Face Location
        if face_loc:
            y1, x2, y2, x1 = face_loc[0]
            font_size = 1.25 - (1 / (x2 - x1)) * 100
            if font_size < 0.60:
                font_size = 0.60

            current_face_encoding = face_encodings(frame)[0]
            face_cmp = compare_faces([current_face_encoding], defined_face_encode, 0.55)

            if face_cmp[0]:
                state += 1
                if state == 5:
                    cv.imwrite("DefinedFaces/" + current_sign_in_name + ".png", frame)
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv.rectangle(frame, (x1 - 1, y1 - 30), (x2 + 1, y1), (0, 255, 0), cv.FILLED)
                cv.putText(frame, str(current_sign_in_name).title(), (x1 + 6, y1 - 6), cv.FONT_HERSHEY_COMPLEX,
                           font_size, (255, 255, 255), 1)
            else:
                state = 0
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv.rectangle(frame, (x1 - 1, y1 - 30), (x2 + 1, y1), (0, 0, 255), cv.FILLED)
                cv.putText(frame, ("Your not " + current_sign_in_name).title(), (x1 + 6, y1 - 6), cv.FONT_HERSHEY_COMPLEX,
                           font_size, (255, 255, 255), 1)

        cv.imshow('Redefine', frame)
        if cv.waitKey(1) == 27 or state == 5:
            if not face_loc:
                messagebox.showerror("Error", "Couldn't find any faces")
                break
            elif state == 5:
                messagebox.showinfo("Info", "Your face has been redefined successfully")
                break
    cam.release()
    cv.destroyAllWindows()