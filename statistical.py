from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import ttk, messagebox
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import mplcursors
import pandas as pd

class statisticalClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x700+0+0")
        self.root.title("Fashion Management System | Developed By DuyKhanh")
        self.root.config(bg="white")

        # Title
        title2 = Label(self.root, text="Thống Kê", font=("times new roman", 20, "bold"), bg="#f44336", fg="white")
        title2.place(x=350, y=30, width=300, height=50)

        # Left Menu
        self.MenuLogo = Image.open("images/statistical.jpg").resize((200, 200), Image.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=545)
        
        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)
        
        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688")
        lbl_menu.pack(side=TOP, fill=X)

        # Buttons in Menu
        btn_doanhthu = Button(LeftMenu, text="Doanh Thu", command=self.show_revenue_chart, font=("times new roman", 20, "bold"), bg="#CC99CC", bd=5, cursor="hand2")
        btn_doanhthu.pack(side=TOP, fill=X)
        
        btn_hanghoa = Button(LeftMenu, text="Hàng Hóa", command=self.show_product_list, font=("times new roman", 20, "bold"), bg="#CC99CC", bd=5, cursor="hand2")
        btn_hanghoa.pack(side=TOP, fill=X)
        
        btn_tonkho = Button(LeftMenu, text="Tồn Kho", command=self.show_stock_list, font=("times new roman", 20, "bold"), bg="#CC99CC", bd=5, cursor="hand2")
        btn_tonkho.pack(side=TOP, fill=X)
        
        btn_refesh = Button(LeftMenu, text="Refesh", command=self.show_default_image, font=("times new roman", 20, "bold"), bg="#CC99CC", bd=5, cursor="hand2")
        btn_refesh.pack(side=TOP, fill=X)

        btn_back = Button(LeftMenu, text="Back", command=self.main, font=("times new roman", 20, "bold"), bg="#CC99CC", bd=5, cursor="hand2")
        btn_back.pack(side=TOP, fill=X)

        # Right Frame
        self.RightFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.RightFrame.place(x=205, y=102, width=820, height=485)
        
        # Default Image in Right Frame
        self.default_img = Image.open("images/statistical1.png").resize((755, 485), Image.LANCZOS)
        self.default_img = ImageTk.PhotoImage(self.default_img)
        self.lbl_img = Label(self.RightFrame, image=self.default_img)
        self.lbl_img.pack()

        # Button Excel

        btn_excel = Button(text="Excel", command=self.excel, font=("times new roman", 20, "bold"), bg="#00CCCC", bd=5, cursor="hand2")
        btn_excel.place(relx=0.6, rely=0.9, anchor=CENTER) 

    def show_default_image(self):
        for widget in self.RightFrame.winfo_children():
            widget.destroy()
        Label(self.RightFrame, image=self.default_img).pack()

    def show_revenue_chart(self):
        plt.close('all')
        for widget in self.RightFrame.winfo_children():
            widget.destroy()

        # Kết nối và truy vấn dữ liệu doanh thu theo ngày, tháng, năm
        con = sqlite3.connect("fms.db")
        cur = con.cursor()

        cur.execute("SELECT sale_date, SUM(quantity * price) FROM sales JOIN product ON sales.product_id = product.pid GROUP BY sale_date")
        daily_data = cur.fetchall()

        cur.execute("SELECT strftime('%Y-%m', sale_date), SUM(quantity * price) FROM sales JOIN product ON sales.product_id = product.pid GROUP BY strftime('%Y-%m', sale_date)")
        monthly_data = cur.fetchall()

        cur.execute("SELECT strftime('%Y', sale_date), SUM(quantity * price) FROM sales JOIN product ON sales.product_id = product.pid GROUP BY strftime('%Y', sale_date)")
        yearly_data = cur.fetchall()

        con.close()

        # Chuẩn bị dữ liệu để vẽ
        daily_dates, daily_revenue = zip(*daily_data)
        monthly_dates, monthly_revenue = zip(*monthly_data)
        yearly_dates, yearly_revenue = zip(*yearly_data)

        # Thiết lập biểu đồ
        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)

        # Vẽ biểu đồ
        daily_plot, = ax.plot(daily_dates, daily_revenue, '-o', color='blue', label="Doanh thu hàng ngày")
        monthly_plot, = ax.plot(monthly_dates, monthly_revenue, '-o', color='orange', label="Doanh thu hàng tháng")
        yearly_plot, = ax.plot(yearly_dates, yearly_revenue, '-o', color='green', label="Doanh thu hàng năm")

        ax.set_title("Doanh Thu Theo Ngày, Tháng, Năm")
        ax.set_xlabel("Thời gian")
        ax.set_ylabel("Doanh thu (VND)")
        ax.legend()

        # Định dạng trục Y thành đơn vị tiền tệ VND
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,} VND'))

        # Thêm chức năng chú thích khi di chuột qua các điểm dữ liệu
        cursor = mplcursors.cursor([daily_plot, monthly_plot, yearly_plot], hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f"{sel.artist.get_label()}\n{sel.target[0]}: {int(sel.target[1]):,} VND"))

        # Hiển thị biểu đồ trong tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.RightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    def show_product_list(self):
            for widget in self.RightFrame.winfo_children():
                widget.destroy()

            # Tạo thanh cuộn cho Treeview
            scroll_y = Scrollbar(self.RightFrame, orient=VERTICAL)
            scroll_x = Scrollbar(self.RightFrame, orient=HORIZONTAL)

            # Cấu hình Treeview với các cột và thanh cuộn
            tree = ttk.Treeview(self.RightFrame, columns=("pid", "supplier", "category", "name", "price", "qty", "status"), 
                                show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
            scroll_y.config(command=tree.yview)
            scroll_x.config(command=tree.xview)

            # Đặt thanh cuộn vào khung
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_x.pack(side=BOTTOM, fill=X)
            tree.pack(fill=BOTH, expand=True)

            # Kết nối cơ sở dữ liệu và hiển thị dữ liệu
            con = sqlite3.connect("fms.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            con.close()

            for col in tree["columns"]:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in rows:
                tree.insert("", END, values=row)

    def show_stock_list(self):
        for widget in self.RightFrame.winfo_children():
            widget.destroy()

        # Tạo thanh cuộn cho Treeview
        scroll_y = Scrollbar(self.RightFrame, orient=VERTICAL)
        scroll_x = Scrollbar(self.RightFrame, orient=HORIZONTAL)

        # Cấu hình Treeview với các cột và thanh cuộn
        tree = ttk.Treeview(self.RightFrame, columns=("name", "qty"), show="headings", 
                            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        # Đặt thanh cuộn vào khung
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        tree.pack(fill=BOTH, expand=True)

        # Kết nối cơ sở dữ liệu và hiển thị dữ liệu
        con = sqlite3.connect("fms.db")
        cur = con.cursor()
        cur.execute("SELECT name, qty FROM product")
        rows = cur.fetchall()
        con.close()

        tree.heading("name", text="Tên Sản Phẩm")
        tree.heading("qty", text="Tồn Kho")
        tree.column("name", width=200)
        tree.column("qty", width=100)

        for row in rows:
            tree.insert("", END, values=row)
    
    def excel(self):
        # Kết nối cơ sở dữ liệu và truy xuất dữ liệu
        con = sqlite3.connect("fms.db")
        cur = con.cursor()

        # Doanh thu
        cur.execute("SELECT sale_date, SUM(quantity * price) AS doanh_thu FROM sales JOIN product ON sales.product_id = product.pid GROUP BY sale_date")
        revenue_data = cur.fetchall()

        # Hàng hóa
        cur.execute("SELECT * FROM product")
        product_data = cur.fetchall()

        # Hàng tồn
        cur.execute("SELECT name, qty FROM product")
        stock_data = cur.fetchall()

        con.close()

        # Chuyển dữ liệu thành DataFrame
        df_revenue = pd.DataFrame(revenue_data, columns=["Ngày", "Doanh thu"])
        df_product = pd.DataFrame(product_data, columns=["ID", "Tên sản phẩm", "Loại", "Nhà cung cấp", "Giá", "Số lượng", "Trạng thái"])
        df_stock = pd.DataFrame(stock_data, columns=["Tên sản phẩm", "Tồn kho"])

        # Xuất dữ liệu sang file Excel tại đường dẫn cụ thể
        output_path = r"D:\Workspace\FMS\excel\statistical_report.xlsx"  # Đường dẫn file Excel
        with pd.ExcelWriter(output_path) as writer:
            df_revenue.to_excel(writer, sheet_name="Doanh thu", index=False)
            df_product.to_excel(writer, sheet_name="Hàng hóa", index=False)
            df_stock.to_excel(writer, sheet_name="Tồn kho", index=False)

        messagebox.showinfo("Xuất file Excel", "Dữ liệu đã được xuất thành công tại " + output_path)


    def main(self):
        self.root.destroy()
        os.system("python dashboard.py")
    
if __name__ == "__main__":
    root = Tk()
    obj = statisticalClass(root)
    root.mainloop()
