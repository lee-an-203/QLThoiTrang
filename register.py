import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk 

class registerClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x700+0+0")
        self.root.title("Fashion Management System | Developed By DuyKhanh")
        self.root.config(bg="white")

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
        self.var_searchby = StringVar()  # Thêm biến tìm kiếm
        self.var_searchtxt = StringVar()  # Thêm biến cho text tìm kiếm

        # Title
        title = Label(self.root, text="Recruitment Management System", font=("times new roman", 40, "bold"),
                      bg="#010c48", fg="white", anchor="center", padx=20).place(x=0, y=0, relwidth=1, height=70)
        

        self.img_Statistical = Image.open("images/logo_statistical.jpg")
        self.img_Statistical = self.img_Statistical.resize((250, 80), Image.LANCZOS)
        self.img_Statistical = ImageTk.PhotoImage(self.img_Statistical)
        left_img_label = Label(self.root, image=self.img_Statistical, bd=0)
        left_img_label.place(x=80, y=130)

        #_____searchFrame_____
        SearchFrame = LabelFrame(self.root, text="Search Statistical", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=350, y=130, width=600, height=70)

        #_____options_____
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="#99d8c9")
        txt_search.place(x=200, y=10)

        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("times new roman", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_search.place(x=430, y=8, width=150, height=30)

        # Frame for Treeview
        r_frame = Frame(self.root, bd=3, relief=RIDGE)
        r_frame.place(x=80, y=230, width=870, height=400)

        scrolly = Scrollbar(r_frame, orient=VERTICAL)
        scrollx = Scrollbar(r_frame, orient=HORIZONTAL)
        self.recFrame = ttk.Treeview(r_frame, columns=("rid", "name", "email", "address", "sex", "contact", "date", "cccd", "workplace"),
                                     yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.recFrame.xview)
        scrolly.config(command=self.recFrame.yview)

        self.recFrame.heading("rid", text="Mã ID")
        self.recFrame.heading("name", text="Tên")
        self.recFrame.heading("email", text="Email")
        self.recFrame.heading("address", text="Địa chỉ")
        self.recFrame.heading("sex", text="Giới tính")
        self.recFrame.heading("contact", text="Liên hệ")
        self.recFrame.heading("date", text="Ngày sinh")
        self.recFrame.heading("cccd", text="CCCD")
        self.recFrame.heading("workplace", text="Vị trí làm việc")
        self.recFrame["show"] = "headings"
        self.recFrame.column("rid", width=50)
        self.recFrame.column("name", width=130)
        self.recFrame.column("email", width=130)
        self.recFrame.column("address", width=130)
        self.recFrame.column("date", width=130)
        self.recFrame.column("sex", width=90)
        self.recFrame.column("contact", width=90)
        self.recFrame.column("cccd", width=130)
        self.recFrame.pack(fill=BOTH, expand=1)
        self.recFrame.bind("<ButtonRelease-1>", self.get_data)

        # Approve and Delete Buttons
        btn_approve = Button(self.root, text="Approve", command=self.approve_candidate, font=("times new roman", 15), bg="green", fg="white", cursor="hand2")
        btn_approve.place(x=235, y=650, width=120, height=30)
        btn_delete = Button(self.root, text="Delete", command=self.delete_candidate, font=("times new roman", 15), bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=435, y=650, width=120, height=30)
        btn_back = Button(self.root, text="Back", command=self.back, font=("times new roman", 15), bg="blue", fg="white", cursor="hand2")
        btn_back.place(x=635, y=650, width=120, height=30)
        
        self.show()

    def show(self):
        con = sqlite3.connect(database=r'fms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM recruitment")
            rows = cur.fetchall()
            self.recFrame.delete(*self.recFrame.get_children())
            for row in rows:
                self.recFrame.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.recFrame.focus()
        content = self.recFrame.item(f)
        row = content['values']
        if row:
            self.var_r_id.set(row[0])
            self.var_r_name.set(row[1])
            self.var_r_email.set(row[2])
            self.var_r_address.set(row[3])
            self.var_r_contact.set(row[5])
            self.var_r_date.set(row[6])
            self.var_r_sex.set(row[4])
            self.var_r_cccd.set(row[7])
            self.var_r_workplace.set(row[8])

    def search(self):
        con = sqlite3.connect(database=r'fms.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select" or self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Vui lòng chọn tiêu chí và nhập nội dung tìm kiếm", parent=self.root)
                return

            query = f"SELECT * FROM recruitment WHERE {self.var_searchby.get().lower()} LIKE ?"
            cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))
            rows = cur.fetchall()
            self.recFrame.delete(*self.recFrame.get_children())
            for row in rows:
                self.recFrame.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi khi tìm kiếm: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def approve_candidate(self):
        if self.var_r_id.get() == "":
            messagebox.showerror("Error", "Vui lòng chọn một ứng viên để duyệt", parent=self.root)
            return

        con = sqlite3.connect(database=r'fms.db')
        cur = con.cursor()
        try:
            # Thêm thông tin ứng viên vào bảng employee
            cur.execute("INSERT INTO employee (name, email, gender, contact, dob, doj, pass, utype, address, salary) VALUES (?, ?, ?, ?, ?, date('now'), '1', 'employee', ?, '3000')",
                        (self.var_r_name.get(), self.var_r_email.get(), self.var_r_sex.get(),
                         self.var_r_contact.get(), self.var_r_date.get(), self.var_r_address.get()))
            con.commit()
            messagebox.showinfo("Approved", "Ứng viên đã được duyệt và thêm vào danh sách nhân viên", parent=self.root)
            self.delete_candidate(confirmation=False)  # Xóa ứng viên sau khi duyệt mà không hiển thị thông báo xóa
        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi khi duyệt ứng viên: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete_candidate(self, confirmation=True):
        if self.var_r_id.get() == "":
            messagebox.showerror("Error", "Vui lòng chọn một ứng viên để xóa", parent=self.root)
            return

        if confirmation and not messagebox.askyesno("Confirm", "Bạn có chắc chắn muốn xóa ứng viên này?", parent=self.root):
            return

        con = sqlite3.connect(database=r'fms.db')
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM recruitment WHERE rid = ?", (self.var_r_id.get(),))
            con.commit()
            self.clear_fields()
            messagebox.showinfo("Deleted", "Ứng viên đã được xóa thành công", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi khi xóa ứng viên: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear_fields(self):
        self.var_r_id.set("")
        self.var_r_name.set("")
        self.var_r_email.set("")
        self.var_r_address.set("")
        self.var_r_contact.set("")
        self.var_r_sex.set("")
        self.var_r_date.set("")
        self.var_r_cccd.set("")
        self.var_r_workplace.set("")

    def back(self):
        self.root.destroy()
        os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = registerClass(root)
    root.mainloop()
