from Functions import *
from tkinter import font
import pyglet

pyglet.font.add_file('ReadexPro-bold.ttf')

database_path = "data.db"
conn = db.connect(database_path)
c = conn.cursor()
try:
    c.execute("""CREATE TABLE addresses(
    name text
    )
    """)
except db.OperationalError:
    pass

conn.commit()
conn.close()


def raise_page(page):
    page.tkraise()


window = Tk()
window.title("Face Recognition System")
window.iconbitmap(f"Designs/face_recognition_icon.ico")
window.geometry("750x425")
window.configure(bg="white")

entry_font = font.Font(family=("Calibre", 12), weight="bold")

# ------------------ START PAGE ------------------
start_page = Frame(window)
start_page.place(anchor=CENTER, relx=0, rely=0)

start_page_background = ImageTk.PhotoImage(Image.open(f"Designs/Backgrounds/StartPageBackground.png"))
start_page_background_label = Label(start_page, image=start_page_background,
                                    bd=0, highlightthickness=0)
start_page_background_label.pack()

sign_in_button_img = PhotoImage(file=f"Designs/Buttons/SignInButton.png")
sign_in_button = Button(start_page, image=sign_in_button_img, borderwidth=0,
                        command=lambda: raise_page(sign_in_page), relief="flat")
sign_in_button.place(x=400, y=300, width=100, height=39)

register_button_img = PhotoImage(file=f"Designs/Buttons/RegisterButton.png")
register_button = Button(start_page, image=register_button_img, borderwidth=0,
                         command=lambda: raise_page(register_page), relief="flat")
register_button.place(x=250, y=300, width=108, height=39)

# ------------------ REGISTER PAGE ------------------
register_page = Frame(window)
register_page.place(anchor=CENTER, relx=0, rely=0)

register_page_background = ImageTk.PhotoImage(Image.open(f"Designs/Backgrounds/RegisterBackground.png"))
register_page_background_label = Label(register_page, image=register_page_background,
                                       bd=0, highlightthickness=0)
register_page_background_label.pack()

text_box_img = PhotoImage(file=f"Designs/TextBox.png")
name_img_label = Label(register_page, image=text_box_img, bd=0, highlightthickness=0).place(x=325, y=212)
name_entry = Entry(register_page, bd=0, bg="#c4b2f6", highlightthickness=0, font=("ReadexPro-bold", 18), fg="white")
name_entry.place(x=350, y=212, width=250.0, height=48)

back_to_start_page_btn_img = PhotoImage(file=f"Designs/Buttons/BackToStartPageButton.png")
back_to_start_page_btn = Button(register_page, image=back_to_start_page_btn_img, bd=0, highlightthickness=0,
                                command=lambda: raise_page(start_page), relief="flat", bg="white")
back_to_start_page_btn.place(x=8, y=383)

define_your_face_btn_img = PhotoImage(file=f"Designs/Buttons/DefineYourFaceButton.png")
define_your_face_btn = Button(register_page, image=define_your_face_btn_img, bd=0, highlightthickness=0,
                              command=lambda: define_face_register(name_entry, sign_in_page), relief="flat", bg="white")
define_your_face_btn.place(x=383, y=288)

sign_in_small_button_img = PhotoImage(file=f"Designs/Buttons/SignInSmallButton.png")
sign_in_small_button = Button(register_page, image=sign_in_small_button_img, borderwidth=0,
                              command=lambda: raise_page(sign_in_page), relief="flat")
sign_in_small_button.place(x=657, y=383, width=85, height=34)

# ------------------ Sign In PAGE ------------------
sign_in_page = Frame(window)
sign_in_page.place(anchor=CENTER, relx=0, rely=0)

Sign_in_page_background = ImageTk.PhotoImage(Image.open(f"Designs/Backgrounds/SignInBackground.png"))
Sign_in_page_background_label = Label(sign_in_page, image=Sign_in_page_background,
                                      bd=0, highlightthickness=0)
Sign_in_page_background_label.pack()

define_your_face_btn = Button(sign_in_page, image=define_your_face_btn_img, bd=0, highlightthickness=0,
                              command=lambda: define_face_sign_in(applications_page), relief="flat", bg="white")
define_your_face_btn.place(x=354, y=222)

back_to_start_page_btn = Button(sign_in_page, image=back_to_start_page_btn_img, bd=0, highlightthickness=0,
                                command=lambda: raise_page(start_page), relief="flat", bg="white")
back_to_start_page_btn.place(x=8, y=383)

register_small_button_img = PhotoImage(file=f"Designs/Buttons/RegisterSmallButton.png")
register_small_button = Button(sign_in_page, image=register_small_button_img, borderwidth=0,
                               command=lambda: raise_page(register_page), relief="flat")
register_small_button.place(x=651, y=383, width=91, height=34)
# ------------------ APPLICATIONS PAGE ------------------
applications_page = Frame(window)
applications_page.place(anchor=CENTER, relx=0, rely=0)

applications_background_img = ImageTk.PhotoImage(Image.open(f"Designs/Backgrounds/ApplicationsBackground.png"))
applications_background_img_label = Label(applications_page, image=applications_background_img,
                                          bd=0, highlightthickness=0)
applications_background_img_label.pack()

sign_out_btn_img = PhotoImage(file=f"Designs/Buttons/SignOutButton.png")
sign_out_btn = Button(applications_page, image=sign_out_btn_img, bd=0, highlightthickness=0,
                      command=lambda: raise_page(start_page), relief="flat", bg="white")
sign_out_btn.place(x=644, y=380)

recognizing_face_btn_img = PhotoImage(file=f"Designs/Buttons/RecognizingFacesButton.png")
recognizing_face_btn = Button(applications_page, image=recognizing_face_btn_img, bd=0, highlightthickness=0,
                              command=recognizing_faces, relief="flat", bg="#D5CEE8")
recognizing_face_btn.place(x=129, y=179)

detecting_faces_btn_img = PhotoImage(file=f"Designs/Buttons/DetectingFacesButton.png")
detecting_faces_btn = Button(applications_page, image=detecting_faces_btn_img, bd=0, highlightthickness=0,
                             command=detecting_faces, relief="flat", bg="#D5CEE8")
detecting_faces_btn.place(x=384, y=179)

DetectingFacialFeaturesBtn_img = PhotoImage(file=f"Designs/Buttons/DetectingFacialFeaturesButton.png")
DetectingFacialFeaturesBtn = Button(applications_page, image=DetectingFacialFeaturesBtn_img, bd=0, highlightthickness=0,
                                    command=lambda: raise_page(detecting_facial_features_page), relief="flat",
                                    bg="#D5CEE8")
DetectingFacialFeaturesBtn.place(x=129, y=222)

draw_facial_features_in_pictures_btn_img = PhotoImage(file=f"Designs/Buttons/DrawFacialFeaturesInPicturesButton.png")
draw_facial_features_in_pictures_btn = Button(applications_page, image=draw_facial_features_in_pictures_btn_img, bd=0,
                                              highlightthickness=0,
                                              command=lambda: raise_page(draw_facial_features_page),
                                              relief="flat", bg="#D5CEE8")
draw_facial_features_in_pictures_btn.place(x=384, y=222)

redefine_your_face_btn_img = PhotoImage(file=f"Designs/Buttons/RedefineYourFaceButton.png")
redefine_your_face_btn = Button(applications_page, image=redefine_your_face_btn_img, bd=0, highlightthickness=0,
                                command=redefine_face, relief="flat", bg="#D5CEE8")
redefine_your_face_btn.place(x=255, y=265)

# ------------------ DEFECTING FACIAL FEATURES PAGE ------------------

detecting_facial_features_page = Frame(window)
detecting_facial_features_page.place(anchor=CENTER, relx=0, rely=0)

detecting_facial_features_background = ImageTk.PhotoImage(
    Image.open(f"Designs/Backgrounds/DetectingFacialFeaturesBackground.png"))
detecting_facial_features_background_label = Label(detecting_facial_features_page,
                                                   image=detecting_facial_features_background, bd=0,
                                                   highlightthickness=0)
detecting_facial_features_background_label.pack()

is_on = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
on = []
off = []


def switch(button, i):
    global is_on

    if not is_on[i]:
        button.config(image=off[i])
        is_on[i] = 1
    else:
        button.config(image=on[i])
        is_on[i] = 0

button_images = [
        'Chin',
        'LeftEye',
        'RightEye',
        'LeftEyebrow',
        'RightEyebrow',
        'NoseBridge',
        'NoseTip',
        'TopLip',
        'BottomLip',
        'SelectAllButton'
]
for button_image in button_images:
    on.append(PhotoImage(file="Designs/Buttons/FacialFeaturesButtonsWhite/"+button_image+".png"))
    off.append(PhotoImage(file="Designs/Buttons/FacialFeaturesButtonsBlack/"+button_image+".png"))


chin_btn = Button(detecting_facial_features_page, image=on[0], bd=0, bg="#D5CEE8",
                  command=lambda: switch(chin_btn, 0))
left_eye_btn = Button(detecting_facial_features_page, image=on[1], bd=0, bg="#D5CEE8",
                      command=lambda: switch(left_eye_btn, 1))
right_eye_btn = Button(detecting_facial_features_page, image=on[2], bd=0, bg="#D5CEE8",
                       command=lambda: switch(right_eye_btn, 2))
left_eyebrow_btn = Button(detecting_facial_features_page, image=on[3], bd=0, bg="#D5CEE8",
                          command=lambda: switch(left_eyebrow_btn, 3))
right_eyebrow_btn = Button(detecting_facial_features_page, image=on[4], bd=0, bg="#D5CEE8",
                           command=lambda: switch(right_eyebrow_btn, 4))
nose_bridge_btn = Button(detecting_facial_features_page, image=on[5], bd=0, bg="#D5CEE8",
                         command=lambda: switch(nose_bridge_btn, 5))
nose_tip_btn = Button(detecting_facial_features_page, image=on[6], bd=0, bg="#D5CEE8",
                      command=lambda: switch(nose_tip_btn, 6))
top_lip_btn = Button(detecting_facial_features_page, image=on[7], bd=0, bg="#D5CEE8",
                     command=lambda: switch(top_lip_btn, 7))
bottom_lip_btn = Button(detecting_facial_features_page, image=on[8], bd=0, bg="#D5CEE8",
                        command=lambda: switch(bottom_lip_btn, 8))
start_btn_img = PhotoImage(file=f"Designs/Buttons/StartButton.png")
start_btn = Button(detecting_facial_features_page, image=start_btn_img, bd=0, bg="#D5CEE8",
                   command=lambda: detecting_facial_features_start(is_on))
start_btn.place(x=486, y=271)

select_all_btn = Button(detecting_facial_features_page, image=on[9], bd=0, bg="#D5CEE8",
                        command=lambda: switch(select_all_btn, 9))

chin_btn.place(x=113, y=211)
left_eyebrow_btn.place(x=291, y=211)
right_eyebrow_btn.place(x=384, y=211)
nose_bridge_btn.place(x=487, y=211)
nose_tip_btn.place(x=577, y=211)
left_eye_btn.place(x=156, y=211)
right_eye_btn.place(x=219, y=211)
top_lip_btn.place(x=307, y=246)
bottom_lip_btn.place(x=364, y=246)
select_all_btn.place(x=524, y=178)

sign_out_btn = Button(detecting_facial_features_page, image=sign_out_btn_img, bd=0, highlightthickness=0,
                      command=lambda: raise_page(start_page), relief="flat", bg="white")
sign_out_btn.place(x=644, y=380)

back_to_applications_page_btn_img = PhotoImage(file=f"Designs/Buttons/BackToApplicationsButton.png")
back_to_applications_page_btn = Button(detecting_facial_features_page, image=back_to_applications_page_btn_img, bd=0,
                                       highlightthickness=0, command=lambda: raise_page(applications_page),
                                       relief="flat", bg="white")
back_to_applications_page_btn.place(x=8, y=383)

# ------------------ DRAW FACIAL FEATURES PAGE ------------------

draw_facial_features_page = Frame(window)
draw_facial_features_page.place(anchor=CENTER, relx=0, rely=0)

draw_facial_features_background_img = ImageTk.PhotoImage(Image.open(f"Designs/Backgrounds/DrawFacialFeaturesBackground.png"))
draw_facial_features_background_img_label = Label(draw_facial_features_page,
                                                  image=draw_facial_features_background_img, bd=0, highlightthickness=0)
draw_facial_features_background_img_label.pack()

back_to_applications_page_btn = Button(draw_facial_features_page, image=back_to_applications_page_btn_img, bd=0,
                                       highlightthickness=0, command=lambda: raise_page(applications_page),
                                       relief="flat", bg="white")
back_to_applications_page_btn.place(x=8, y=383)

select_picture_btn_img = PhotoImage(file=f"Designs/Buttons/SelectPictureButton.png")
select_picture_btn = Button(draw_facial_features_page, image=select_picture_btn_img,  bd=0, highlightthickness=0,
                            command=lambda: select_picture(draw_facial_features_page), relief="flat", bg="#D5CEE8")
select_picture_btn.place(x=184, y=214)

sign_out_btn = Button(draw_facial_features_page, image=sign_out_btn_img, bd=0, highlightthickness=0,
                      command=lambda: raise_page(start_page), relief="flat", bg="white")
sign_out_btn.place(x=644, y=380)

# Pages
for frame in (start_page, register_page, sign_in_page, applications_page, detecting_facial_features_page,
              draw_facial_features_page):
    frame.grid(row=0, column=0, sticky='news')

window.resizable(False, False)
raise_page(start_page)
window.mainloop()
