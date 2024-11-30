import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk  # pip install pillow

class recruitmentClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1370x700+0+0")
        self.root.title("Fashion Management System | Developed By DuyKhanh")
        self.root.config(bg="#fafafa")

        # All Variables
        self.var_r_id = StringVar()
        self.var_r_name = StringVar()
        self.var_r_email = StringVar()
        self.var_r_address = StringVar()
        self.var_r_contact = StringVar()
        self.var_r_sex = StringVar()
        self.var_r_date = StringVar()
        self.var_r_cccd = StringVar()
        self.var_r_workplace = StringVar()

        # Title
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Fashion Management System", image=self.icon_title, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)
        
        btn_logout = Button(self.root, text="Back", command=self.back, font=("times new roman", 15, "bold"),
                            bg="#8856a7", cursor="hand2").place(x=1180, y=10, height=50, width=150)

        # Recruitment Frame
        Rec_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Rec_frame.place(x=150, y=120, width=390, height=550)
        title = Label(Rec_frame, text="Recruitment System", font=("times new roman", 30, "bold"), bg="white").place(x=23, y=20, width=340)
        

        self.img_Main = Image.open("images/recruitment.jpg")
        self.img_Main = self.img_Main.resize((670, 450), Image.LANCZOS)
        self.img_Main = ImageTk.PhotoImage(self.img_Main)
        right_img_label = Label(self.root, image=self.img_Main, bd=0)
        right_img_label.place(x=550, y=120)

        title_Main = Label(self.root, text="Welcome to DuyKhanh Store", font=("times new roman", 35, "bold"), fg="#33CCCC")
        title_Main.place(x=590, y=120 + 470, height=70)

        # Labels and Entries
        lbl_r_name = Label(Rec_frame, text="Full name", font=("times new roman", 18), bg="#FCFCFC").place(x=30, y=80)
        lbl_r_email = Label(Rec_frame, text="Email", font=("times new roman", 18), bg="#FCFCFC").place(x=30, y=130)
        lbl_r_address = Label(Rec_frame, text="Address", font=("times new roman", 18), bg="#FCFCFC").place(x=30, y=180)
        lbl_r_contact = Label(Rec_frame, text="Contact", font=("times new roman", 18), bg="#FCFCFC").place(x=30, y=230)
        lbl_r_date = Label(Rec_frame, text="Date", font=("times new roman", 18), bg="#FCFCFC").place(x=30, y=280)
        lbl_r_sex = Label(Rec_frame, text="Gender", font=("times new roman", 18), bg="#FCFCFC").place(x=30, y=330)
        lbl_r_cccd = Label(Rec_frame, text="CCCD", font=("times new roman", 18), bg="#FCFCFC").place(x=30, y=380)
        lbl_r_workplace = Label(Rec_frame, text="Workplace", font=("times new roman", 18), bg="#FCFCFC").place(x=30, y=430)

        txt_name = Entry(Rec_frame, textvariable=self.var_r_name, font=("times new roman", 15), bg='#99d8c9').place(x=150, y=80, width=200)
        txt_email = Entry(Rec_frame, textvariable=self.var_r_email, font=("times new roman", 15), bg='#99d8c9').place(x=150, y=130, width=200)
        txt_address = Entry(Rec_frame, textvariable=self.var_r_address, font=("times new roman", 15), bg='#99d8c9').place(x=150, y=180, width=200)
        txt_contact = Entry(Rec_frame, textvariable=self.var_r_contact, font=("times new roman", 15), bg='#99d8c9').place(x=150, y=230, width=200)
        txt_date = Entry(Rec_frame, textvariable=self.var_r_date, font=("times new roman", 15), bg='#99d8c9').place(x=150, y=280, width=200)
        
        cmb_sex = ttk.Combobox(Rec_frame, textvariable=self.var_r_sex, values=("Select", "Nam", "Nữ", "Khác"),
                               state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_sex.place(x=150, y=330, width=200)
        cmb_sex.current(0)

        txt_cccd = Entry(Rec_frame, textvariable=self.var_r_cccd, font=("times new roman", 15), bg='#99d8c9').place(x=150, y=380, width=200)
        
        cmb_work = ttk.Combobox(Rec_frame, textvariable=self.var_r_workplace, values=("Select", "Sales agent", "Billing staff", "Protect"),
                                state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_work.place(x=150, y=430, width=200)
        cmb_work.current(0)

        btn_register = Button(Rec_frame, text="Register", command=self.register, font=("times new roman", 15),
                              bg="#2196f3", fg="white", cursor="hand2").place(x=70, y=500, width=120, height=30)
        btn_clear = Button(Rec_frame, text="Clear", command=self.clear, font=("times new roman", 15),
                           bg="#4caf50", fg="white", cursor="hand2").place(x=200, y=500, width=120, height=30)

    def register(self):
        con = sqlite3.connect(database=r'fms.db')
        cur = con.cursor()
        try:
            # Kiểm tra nếu có trường nào chưa được điền
            if (self.var_r_workplace.get() == "Select" or self.var_r_sex.get() == "Select" or
                    self.var_r_cccd.get() == "" or self.var_r_email.get() == ""):
                messagebox.showerror("Error", "Tất cả các trường đều phải được điền", parent=self.root)
            else:
                cur.execute("INSERT INTO recruitment (name, email, address, contact, date, sex, cccd, workplace) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (self.var_r_name.get(), self.var_r_email.get(), self.var_r_address.get(), self.var_r_contact.get(),
                             self.var_r_date.get(), self.var_r_sex.get(), self.var_r_cccd.get(), self.var_r_workplace.get()))
                con.commit()
                messagebox.showinfo("Success", "Bạn đã đăng kí thành công", parent=self.root)
                self.clear()  # Xóa thông tin sau khi đăng ký thành công
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_r_name.set("")
        self.var_r_email.set("")
        self.var_r_address.set("")
        self.var_r_contact.set("")
        self.var_r_date.set("")
        self.var_r_sex.set("Select")
        self.var_r_cccd.set("")
        self.var_r_workplace.set("Select")

    def back(self):
        self.root.destroy()
        os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = recruitmentClass(root)
    root.mainloop()
