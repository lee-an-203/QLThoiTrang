from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from billing import BillClass
from statistical import statisticalClass
import sqlite3
from tkinter import messagebox
import os
import time
class FMS:
# bg= màu nền / fg= màu chữ / anchor= căn lề / padx= khoảng cách đệm / relief= kiểu viền / orient= xác định hướng thanh cuộn / bd= độ dày viền 
# / relwidth= thiết lập chiều rộng đối tượng / state= thiết lập trạng thái hoạt động của widget / current thiết lập giá trị mặc định 
# / append thêm một phần tử vào cuối danh sách / commit xác nhận các thay đổi đã thực hiện
    def __init__(self,root):
        self.root = root
        self.root.geometry("1370x700+0+0") #kích thước
        self.root.title("Fashion Management System | Developed By DuyKhanh") #itêu đề
        self.root.config(bg="white") #nền
        #______title______ 
        # # bg= màu nền / fg= màu chữ / anchor= căn lề / padx= khoảng cách đệm / relief= kiểu viền / orient= xác định hướng thanh cuộn
        self.icon_title=PhotoImage(file="images/logo1.png")
        title = Label(self.root,text="Fashion Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #______btn_logout______
        btn_statistical=Button(self.root,text="Statistical",command=self.statistical,font=("times new roman",15,"bold"),bg="#33bbf9",cursor="hand2").place(x=860,y=10,height=50,width=150)
        btn_rec=Button(self.root,text="Register",command=self.register,font=("times new roman",15,"bold"),bg="#33bbf9",cursor="hand2").place(x=1020,y=10,height=50,width=150)
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="#33bbf9",cursor="hand2").place(x=1180,y=10,height=50,width=150)

        #______Clock______
        self.lbl_clock= Label(self.root,text="Welcome To Fashion Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        #______Left Menu______
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side.png")
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)

        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_payment=Button(LeftMenu,text="Payment",command=self.billing,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #______content______

        self.lbl_employee=Label(self.root,text="Total Employee\n[ 0 ]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier\n[ 0 ]",bd=5,relief=RIDGE,bg="#8856a7",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)
        
        self.lbl_category=Label(self.root,text="Total Category\n[ 0 ]",bd=5,relief=RIDGE,bg="#fec44f",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)
        
        self.lbl_product=Label(self.root,text="Total Product\n[ 0 ]",bd=5,relief=RIDGE,bg="#fc9272",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n[ 0 ]",bd=5,relief=RIDGE,bg="#f03b20",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        self.lbl_register=Label(self.root,text="Total Register\n[ 0 ]",bd=5,relief=RIDGE,bg="#d95f0e",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_register.place(x=300,y=480,height=150,width=300)


        #______footer______
        lbl_footer=Label(self.root,text="FMS-Fashion Management System | Developed By DuyKhanh\n For any Technical Issue Contact: 0329010567",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
#_________________________________________________________________
# Mở các cửa sổ cho từng module riêng biệt
    def employee(self):   
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):   
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):   
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self):   
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):   
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)
    
    def billing(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=BillClass(self.new_win)

    def statistical(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=statisticalClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Product\n[{str(len(product))}]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total Employee\n[{str(len(employee))}]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total Category\n[{str(len(category))}]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Supplier\n[{str(len(supplier))}]')
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales\n[{str(bill)}]')

            cur.execute("select * from recruitment")
            recruitment=cur.fetchall()
            self.lbl_register.config(text=f'Total Recruitment\n[{str(len(recruitment))}]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome To Fashion Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}",font=("times new roman",15),bg="#4d636d",fg="white")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    # def payment(self):
    #     os.system("python billing.py")

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def register(self):
        self.root.destroy()
        os.system("python register.py")

    def statistical(self):
        self.root.destroy()
        os.system("python statistical.py")

if __name__=="__main__":
    root = Tk()
    obj = FMS(root)
    root.mainloop()