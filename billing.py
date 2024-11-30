from datetime import datetime
from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile

class BillClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1370x700+0+0")
        self.root.title("Fashion Management System | Developed By DuyKhanh")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
# bg= màu nền / fg= màu chữ / anchor= căn lề / padx= khoảng cách đệm / relief= kiểu viền / orient= xác định hướng thanh cuộn / bd= độ dày viền 
# / relwidth= thiết lập chiều rộng đối tượng / state= thiết lập trạng thái hoạt động của widget / current thiết lập giá trị mặc định 
# / append thêm một phần tử vào cuối danh sách / commit xác nhận các thay đổi đã thực hiện
        #______title______
        self.icon_title=PhotoImage(file="images/logo1.png")
        title = Label(self.root,text="Fashion Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #______btn_logout______
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1180,y=10,height=50,width=150)

        #______Clock______
        self.lbl_clock= Label(self.root,text="Welcome To Fashion Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #_____Product_Frame_____

        ProductFrame_one=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame_one.place(x=10,y=110,width=410,height=550)

        pTitle=Label(ProductFrame_one,text="All Products",font=("times new roman",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        #_____Product_Search_Frame_____
        self.var_search=StringVar()
        ProductFrame_two=Frame(ProductFrame_one,bd=2,relief=RIDGE,bg="white")
        ProductFrame_two.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame_two,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        lbl_search=Label(ProductFrame_two,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame_two,textvariable=self.var_search,font=("times new roman",15),bg="#99d8c9").place(x=135,y=47,width=150,height=22)
        btn_search=Button(ProductFrame_two,text="Search",command=self.search,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2").place(x=290,y=45,width=90,height=24)
        btn_show_all=Button(ProductFrame_two,text="Show All",command=self.show,font=("times new roman",15),bg="#083531",fg="white",cursor="hand2").place(x=290,y=10,width=90,height=24)

        #_____Product_Details_Frame_____
        ProductFrame_three=Frame(ProductFrame_one,bd=3,relief=RIDGE)
        ProductFrame_three.place(x=2,y=140,width=398,height=400)

        scrolly=Scrollbar(ProductFrame_three,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame_three,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame_three,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)


        self.product_Table.heading("pid",text="ID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="Quantity")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=140)
        self.product_Table.column("price",width=70)
        self.product_Table.column("qty",width=60)
        self.product_Table.column("status",width=70)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)

        self.product_Table.pack(fill=BOTH,expand=1)
        lbl_note=Label(ProductFrame_three,text="Note: 'Enter 0 Quantity to remove product from the Cart'",font=("times new roman",11),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)

        
        #_____CustomerFrame_____
        self.var_c_name=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=423,y=110,width=530,height=74)

        cTitle=Label(CustomerFrame,text="Customer Details",font=("times new roman",15),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_c_name,font=("times new roman",13),bg="#99d8c9").place(x=65,y=35,width=180)
        
        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=260,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="#99d8c9").place(x=369,y=35,width=140)
        
        
        #_____Cal Cart Frame_____
        Cal_Cart_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=423,y=190,width=530,height=360)


        #_____calculator frame_____
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=3,y=10,width=268,height=340)


        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=("arial",15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)
        
        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=12,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=12,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=12,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=12,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=12,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=12,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=12,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=12,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=12,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=12,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=12,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=12,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=10,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=10,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=10,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=10,cursor="hand2").grid(row=4,column=3)

        #_____cart frame_____
        cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=275,y=8,width=245,height=343)
        self.cartTitle=Label(cart_Frame,text="Cart \t Total Product: [0]",font=("times new roman",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid",text="P ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Quantity")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=140)
        self.CartTable.column("price",width=70)
        self.CartTable.column("qty",width=60)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #_____ADD Cart Widgets Frame_____
        self.var_pid=StringVar()
        self.var_p_name=StringVar()
        self.var_p_price=StringVar()
        self.var_p_qty=StringVar()
        self.var_p_stock=StringVar()

        Add_CartWidgetsFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=423,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_p_name,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=210,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_p_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=210,y=35,width=150,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=375,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_p_qty,font=("times new roman",15),bg="#99d8c9").place(x=375,y=35,width=140,height=22)

        self.lbl_p_inStock=Label(Add_CartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_p_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=170,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=335,y=70,width=180,height=30)

        #__________billing area__________
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=955,y=110,width=410,height=410)

        bill_Title=Label(billFrame,text="Customer Bill Area",font=("times new roman",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #___________________Billing buttons___________________
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=955,y=520,width=410,height=140)

        self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=("times new roman",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=5,y=5,width=130,height=70)

        self.lbl_discount=Label(billMenuFrame,text='Discount\n[5%]',font=("times new roman",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=137,y=5,width=130,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text='Net Pay\n[0]',font=("times new roman",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=269,y=5,width=130,height=70)

        btn_print=Button(billMenuFrame,text='Print',command=self.print_bill,cursor='hand2',font=("times new roman",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=5,y=80,width=130,height=50)

        btn_clear=Button(billMenuFrame,text='Clear All',command=self.clear_all,cursor='hand2',font=("times new roman",15,"bold"),bg="gray",fg="white")
        btn_clear.place(x=137,y=80,width=130,height=50)

        btn_generate=Button(billMenuFrame,text='Save Bill',command=self.generate_bill,cursor='hand2',font=("times new roman",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=269,y=80,width=130,height=50)

        #______footer______
        lbl_footer=Label(self.root,text="FMS-Fashion Management System | Developed By DuyKhanh\n For any Technical Issue Contact: 0329010567",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.show()
        self.update_date_time()
    #____________________________ALl Functions______________________________
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
        # self.product_Table=ttk.Treeview(ProductFrame_three,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            cur.execute("Select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
            con.close()

    def search(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Cần phải có đầu vào tìm kiếm",parent=self.root)

            else:
                cur.execute("select pid,name,price,qty,status from product where name  LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Không tìm thấy sản phẩm!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_p_name.set(row[1])
        self.var_p_price.set(row[2])
        self.lbl_p_inStock.config(text=f"In Stock[{str(row[3])}]")
        self.var_p_stock.set(row[3])
        self.var_p_qty.set('1')

    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_p_name.set(row[1])
        self.var_p_price.set(row[2])
        self.var_p_qty.set(row[3])
        self.lbl_p_inStock.config(text=f"In Stock[{str(row[4])}]")
        self.var_p_stock.set(row[4])
        
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Vui lòng chọn sản phẩm từ danh sácht",parent=self.root)
        elif self.var_p_qty.get()=='':
            messagebox.showerror('Error',"Số lượng là bắt buộc",parent=self.root)
        elif int(self.var_p_qty.get())>int(self.var_p_stock.get()):
            messagebox.showerror('Error',"Số lượng không hợp lệ",parent=self.root)
        else:
            # price_cal=int(self.var_p_qty.get())*float(self.var_p_price.get())
            # price_cal=float(price_cal)
            price_cal=self.var_p_price.get()
            cart_data=[self.var_pid.get(),self.var_p_name.get(),price_cal,self.var_p_qty.get(),self.var_p_stock.get()]
    
            #_____Update-cart______
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Sản phẩm đã có trong giỏ hàng\nBạn có muốn Cập nhật|Xóa khỏi danh sách Giỏ hàng không",parent=self.root)
                if op==True:
                    if self.var_p_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3]=self.var_p_qty.get() #quantity
            else:    
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()
    
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))

        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def generate_bill(self):
        # Kiểm tra thông tin khách hàng và giỏ hàng
        if self.var_c_name.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", "Thông tin khách hàng là bắt buộc", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Vui lòng thêm sản phẩm vào Giỏ hàng!", parent=self.root)
        else:
            # Tạo hóa đơn
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()

            # Lưu hóa đơn vào bảng sales
            try:
                con = sqlite3.connect(database=r'fms.db')
                cur = con.cursor()
                sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for item in self.cart_list:
                    pid = item[0]
                    name = item[1]
                    quantity_sold = int(item[3])
                    price_paid = float(item[2]) * quantity_sold

                    # Lưu giao dịch vào bảng sales
                    cur.execute("""
                        INSERT INTO sales (product_id, product_name, quantity, price_paid, sale_date)
                        VALUES (?, ?, ?, ?, ?)
                    """, (pid, name, quantity_sold, price_paid, sale_date))
                    
                con.commit()
                con.close()
                messagebox.showinfo('Save', "Hóa đơn và giao dịch bán hàng đã được lưu", parent=self.root)
                self.chk_print = 1
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\t   Store DuyKhanh
\tSố điện thoại 0329010567 | Ha Dong, Ha Noi
{str("="*47)}
 Customer Name: {self.var_c_name.get()}
 Phone :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQuantity\t\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_middle(self):
        # Kết nối cơ sở dữ liệu
        con = sqlite3.connect(database=r'fms.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty_in_stock = int(row[4])
                qty_sold = int(row[3])
                qty_remaining = qty_in_stock - qty_sold

                # Cập nhật trạng thái tồn kho của sản phẩm
                status = 'Inactive' if qty_remaining == 0 else 'Active'
                price = float(row[2]) * qty_sold

                # Cập nhật thông tin sản phẩm vào hóa đơn
                self.txt_bill_area.insert(END, f"\n {name}\t\t\t{qty_sold}\tRs.{price:.2f}")

                # Cập nhật số lượng sản phẩm trong bảng product
                cur.execute('UPDATE product SET qty = ?, status = ? WHERE pid = ?', (qty_remaining, status, pid))
                con.commit()
            
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


            
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs. {self.bill_amnt}
 Discount\t\t\t\tRs. {self.discount}
 Net Pay\t\t\t\tRs. {self.net_pay}
{str("="*47)}\n
'''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_p_name.set('')
        self.var_p_price.set('')
        self.var_p_qty.set('')
        self.lbl_p_inStock.config(text=f"In Stock")
        self.var_p_stock.set('')
        
    def clear_all(self):
        del self.cart_list[:]
        self.var_c_name.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome To Fashion Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print', "Vui lòng đợi trong khi in", parent=self.root)
            # Tạo tệp tạm thời
            fd, path = tempfile.mkstemp(suffix='.txt')
            try:
                # Mở tệp tạm thời và ghi nội dung hóa đơn vào đó
                with open(fd, 'w', encoding='utf-8') as temp_file:
                    temp_file.write(self.txt_bill_area.get('1.0', END))
                # In tệp tạm thời
                os.startfile(path, 'print')
            except Exception as ex:
                messagebox.showerror("Error", f"Lỗi trong khi in: {str(ex)}", parent=self.root)
            finally:
                os.close(fd)
        else:
            messagebox.showerror('Print', "Vui lòng lưu hóa đơn trước khi in", parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()