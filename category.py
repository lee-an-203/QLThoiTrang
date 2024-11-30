from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1150x500+220+130")
        self.root.title("Fashion Management System | Developed By DuyKhanh")
        self.root.config(bg="white")
        self.root.focus_force()
        #_____Variables_____ 
# bg= màu nền / fg= màu chữ / anchor= căn lề / padx= khoảng cách đệm / relief= kiểu viền / orient= xác định hướng thanh cuộn / bd= độ dày viền 
# / relwidth= thiết lập chiều rộng đối tượng / state= thiết lập trạng thái hoạt động của widget / current thiết lập giá trị mặc định 
# / append thêm một phần tử vào cuối danh sách / commit xác nhận các thay đổi đã thực hiện'

        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        #_____title_____
        lbl_title=Label(self.root,text="Manage Product Category",font=("times new roman",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_name=Label(self.root,text="Enter Category Name",font=("times new roman",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("times new roman",18),bg="#99d8c9").place(x=50,y=170,width=300)

        #_____Buttons_____
        btn_add=Button(self.root,text="ADD",command=self.add,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("times new roman",15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

        #_____Category Details_____

        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=730,y=110,width=375,height=90)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.categoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)


        self.categoryTable.heading("cid",text="Cate ID")
        self.categoryTable.heading("name",text="Name")
        self.categoryTable["show"]="headings"
        self.categoryTable.column("cid",width=90)
        self.categoryTable.column("name",width=100)
        self.categoryTable.pack(fill=BOTH,expand=1)
        self.categoryTable.bind("<ButtonRelease-1>",self.get_data) # được sử dụng để liên kết sự kiện "ButtonRelease-1

        #-----images-----
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((500,260),Image.LANCZOS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=600,y=220)


        self.im2=Image.open("images/category.jpg")
        self.im2=self.im2.resize((500,260),Image.LANCZOS)
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=50,y=220)

        self.show()

    #______________________Functions_____________________

    def add(self):
            con=sqlite3.connect(database=r'fms.db')
            cur=con.cursor() # Tạo đối tượng con trỏ
            try:
                if self.var_name.get()=="":
                    messagebox.showerror("Error","Tên loại SP là bắt buộc",parent=self.root)
                else:
                    cur.execute("Select * from category where name=?",(self.var_name.get(),))
                    row=cur.fetchone() # lấy một dòng dữ liệu từ kết quả truy vấn.
                    if row is not None:
                        messagebox.showerror("Error","Loại SP đã tồn tại, vui lòng thử lại khác",parent=self.root)
                    else:
                        cur.execute("Insert into category (name) values(?)",(self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Đã thêm loại sản phẩm thành công",parent=self.root)
                        self.show()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            finally:
                con.close()


    def show(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall() # ấy tất cả các dòng dữ liệu từ kết quả truy vấn.
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def get_data(self,ev):
        f=self.categoryTable.focus() #để hiển thị danh sách các mục (items).
        content=(self.categoryTable.item(f)) # trả về thông tin chi tiết về mục được chọn
        row=content['values'] # trả về các giá trị (values) 
        #print(row)
        self.var_cat_id.set(row[0]) # gán giá trị và sử dụng cập nhật điều khiển giao diện
        self.var_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Vui lòng chọn loại sản phẩm từ danh sách",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Có lỗi xảy ra, vui lòng thử lại",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Bạn có thực sự muốn xóa không?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Đã xóa loại sản phẩm thành công",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()


    
if __name__=="__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()