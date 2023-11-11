import tkinter as tk
from PIL import ImageTk, Image, ImageDraw, ImageFont
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename, askdirectory
import re
import random
import sqlite3
import os
import win32api
import mysql.connector as C

root=tk.Tk()
root.geometry("500x600")
root.title("(STUDENTS DETAILS MANAGEMENT SYSTEM)")

bg_color="sandybrown"
button="springgreen"

login_student_icon=tk.PhotoImage(file="C:\\Users\\Lenovo\\OneDrive\\Desktop\\pranay\\project\\student.png")
login_admin_icon=tk.PhotoImage(file="C:\\Users\\Lenovo\\OneDrive\\Desktop\\pranay\\project\\admin.png")
add_student_icon=tk.PhotoImage(file="C:\\Users\\Lenovo\\OneDrive\\Desktop\\pranay\\project\\add.png")
add_student_pic_icon=tk.PhotoImage(file="C:\\Users\\Lenovo\\OneDrive\\Desktop\\pranay\\project\\student_profile_img.png")

#########################################------------------------------------#########################################
'''
def init_database():

    if os.path.exists("students_accounts.db"):
        pass


    else:

        connection=C.connect(host="localhost",user="root",password="root",db="students_accounts")

        cursor= connection.cursor()

        cursor.execute("""
        create table data(
        id_number text,
        password text,
        name text,
        age text,
        gender text,
        phone_number text,
        student_class text,
        email text,
        image blob
        )
        """)

        connection.commit()
        connection.close()
'''
#########################################------------------------------------#########################################

def check_id_already_exists(id_number):
    connection=connection=C.connect(host="localhost",user="root",password="root",db="students_accounts")

    cursor= connection.cursor()

    cursor.execute(f"""
    SELECT id_number FROM data WHERE id_number == "{id_number}"
    """)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response

##################################-----------------------------------############################

def check_valid_password(id_number, password):
    connection=connection=C.connect(host="localhost",user="root",password="root",db="students_accounts")

    cursor= connection.cursor()

    cursor.execute(f"""
    SELECT password FROM data WHERE id_number == "{id_number}" AND password == "{password}"
    """)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response

#########################################------------------------------------#########################################

def add_data(id_number ,password ,name ,age ,gender,phone_number,
            student_class,email,pic_data):
    connection=connection=C.connect(host="localhost",user="root",password="root",db="students_accounts")

    cursor= connection.cursor()

    cursor.execute("""
    INSERT INTO data VALUES("{id_number}", "{password}", "{name}",
    "{age}", "{gender}","{phone_number}","{student_class}","{email}", ?)
    """,[pic_data])

    connection.commit()
    connection.close()

#########################################------------------------------------#########################################
def confirmation_box(message):

    answer=tk.BooleanVar()
    answer.set(False)

    def action(ans):
        answer.set(ans)
        confirmation_box_fm.destroy()
    
    confirmation_box_fm=tk.Frame(root,highlightbackground=bg_color, highlightthickness=3)

    message_lb=tk.Label(confirmation_box_fm, text=message, font=("Bold",12))
    message_lb.pack(pady=20)

    cancel_btn=tk.Button(confirmation_box_fm, text="CANCEL", font=("Bold",12),
                         bd=2, bg="green",fg="white", command=lambda:action(False))
    cancel_btn.place(x=50, y=160)

    yes_btn=tk.Button(confirmation_box_fm, text="Yes", font=("Bold",12),
                         bd=2, bg="red",fg="white",command=lambda:action(True))
    yes_btn.place(x=190, y=160, width=80)

    confirmation_box_fm.place(x=100,y=120, width=320,height=220)

    root.wait_window(confirmation_box_fm)
    return answer.get()
#########################################------------------------------------#########################################
def message_box(message):
    message_box_fm=tk.Frame(root,highlightbackground=bg_color, highlightthickness=3)

    close_btn=tk.Button(message_box_fm, text="X", bd=0, font=("Bold", 13), 
                        fg="red", command=lambda: message_box_fm.destroy())
    close_btn.place(x=285,y=5)

    message_lb= tk.Label(message_box_fm, text=message, font=("Bold", 15))
    message_lb.pack(pady=50)

    message_box_fm.place(x=100, y=120, width=320, height=200)

#########################################------------------------------------#########################################

def draw_student_card(student_pic_path, student_data):

    labels="""
ID Number:
Name:
Gender:
Age:
Class:
Contact:
Email:
"""

    student_card=Image.open("C:\\Users\\Lenovo\\OneDrive\\Desktop\\pranay\\project\\student_card_frame.png")
    pic = Image.open(student_pic_path).resize((100, 100))


    student_card.paste(pic, (15, 25))

    draw= ImageDraw.Draw(student_card)

    heading_font= ImageFont.truetype("bahnschrift", 18)
    labels_font= ImageFont.truetype("arial", 15)
    data_font= ImageFont.truetype("bahnschrift", 15)

    draw.text(xy=(150,60), text="Student Card", fill=(0,0,0),
              font=heading_font)
    
    draw.multiline_text(xy=(15,120), text=labels, fill=(0,0,0,),
                        font=labels_font, spacing=6)
    
    draw.multiline_text(xy=(95, 120), text=student_data, fill=(0,0,0),
                        font=data_font, spacing=float(8.5))

    return student_card

#########################################------------------------------------#########################################

def student_card_page(student_card_obj):

    def save_student_card():
        path=askdirectory()

        if path:
            print(path)

            student_card_obj.save(f"{path}/student_card.png")

    def print_student_card():
         path=askdirectory()

         if path:
            print(path)

            student_card_obj.save(f"{path}/student_card.png")

            win32api.ShellExecute(0, "print", f"{path}/student_card.png",
                                  None, ".",0)
            
    def close_page():
        student_card_page_fm.destroy()
        root.update()
        student_login_page()

    student_card_img= ImageTk.PhotoImage(student_card_obj)
    
    student_card_page_fm= tk.Frame(root, highlightbackground=bg_color, 
                                   highlightthickness=3)
    
    heading_lb=tk.Label(student_card_page_fm, text="Student Card",
                         bg=bg_color, fg="white", font=("Bold", 16))
    heading_lb.place(x=0,y=0, width=410)

    close_btn= tk.Button(student_card_page_fm, text="X", bg=bg_color,
                         fg="white", font=("Bold", 13), bd=0,
                         command=close_page)
    close_btn.place(x=370, y=0)

    student_card_lb=tk.Label(student_card_page_fm, image=student_card_img)
    student_card_lb.place(x=50, y=50)

    student_card_lb.image=student_card_img

    save_student_card_btn= tk.Button(student_card_page_fm, text="Save Student Card",
                                     bg="green", fg="white", font=("Bold", 15),
                                     bd=1 ,command=save_student_card)
    save_student_card_btn.place(x=80, y=375)

    print_student_card_btn= tk.Button(student_card_page_fm, text="🖨",
                                     bg="deepskyblue", fg="black", font=("Bold", 18),
                                     bd=1, command=print_student_card)
    print_student_card_btn.place(x=270, y=370)

    student_card_page_fm.place(x=50, y=30, width=400, height=450)

#######################################------------------------------------#########################################
def welcome_page():
    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        root.update()
        student_login_page()

    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    def forward_to_add_account_page():
        welcome_page_fm.destroy()
        root.update()
        add_account_page()

    welcome_page_fm=tk.Frame(root, highlightbackground=bg_color, highlightthickness=3) 

    heading_lb=tk.Label(welcome_page_fm,text="WELCOME TO THE SYSTEM", bg=bg_color, fg="white", font=("Bold",18))
    heading_lb.place(x=0,y=0,width=400,)

    image1 = Image.open("C:\\Users\\Lenovo\\OneDrive\\Desktop\\pranay\\project\\logo1.png")
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(welcome_page_fm, image=test)
    label1.image = test
    label1.place(x=135, y=40,width=120,height=100)

    student_login_btn=tk.Button(welcome_page_fm,text="Login student", bg=button,borderwidth=2, relief="solid"
                                ,command=forward_to_student_login_page)
    student_login_btn.place(x=230,y=244,width=100,height=35)

    admin_login_btn=tk.Button(welcome_page_fm,text="Login admin", bg=button,borderwidth=2, relief="solid"
                              ,command=forward_to_admin_login_page)
    admin_login_btn.place(x=51,y=244,width=100,height=35)

    admin_login_img=tk.Button(welcome_page_fm,image=login_admin_icon, bd=0)
    admin_login_img.place(x=60,y=162)

    student_login_img=tk.Button(welcome_page_fm,image=login_student_icon, bd=0)
    student_login_img.place(x=240,y=162)

    add_student_btn=tk.Button(welcome_page_fm,text="add new student", 
                              bg=button,borderwidth=2, relief="solid",command=forward_to_add_account_page)
    add_student_btn.place(x=140,y=370,width=100,height=35)

    add_student_img=tk.Button(welcome_page_fm,image=add_student_icon, bd=0)
    add_student_img.place(x=150,y=288)

    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400, height=430, bg="#f8f8ff")

#########################################------------------------------------#########################################

def student_login_page():
    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()

    def remove_highlight_warning(entry):
        if entry["highlightbackground"]!="grey":
            if entry.get() != "":
                entry.config(highlightcolor="black",
                             highlightbackground="grey")
    def login_account():
        verify_id_number= check_id_already_exists(id_number=id_number_ent.get())
        
        if verify_id_number:
            print("ID is correct")

        else:
            print("!oops ID is Incorrect")
            id_number_ent.config(highlightcolor="red",
                             highlightbackground="red")
            
            message_box(message="Please Enter Valid Student ID")
            

    student_login_page_fm=tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb=tk.Label(student_login_page_fm,text="Student Login Page", bg=bg_color,fg="white",font=("Bold",18))
    heading_lb.place(x=0,y=0,width=400)

    back_btn=tk.Button(student_login_page_fm,text="⬅",font=("Bold",20), fg="black",bd=0,
                       command=forward_to_welcome_page)
    back_btn.place(x=5,y=40)

    stud_icon_lb=tk.Label(student_login_page_fm,image=login_student_icon)
    stud_icon_lb.place(x=150, y=40)

    id_number_lb=tk.Label(student_login_page_fm, text="ENTER STUDENT ID NUMBER",font=("bold",10))
    id_number_lb.place(x=77, y=173)

    id_number_ent= tk.Entry(student_login_page_fm, font=("Bold", 15), fg="black", 
                        highlightcolor=bg_color,highlightbackground="grey", highlightthickness=2)
    id_number_ent.place(x=80,y=190)
    id_number_ent.bind("<KeyRelease>", lambda e: remove_highlight_warning(entry=id_number_ent))

    password_lb=tk.Label(student_login_page_fm, text="ENTER PASSWORD",font=("bold",10))
    password_lb.place(x=77, y=250)

    password_ent= tk.Entry(student_login_page_fm, font=("Bold", 15), fg="black", 
                        highlightcolor=bg_color,highlightbackground="grey", highlightthickness=2,show="*")
    password_ent.place(x=80,y=270)

    login_btn=tk.Button(student_login_page_fm, text="LogIN",font=("Bold",15),
                        bg="navy", fg="white",width="20",height="1", command=login_account)
    login_btn.place(x=79,y=320)

    forget_password_btn=tk.Button(student_login_page_fm, text="⚠\n Forgot Password?", fg="dark blue", bd=0)
    forget_password_btn.place(x=140,y=380)

    student_login_page_fm.pack(pady=30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=400, height=450, bg="#f8f8ff")

#########################################------------------------------------#########################################
def admin_login_page():
    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()

    admin_login_page_fm=tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb=tk.Label(admin_login_page_fm,text="Admin Login Page", bg=bg_color,fg="white",font=("Bold",18))
    heading_lb.place(x=0,y=0,width=400)

    back_btn=tk.Button(admin_login_page_fm,text="⬅",font=("Bold",20), fg="black",bd=0,
                       command=forward_to_welcome_page)
    back_btn.place(x=5,y=40)

    stud_icon_lb=tk.Label(admin_login_page_fm,image=login_admin_icon)
    stud_icon_lb.place(x=150, y=40)

    username_lb=tk.Label(admin_login_page_fm, text="ENTER ADMIN USERNAME",font=("bold",10))
    username_lb.place(x=77, y=173)

    username_ent= tk.Entry(admin_login_page_fm, font=("Bold", 15), fg="black", 
                            highlightcolor=bg_color,highlightbackground="grey", highlightthickness=2)
    username_ent.place(x=80,y=190)

    password_lb=tk.Label(admin_login_page_fm, text="ENTER ADMIN PASSWORD",font=("bold",10))
    password_lb.place(x=77, y=250)

    password_ent= tk.Entry(admin_login_page_fm, font=("Bold", 15), fg="black", 
                            highlightcolor=bg_color,highlightbackground="grey", highlightthickness=2,show="*")
    password_ent.place(x=80,y=270)

    login_btn=tk.Button(admin_login_page_fm, text="LogIN",font=("Bold",15),
                            bg="navy", fg="white",width="20",height="1")
    login_btn.place(x=79,y=320)

    forget_password_btn=tk.Button(admin_login_page_fm, text="⚠\n Forgot Password?", fg="dark blue", bd=0)
    forget_password_btn.place(x=140,y=380)

    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=400, height=450, bg="#f8f8ff")

#########################################------------------------------------#########################################

student_gender=tk.StringVar()


class_list=["6-A","6-B","6-C","6-D","7-A","7-B","7-C","7-D","8-A","8-B","8-C","8-D","9-A","9-B","9-C","9-D","10-A","10-B",
            "10-C","10-D","11-A","11-B","11-C","12-A","12-B","12-C",]

def add_account_page():

    pic_path=tk.StringVar()
    pic_path.set("")

    def open_pic():
        path= askopenfilename()

        if path:
            img=ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
            pic_path.set(path)

            add_pic_btn.config(image=img)
            add_pic_btn.image=img

    def forward_to_welcome_page():

        ans=confirmation_box(message="Do You Want To Leave\nRegistration Form?")
        
        if ans:
            add_account_page_fm.destroy()
            root.update()
            welcome_page()

    def remove_highlight_warning(entry):
        if entry["highlightbackground"]!="grey":
            if entry.get() != "":
                entry.config(highlightcolor="black",
                             highlightbackground="grey")
    
    def check_invalid_email(email):
        pattern="^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
        match = re.match(pattern=pattern, string=email)
 
        return match
    
    def generate_id_number():
        generated_id=""

        for i in range(6):

            generated_id += str(random.randint(0,9))

        if not check_id_already_exists(id_number=generated_id):

            print("id number:", generated_id)

            student_id.config(state=tk.NORMAL)
            student_id.delete(0, tk.END)
            student_id.insert(tk.END, generated_id)
            student_id.config(state="readonly")

        else:
            generate_id_number()

    def check_input_validation():
        if student_name_ent.get()=="":
            student_name_ent.config(highlightcolor="red"
                                    ,highlightbackground="red")
            student_name_ent.focus()
            message_box(message="Student Full Name is Required")

        elif student_age_ent.get()=="":
            student_age_ent.config(highlightcolor="red"
                                    ,highlightbackground="red")
            student_age_ent.focus()
            message_box(message="Student Age is Required")

        elif student_contact_ent.get() == "":
            student_contact_ent.config(highlightcolor="red"
                                    ,highlightbackground="red")
            student_contact_ent.focus()
            message_box(message="Student Phone Number is Required")

        elif select_class_btn.get() == "":
            select_class_btn.focus()
            message_box(message="Student Class is Required")

        elif student_email_ent.get() == "":
            student_email_ent.config(highlightcolor="red"
                                    ,highlightbackground="red")
            student_email_ent.focus()
            message_box(message="Student Email ID is Required")

        elif not check_invalid_email(email=student_email_ent.get().lower()):
            student_email_ent.config(highlightcolor="red"
                                    ,highlightbackground="red")
            student_email_ent.focus()
            message_box(message="Please Enter Valid\nEmail ID")

        elif account_password_ent.get() == "":
            account_password_ent.config(highlightcolor="red"
                                    ,highlightbackground="red")
            account_password_ent.focus()
            message_box(message="Password is Required")
        else:

            pic_data=b""

            if pic_path.get() != "":

                resize_pic=Image.open(pic_path.get()).resize((100,100))
                resize_pic.save("temp_pic.png")

                read_data = open("temp_pic.png", "rb")
                pic_data = read_data.read()
                read_data.close()

            else:
                read_data = open("C:\\Users\\Lenovo\\OneDrive\\Desktop\\pranay\\project\\student_profile_img.png", "rb")
                pic_data = read_data.read()
                read_data.close()


            add_data(id_number=student_id.get(),
                     password=account_password_ent.get(),
                     name=student_name_ent.get(),
                     age=student_age_ent.get(),
                     gender=student_gender.get(),
                     phone_number=student_contact_ent.get(),
                     student_class=select_class_btn.get(),
                     email=student_email_ent.get(),
                     pic_data=pic_data)
            
            message_box("Account Created Successfully")
             
            data=f"""
{student_id.get()}
{student_name_ent.get()}
{student_gender.get()}
{student_age_ent.get()}
{select_class_btn.get()}
{student_contact_ent.get()}
{student_email_ent.get()}
"""

            get_student_card=draw_student_card(student_pic_path=pic_path.get(),
                              student_data=data)
            student_card_page(student_card_obj=get_student_card)

            add_account_page_fm.destroy()
            root.update()

            message_box("Account Created Successfully")
            

    add_account_page_fm=tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    add_pic_section_fm= tk.Frame(add_account_page_fm, highlightbackground="black", highlightthickness=2)
    add_pic_btn=tk.Button(add_pic_section_fm, image=add_student_pic_icon,bd=0, command=open_pic)
    add_pic_btn.pack()

    add_pic_section_fm.place(x=5, y=5, width= 105, height=105)


    student_name_lb=tk.Label(add_account_page_fm, text="Enter Student Full Name", font=("Bold",10),bg="white")
    student_name_lb.place(x=5,y=130)

    student_name_ent=tk.Entry(add_account_page_fm, font=("Bold",12), 
                            highlightcolor="black", highlightbackground="grey",highlightthickness=2)
    student_name_ent.place(x=5,y=160, width=180)
    student_name_ent.bind("<KeyRelease>",
                          lambda e: remove_highlight_warning(entry=student_name_ent))


    student_gender_lb=tk.Label(add_account_page_fm, text="Select Student Gender", font=("Bold", 10),bg="white")
    student_gender_lb.place(x=5, y=210)

    male_gender_btn=tk.Radiobutton(add_account_page_fm, text="MALE",font=("Bold",10),
                                bg="white", variable=student_gender, value="MALE")
    male_gender_btn.place(x=5, y=235)

    female_gender_btn=tk.Radiobutton(add_account_page_fm, text="FEMALE",font=("Bold",10),
                                    bg="white",variable=student_gender,value="FEMALE")
    female_gender_btn.place(x=75, y=235)
    student_gender.set("MALE")


    student_age_lb=tk.Label(add_account_page_fm, text="Enter Student Age",
                            font=("Bold",10), bg="white")
    student_age_lb.place(x=5, y=275)

    student_age_ent=tk.Entry(add_account_page_fm, font=("Bold",12), 
                            highlightcolor="black", highlightbackground="grey",highlightthickness=2)
    student_age_ent.place(x=5,y=305, width=180)

    student_age_ent.bind("<KeyRelease>",
                          lambda e: remove_highlight_warning(entry=student_age_ent))


    student_contact_lb=tk.Label(add_account_page_fm, text="Enter Phone Number",
                            font=("Bold",10), bg="white")
    student_contact_lb.place(x=5, y=360)

    student_contact_ent=tk.Entry(add_account_page_fm, font=("Bold",12), 
                            highlightcolor="black", highlightbackground="grey",highlightthickness=2)
    student_contact_ent.place(x=5,y=390, width=180)

    student_contact_ent.bind("<KeyRelease>",
                          lambda e: remove_highlight_warning(entry=student_contact_ent))


    student_class_lb=tk.Label(add_account_page_fm, text="Select Student Class",
                            font=("Bold",10), bg="white")
    student_class_lb.place(x=5, y=445)

    select_class_btn=Combobox(add_account_page_fm, font=("bold",12), state="readonly", values=class_list)
    select_class_btn.place(x=5,y=475, width=180, height=30)


    student_id_lb= tk.Label(add_account_page_fm, text="Student ID Number:" ,font=("bold",10),bg="white")
    student_id_lb.place(x=240, y=35)

    student_id= tk.Entry(add_account_page_fm,font=("Bold",16),bd=0)
    student_id.place(x=380, y=35, width=80)

    
    student_id.config(state="readonly")

    generate_id_number()

    id_info_lb=tk.Label(add_account_page_fm, text="""Atumatically Generated ID Number!
                    For Student Login!""",justify=tk.LEFT,bg="lightcoral")
    id_info_lb.place(x=240, y=65,width=220)


    student_email_lb=tk.Label(add_account_page_fm, text="Enter Student Email ID",
                            font=("Bold",10), bg="white")
    student_email_lb.place(x=240, y=130)

    student_email_ent=tk.Entry(add_account_page_fm, font=("Bold",12), 
                            highlightcolor="black", highlightbackground="grey",highlightthickness=2)
    student_email_ent.place(x=240,y=160, width=180)

    student_email_ent.bind("<KeyRelease>",
                          lambda e: remove_highlight_warning(entry=student_email_ent))

    email_info_lb=tk.Label(add_account_page_fm, text="""Via Email ID Student Can Recover 
Account! In Case of Forgetten Password 
and Will Get Notifications.""",font=("Bold",8), justify=tk.LEFT)
    email_info_lb.place(x=240, y=200, width=220)


    account_password_lb=tk.Label(add_account_page_fm, text="Create Account Password", font=("Bold", 10),bg="white")
    account_password_lb.place(x=240, y=275)

    account_password_ent=tk.Entry(add_account_page_fm, font=("Bold",12), 
                            highlightcolor="black", highlightbackground="grey",highlightthickness=2)
    account_password_ent.place(x=240,y=307, width=180)

    account_password_ent.bind("<KeyRelease>",
                          lambda e: remove_highlight_warning(entry=account_password_ent))

    account_paasword_info_lb= tk.Label(add_account_page_fm, text="""Via Student Created Password 
And Provided Student ID Number
Student Can Login Account.""", justify=tk.LEFT)
    account_paasword_info_lb.place(x=240,y=345)
    

    home_btn= tk.Button(add_account_page_fm, text="HOME", font=("Bold", 12),
                        bg="red", fg="white", bd=2, command=forward_to_welcome_page)
    home_btn.place(x=240, y=420)


    submit_btn= tk.Button(add_account_page_fm, text="SUBMIT", font=("Bold", 12),
                        bg="green", fg="white", bd=2, command=check_input_validation)
    submit_btn.place(x=360, y=420)



    add_account_page_fm.pack(pady=5)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width=480, height=580, bg="#f8f8ff")

#init_database()
add_account_page()
#student_card_page()
root.mainloop()
