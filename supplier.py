from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class supplierClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1150x500+220+130")
        self.root.title("Fashion Management System | Developed By DuyKhanh")
        self.root.config(bg="white")
        self.root.focus_force()

# bg= màu nền / fg= màu chữ / anchor= căn lề / padx= khoảng cách đệm / relief= kiểu viền / orient= xác định hướng thanh cuộn / bd= độ dày viền 
# / relwidth= thiết lập chiều rộng đối tượng / state= thiết lập trạng thái hoạt động của widget / current thiết lập giá trị mặc định 
# / append thêm một phần tử vào cuối danh sách / commit xác nhận các thay đổi đã thực hiện

        #_________________
        #All Variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        
        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()


        #_____searchFrame_____
        #_____options_____
        lbl_search=Label(self.root,text="Mã NCC",bg="white",font=("times new roman",15))
        lbl_search.place(x=700,y=80)

        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("times new roman",15),bg="#99d8c9").place(x=800,y=80,width=160)
        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=970,y=79,width=100,height=28)

        #_____title_____
        title=Label(self.root,text="Supplier Details",font=("times new roman",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1050,height=40)

        #_____content_____
        #_____row1_____
        lbl_supplier_invoice=Label(self.root,text="Mã NCC",font=("times new roman",15),bg="white").place(x=70,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("times new roman",15),bg="#99d8c9").place(x=170,y=80,width=180)
        
        #_____row2_____
        lbl_name=Label(self.root,text="Tên",font=("times new roman",15),bg="white").place(x=70,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("times new roman",15),bg="#99d8c9").place(x=170,y=120,width=180)
        
        #_____row3_____
        lbl_contact=Label(self.root,text="Liên hệ",font=("times new roman",15),bg="white").place(x=70,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("times new roman",15),bg="#99d8c9").place(x=170,y=160,width=180)


        #_____row4_____
        lbl_desc=Label(self.root,text="Mô tả",font=("times new roman",15),bg="white").place(x=70,y=200)
        self.txt_desc=Text(self.root,font=("times new roman",15),bg="#99d8c9")
        self.txt_desc.place(x=170,y=200,width=470,height=120)
                
        #_____buttons_____
        btn_add=Button(self.root,text="Save",command=self.add,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2").place(x=170,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=290,y=370,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("times new roman",15),bg="#f44336",fg="white",cursor="hand2").place(x=410,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15),bg="#607d8b",fg="white",cursor="hand2").place(x=530,y=370,width=110,height=35)

        #_____Employee Details_____

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=370,height=350)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)


        self.supplierTable.heading("invoice",text="Mã NCC")
        self.supplierTable.heading("name",text="Tên")
        self.supplierTable.heading("contact",text="Liên hệ")
        self.supplierTable.heading("desc",text="Mô tả")
        self.supplierTable["show"]="headings"
        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)


        self.show()

    #___________________________________________________________________
    def add(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Mã NCC là bắt buộc",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error","Mã NCC không hợp lệ, vui lòng thử lại",parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                                        self.var_sup_invoice.get(),
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Thêm NNC thành công",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def show(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        #print(row)
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])



    def update(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Mã NNC là bắt buộc",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Mã NCC không hợp lệ",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0',END),
                                        self.var_sup_invoice.get(),
                                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Thay đổi NCC thành công",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()


    def delete(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Mã NNC là bắt buộc",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Mã NCC không hợp lệ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Bạn thực sự muốn xóa?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Xóa NCC thành công.",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()
    
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Bạn cần phải nhập NCC",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Không tìm thấy hồ sơ!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__=="__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()