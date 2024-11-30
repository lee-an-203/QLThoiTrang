from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import os 
class salesClass:
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
        self.bill_list=[]
        self.var_invoice=StringVar()

        #_____title_____
        
        lbl_title=Label(self.root,text="View Customer Bills",font=("times new roman",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_invoice=Label(self.root,text="Invoice No.",font=("times new roman",15),bg="white").place(x=50,y=100)
        
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="#99d8c9").place(x=160,y=100,width=180,height=28)

        #_____Buttons_____
        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=490,y=100,width=120,height=28)

        #_____Bill List_____
        salesFrame=Frame(self.root,bd=3,relief=RIDGE)
        salesFrame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(salesFrame,orient=VERTICAL)
        self.sales_List=Listbox(salesFrame,font=("times new roman",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_List.yview)
        self.sales_List.pack(fill=BOTH,expand=1)
        self.sales_List.bind("<ButtonRelease-1>",self.get_data)

        #_____Bill Area_____
        billFrame=Frame(self.root,bd=3,relief=RIDGE)
        billFrame.place(x=280,y=140,width=410,height=330)

        lbl_title_two=Label(billFrame,text="Customer Bill Area",font=("times new roman",20),bg="orange").pack(side=TOP,fill=X)

        scrolly_two=Scrollbar(billFrame,orient=VERTICAL)
        self.bill_Area=Text(billFrame,bg="#99d8c9",yscrollcommand=scrolly_two.set)
        scrolly_two.pack(side=RIGHT,fill=Y)
        scrolly_two.config(command=self.bill_Area.yview)
        self.bill_Area.pack(fill=BOTH,expand=1)

        #_____Images_____
        self.bill_Photo=Image.open("images/cat2.jpg")
        self.bill_Photo=self.bill_Photo.resize((450,300),Image.LANCZOS)
        self.bill_Photo=ImageTk.PhotoImage(self.bill_Photo)
        
        lbl_image=Label(self.root,image=self.bill_Photo,bd=0)
        lbl_image.place(x=700,y=110)

        self.show()
#_____________________________________________________________

    def show(self):
        del self.bill_list[:]
        self.sales_List.delete(0,END)
        # print(os.listdir('../FMS'))
        for i in os.listdir('bill'):
            # print(i.split('.'),i.split('.')[-1])
            if i.split('.')[-1]=='txt':
                self.sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    

    def get_data(self, ev):
        try:
            index_ = self.sales_List.curselection()
            if not index_:
                return  # Nếu không có mục nào được chọn, thoát phương thức
            
            file_Name = self.sales_List.get(index_)
            # print(file_Name)
            self.bill_Area.delete('1.0', END)
            
            # Mở tệp với mã hóa utf-8
            with open(f'bill/{file_Name}', 'r', encoding='utf-8') as fp:
                for i in fp:
                    self.bill_Area.insert(END, i)
        except UnicodeDecodeError as e:
            messagebox.showerror("Error", f"Unicode Decode Error: {str(e)}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Không tìm thấy hóa đơn, vui lòng nhập hóa đơn", parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                # print("yes find the invoice")
                try:
                    with open(f'bill/{self.var_invoice.get()}.txt', 'r', encoding='utf-8') as fp:
                        self.bill_Area.delete('1.0', END)
                        for i in fp:
                            self.bill_Area.insert(END, i)
                except UnicodeDecodeError as e:
                    messagebox.showerror("Error", f"Unicode Decode Error: {str(e)}", parent=self.root)
                except Exception as ex:
                    messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
            else:
                messagebox.showerror("Error", "Hóa đơn không hợp lệ!!!", parent=self.root)


    def clear(self):
        self.show()
        self.bill_Area.delete('1.0',END)
        self.var_invoice.set("")

if __name__=="__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()