from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class employeeClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1150x500+220+130")
        self.root.title("Fashion Management System | Developed By DuyKhanh")
        self.root.config(bg="white")
        self.root.focus_force()  # Đảm bảo cửa sổ chính nhận được tiêu điểm
        #_________________ 
        
# bg= màu nền / fg= màu chữ / anchor= căn lề / padx= khoảng cách đệm / relief= kiểu viền / orient= xác định hướng thanh cuộn / bd= độ dày viền 
# / relwidth= thiết lập chiều rộng đối tượng / state= thiết lập trạng thái hoạt động của widget / current thiết lập giá trị mặc định 
# / append thêm một phần tử vào cuối danh sách / commit xác nhận các thay đổi đã thực hiện

        #All Variables: khai báo biến
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        
        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        #_____searchFrame_____
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("times new roman",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #_____options_____
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Email","Name","Contact"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("times new roman",15),bg="#99d8c9").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=430,y=8,width=150,height=30)

        #_____title_____
        title=Label(self.root,text="Employee Details",font=("times new roman",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1050)

        #_____content_____
        #_____row1_____
        lbl_empid=Label(self.root,text="Emp ID",font=("times new roman",15),bg="white").place(x=70,y=150)
        lbl_gender=Label(self.root,text="Giới tính",font=("times new roman",15),bg="white").place(x=390,y=150)
        lbl_contact=Label(self.root,text="Liên hệ",font=("times new roman",15),bg="white").place(x=750,y=150)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("times new roman",15),bg="#99d8c9").place(x=170,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Nam","Nữ","Khác"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("times new roman",15),bg="#99d8c9").place(x=850,y=150,width=180)

        #_____row2_____
        lbl_name=Label(self.root,text="Name",font=("times new roman",15),bg="white").place(x=70,y=190)
        lbl_dob=Label(self.root,text="Date",font=("times new roman",15),bg="white").place(x=390,y=190)
        lbl_doj=Label(self.root,text="Join Date",font=("times new roman",15),bg="white").place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("times new roman",15),bg="#99d8c9").place(x=170,y=190,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("times new roman",15),bg="#99d8c9").place(x=500,y=190,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("times new roman",15),bg="#99d8c9").place(x=850,y=190,width=180)

        #_____row3_____
        lbl_email=Label(self.root,text="Email",font=("times new roman",15),bg="white").place(x=70,y=230)
        lbl_pass=Label(self.root,text="Password",font=("times new roman",15),bg="white").place(x=390,y=230)
        lbl_utype=Label(self.root,text="Quyền",font=("times new roman",15),bg="white").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("times new roman",15),bg="#99d8c9").place(x=170,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("times new roman",15),bg="#99d8c9").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin","Employee"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #_____row4_____
        lbl_address=Label(self.root,text="Address",font=("times new roman",15),bg="white").place(x=70,y=270)
        lbl_salary=Label(self.root,text="Lương",font=("times new roman",15),bg="white").place(x=500,y=270)

        self.txt_address=Text(self.root,font=("times new roman",15),bg="#99d8c9")
        self.txt_address.place(x=170,y=270,width=300,height=60)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("times new roman",15),bg="#99d8c9").place(x=600,y=270,width=180)
        
        #_____buttons_____
        btn_add=Button(self.root,text="Save",command=self.add,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("times new roman",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

        #_____Employee Details_____

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid",text="Emp ID")
        self.EmployeeTable.heading("name",text="Name")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("gender",text="Giới tính")
        self.EmployeeTable.heading("contact",text="Liên hệ")
        self.EmployeeTable.heading("dob",text="Date")
        self.EmployeeTable.heading("doj",text="join Date")
        self.EmployeeTable.heading("pass",text="Password")
        self.EmployeeTable.heading("utype",text="Quyền")
        self.EmployeeTable.heading("address",text="Address")
        self.EmployeeTable.heading("salary",text="Lương")

        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("address",width=150)
        self.EmployeeTable.column("salary",width=100)
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

    #___________________________________________________________________
    def add(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Mã người dùng là bắt buộc",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error","Mã người dùng này đã được sử dụng, vui lòng thử mã khác",parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                        self.var_emp_id.get(),
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),
                                        self.var_dob.get(),
                                        self.var_doj.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                                        self.var_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Thêm người dùng thành công",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def show(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        #print(row)
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])

    def update(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Mã người dùng là bắt buộc",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Mã người dùng không hợp lệ",parent=self.root)
                else:
                    cur.execute("Update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),
                                        self.var_dob.get(),
                                        self.var_doj.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                                        self.var_salary.get(),
                                        self.var_emp_id.get(),
                                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success","cập nhật người dùng thành công",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def delete(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Mã người dùng là bắt buộc",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Mã người dùng không hợp lệ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Bạn thực sự muốn xóa?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Xóa người dùng thành công",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()
    
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Chọn chức năng",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Cần phải có đầu vào tìm kiếm",parent=self.root)

            else:
                cur.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Không tìm thấy người dùng!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

if __name__=="__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()