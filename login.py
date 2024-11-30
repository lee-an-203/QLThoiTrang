from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time
class Login_System:
    def __init__(self,root):
        self.root = root
        self.root.geometry("970x700+0+0")
        self.root.title("Fashion Management System | Developed By DuyKhanh")
        self.root.config(bg="#fafafa")

        self.otp=''
# bg= màu nền / fg= màu chữ / anchor= căn lề / padx= khoảng cách đệm / relief= kiểu viền / orient= xác định hướng thanh cuộn / bd= độ dày viền 
# / relwidth= thiết lập chiều rộng đối tượng / state= thiết lập trạng thái hoạt động của widget / current thiết lập giá trị mặc định 
# / append thêm một phần tử vào cuối danh sách / commit xác nhận các thay đổi đã thực hiện


        # #_____Images_____
        # self.phone_image=ImageTk.PhotoImage(file="images/im3.png")
        # self.lbl_Phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)

        #_____Login_Frame_____
        self.employ_id=StringVar()
        self.password=StringVar()
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=400,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("times new roman",30,"bold"),bg="white").place(x=0,y=30,width=340)

        lbl_user=Label(login_frame,text="Employee ID",font=("times new roman",15),bg="white",fg="#767171").place(x=15,y=100,width=220)
        txt_username=Entry(login_frame,textvariable=self.employ_id,font=("times new roman",15),bg="#E0E0E0").place(x=73,y=135,width=200,height=25)

        lbl_pass=Label(login_frame,text="Password",font=("times new roman",15),bg="white",fg="#767171").place(x=0,y=190,width=220)
        txt_pass=Entry(login_frame,textvariable=self.password,font=("times new roman",15),bg="#E0E0E0",show="$").place(x=73,y=225,width=200,height=25)

        btn_login=Button(login_frame,text="Log In",command=self.login,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2").place(x=73,y=290,width=200,height=30)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold")).place(x=160,y=355)

        btn_forget=Button(login_frame,text="Quên mật khẩu?",command=self.forget_window,font=("times new roman",13),bg="white",fg="#2196f3",cursor="hand2",bd=0).place(x=73,y=390,width=200,height=30)

        #_____Frame_Two_____
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=400,y=570,width=350,height=60)

        lbl_reg=Label(register_frame,text="Bạn chưa có tài khoản?",font=("times new roman",13),bg="white",fg="#767171").place(x=0,y=17,width=220)
        btn_signup=Button(register_frame,text="Sign Up",command=self.register,font=("times new roman",13),bg="white",fg="#0080FF",cursor="hand2",bd=0).place(x=190,y=16,width=70,height=30)


        #_________Animation Images_________
        self.imOne=ImageTk.PhotoImage(file="images/im1.png")
        self.imTwo=ImageTk.PhotoImage(file="images/im2.png")
        self.imThree=ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=130,y=103,width=240,height=428)

        self.animate()

    #_______________________All Functions______________________
     # Quá trình thay đổi hình ảnh
    def animate(self):
        self.im=self.imOne
        self.imOne=self.imTwo
        self.imTwo=self.imThree
        self.imThree=self.im
        self.lbl_change_image.config(image=self.imThree)# Cập nhật hình ảnh trên Label
        self.lbl_change_image.after(2000,self.animate)# Lập lịch gọi lại animate sau 2 giây

    def login(self):
            con=sqlite3.connect(database=r'fms.db')
            cur=con.cursor()
            try:
                if self.employ_id.get()=="" or self.password.get()=="":
                     messagebox.showerror('Error',"Tất cả các trường phải được điền",parent=self.root)
                else:
                    cur.execute("select utype from employee where eid=? AND pass=?",(self.employ_id.get(),self.password.get()))
                    user=cur.fetchone()
                    if user==None:
                        messagebox.showerror('Error',"Tên đăng nhập hoặc mật khẩu không hợp lệ",parent=self.root)
                    else:
                        print(user)
                        if user[0]=="Admin":
                            self.root.destroy()
                            os.system("python dashboard.py")
                        else:
                            self.root.destroy()
                            os.system("python billing.py")
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            finally:
                con.close()

    def forget_window(self):
        con=sqlite3.connect(database=r'fms.db')
        cur=con.cursor()
        try:
            if self.employ_id.get()=="":
                messagebox.showerror('Error',"Mã người dùng là bắt buộc",parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.employ_id.get(),))
                email=cur.fetchone()
                if email is None:
                    messagebox.showerror('Error',"Mã người dùng không hợp lệ, hãy thử lại",parent=self.root)
                else:
                    # __________Forget Window___________
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_confirm_pass=StringVar()
                    chk=self.send_email(email[0]) #dybkhv@gmail.com

                    self.forget_win=Toplevel(self.root)
                    self.forget_win.title('Reset Password')
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()
                    if chk=='f':
                        messagebox.showerror("Error","Lỗi kết nối, hãy thử lại",parent=self.root)
                    else:
                        title=Label(self.forget_win,text='Reset Password',font=('times new roman',15,'bold'),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Nhập OTP được gửi qua email đã đăng ký",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg='lightyellow').place(x=20,y=100,width=250,height=30)
                        
                        self.btn_reset=Button(self.forget_win,text="Submit",command=self.validate_otp,font=("times news roman",15),bg='lightblue')
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg='lightyellow',show="$").place(x=20,y=190,width=250,height=30)
                        
                        lbl_c_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=225)
                        txt_c_pass=Entry(self.forget_win,textvariable=self.var_confirm_pass,font=("times new roman",15),bg='lightyellow',show="$").place(x=20,y=255,width=250,height=30)
                        
                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state=DISABLED,font=("times news roman",15),bg='lightblue')
                        self.btn_update.place(x=150,y=300,width=100,height=30) 
        except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        finally:
                con.close()

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_confirm_pass.get()=="":
            messagebox.showerror("Error","Mật khẩu là bắt buộc",parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_confirm_pass.get():
            messagebox.showerror("Error","New Password & Confirm Password phải giống nhau",parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r'fms.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employ_id.get()))
                con.commit()
                messagebox.showinfo("Success","Đổi mật khẩu thành công",parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            finally:
                con.close()



    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
            messagebox.showinfo("Success", "OTP đã được xác minh. Vui lòng đặt lại mật khẩu của bạn.", parent=self.forget_win)
        else:
            messagebox.showerror("Error","OTP không hợp lệ, vui lòng thử lại.",parent=self.forget_win)


    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)#Thiết lập kết nối đến máy chủ SMTP của Gmail trên cổng 587.
        s.starttls()# Bảo mật kết nối bằng cách sử dụng TLS.
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)#Đăng nhập vào tài khoản Gmail sử dụng địa chỉ email và mật khẩu đã cung cấp.

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))# tạo mã OTP bằng thời gian
        
        subj='FMS-Reset Password OTP'
        msg=f'Gui Ong/Ba,\n\nMa OTP thiet lap lai cua ban la {str(self.otp)}.\n\n Voi DuyKhanh,\nFMS Team'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg) #Gửi email từ địa chỉ email_ đến địa chỉ to_ với nội dung là msg.
        chk=s.ehlo() #để kiểm tra mã trạng thái 250, đại diện cho thành công khi gửi email.
        if chk[0]==250:
             return 's'
        else:
             return 'f'

    def register(self):
        self.root.destroy()
        os.system("python recruitment.py")
        
root = Tk()
obj = Login_System(root)
root.mainloop()