from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class productClass:
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
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()


        productFrame=Frame(self.root,bd=3,relief=RIDGE)
        productFrame.place(x=10,y=10,width=450,height=480)

        #_____title_____
        title=Label(productFrame,text="Manage Product Details",font=("times new roman",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        
        #_____Column1
        lbl_category=Label(productFrame,text="Loại",font=("times new roman",18),).place(x=30,y=60)
        lbl_supplier=Label(productFrame,text="NCC",font=("times new roman",18),).place(x=30,y=110)
        lbl_product_name=Label(productFrame,text="Tên",font=("times new roman",18),).place(x=30,y=160)
        lbl_price=Label(productFrame,text="Giá",font=("times new roman",18),).place(x=30,y=210)
        lbl_qty=Label(productFrame,text="Số lượng",font=("times new roman",18),).place(x=30,y=260)
        lbl_status=Label(productFrame,text="Trạng thái",font=("times new roman",18),).place(x=30,y=310)


        #_____Column2_____
        cmb_cat=ttk.Combobox(productFrame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(productFrame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)

        txt_name=Entry(productFrame,textvariable=self.var_name,font=("times new roman",15),bg='#99d8c9').place(x=150,y=160,width=200)
        txt_price=Entry(productFrame,textvariable=self.var_price,font=("times new roman",15),bg='#99d8c9').place(x=150,y=210,width=200)
        txt_qty=Entry(productFrame,textvariable=self.var_qty,font=("times new roman",15),bg='#99d8c9').place(x=150,y=260,width=200)


        cmb_status=ttk.Combobox(productFrame,textvariable=self.var_status,values=("Active","Inative"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)


        #_____buttons_____
        btn_add=Button(productFrame,text="Save",command=self.add,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(productFrame,text="Update",command=self.update,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(productFrame,text="Delete",command=self.delete,font=("times new roman",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(productFrame,text="Clear",command=self.clear,font=("times new roman",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

        #_____searchFrame_____
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("times new roman",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=500,y=10,width=600,height=80)

        #_____options_____
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("times new roman",15),bg="#99d8c9").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=430,y=8,width=150,height=30)


        #_____Product Details_____

        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=500,y=100,width=600,height=390)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.productFrame=ttk.Treeview(p_frame,columns=("pid","Supplier","Category","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productFrame.xview)
        scrolly.config(command=self.productFrame.yview)


        self.productFrame.heading("pid",text="Mã ID")
        self.productFrame.heading("Category",text="Loại")
        self.productFrame.heading("Supplier",text="NCC")
        self.productFrame.heading("name",text="Tên")
        self.productFrame.heading("price",text="Giá")
        self.productFrame.heading("qty",text="Số lượng")
        self.productFrame.heading("status",text="Trạng thái")

        self.productFrame["show"]="headings"

        self.productFrame.column("pid",width=90)
        self.productFrame.column("Category",width=100)
        self.productFrame.column("Supplier",width=100)
        self.productFrame.column("name",width=100)
        self.productFrame.column("price",width=100)
        self.productFrame.column("qty",width=100)
        self.productFrame.column("status",width=150)
        self.productFrame.pack(fill=BOTH,expand=1)
        self.productFrame.bind("<ButtonRelease-1>",self.get_data)

        self.show()

#________________________________________________________________
    

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def add(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","Tất cả các trường đều phải được điền",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error","Sản phẩm đã tồn tại, hãy thử với sản phẩm khác",parent=self.root)
                else:
                    cur.execute("Insert into product (Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Thêm sản phẩm thành công",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def show(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from product")
            rows=cur.fetchall()
            self.productFrame.delete(*self.productFrame.get_children())
            for row in rows:
                self.productFrame.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def get_data(self,ev):
        f=self.productFrame.focus()
        content=(self.productFrame.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_sup.set(row[1])
        self.var_cat.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])



    def update(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Vui lòng chọn sản phẩm từ danh sách",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Sản phẩm không hợp lệ",parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Cập nhật sản phẩm thành công",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()


    def delete(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Chọn sản phẩm từ danh sách",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Bạn có thực sự muốn xóa?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Xóa sản phẩm thành công",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()
    
    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Chọn chức năng tìm kiếm",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Không tìm thấy sản phẩm, vui lòng nhập sản phẩm",parent=self.root)

            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.productFrame.delete(*self.productFrame.get_children())
                    for row in rows:
                        self.productFrame.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Sản phẩm không hợp lệ!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

if __name__=="__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()