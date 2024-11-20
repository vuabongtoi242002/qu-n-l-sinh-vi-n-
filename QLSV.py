import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import bcrypt

db = None
cursor = None

# Hàm để kiểm tra quyền truy cập
def check_user_permissions(user, password):
    query = "SELECT MatKhau, Quyen FROM users WHERE TenDangNhap = %s"
    cursor.execute(query, (user,))
    result = cursor.fetchone()
    if result:
        hashed_password, role = result
        # Kiểm tra mật khẩu đã được mã hóa
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return role  
    return None

# Kết nối tới cơ sở dữ liệu
def connect_to_database():
    host = entry_host.get()
    user = entry_user.get()
    password = entry_password.get()
    database = entry_database.get()

    if not all([host, user, password, database]):
        messagebox.showerror("Lỗi", "Vui lòng điền tất cả các trường.")
        return

    try:
        global db, cursor
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = db.cursor()
        messagebox.showinfo("Thành công", "Kết nối đến cơ sở dữ liệu thành công!")
        display_students()  # Tự động hiển thị danh sách sinh viên
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Kết nối thất bại: {err}")

# Hàm để hiển thị danh sách sinh viên
def display_students():
    if cursor is None:
        messagebox.showerror("Lỗi", "Chưa kết nối đến cơ sở dữ liệu.")
        return
    for row in tree.get_children():
        tree.delete(row)
    query = """
    SELECT 
        sv.MSV,
        sv.Ten, 
        sv.GioiTinh,
        sv.NgaySinh, 
        sv.DiaChi, 
        sv.Nganh, 
        sv.Mon, 
        sv.GiangVien, 
        sv.DiemTB, 
        h.SuKien,
        sv.DanhGia
    FROM 
        sinhVien sv
    LEFT JOIN 
        HDNgoaiKhoa h ON sv.MSV = h.MSV;
    """
    
    try:
        cursor.execute(query)
        for (MSV, Ten, GioiTinh, NgaySinh, DiaChi, Nganh, Mon, GiangVien, DiemTB, SuKien, DanhGia) in cursor.fetchall():
            tree.insert("", "end", values=(MSV, Ten, GioiTinh, NgaySinh, DiaChi, Nganh, Mon, GiangVien, DiemTB if DiemTB is not None else 0, SuKien if SuKien is not None else '', DanhGia if DanhGia is not None else ''))
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Không thể lấy dữ liệu: {err}")

# Hàm để mở cửa sổ thêm/sửa sinh viên
def open_student_window(is_edit=False):
    student_window = tk.Toplevel(root)
    student_window.title("Thêm/Sửa Sinh Viên")

    fields = ['MSV', 'Tên','Giới tính', 'Ngày sinh', 'Địa chỉ', 'Ngành', 'Môn', 'Giảng viên', 'Điểm TB', 'Đánh giá']
    entries = {}

    for field in fields:
        frame = tk.Frame(student_window)
        label = tk.Label(frame, text=field, width=20, anchor='w')
        entry = tk.Entry(frame)
        label.pack(side=tk.LEFT, padx=5, pady=5)
        entry.pack(side=tk.RIGHT, padx=5, pady=5)
        frame.pack(fill='x')

        entries[field] = entry

    if is_edit:
        selected_item = tree.selection()[0]
        student_data = tree.item(selected_item)['values']
        for field, value in zip(fields, student_data):
            entries[field].insert(0, value)

    action_button = tk.Button(student_window, text="Lưu", command=lambda: (update_student(entries) if is_edit else add_student(entries)))
    action_button.pack(pady=10)

    if is_edit:
        entries['MSV'].config(state='readonly')

# Hàm để thêm sinh viên
def add_student(entries):
    msv = entries['MSV'].get()
    ten = entries['Tên'].get()
    gioitinh = entries['Giới tính'].get()
    ngay_sinh = entries['Ngày sinh'].get()
    dia_chi = entries['Địa chỉ'].get()
    nganh = entries['Ngành'].get()
    mon = entries['Môn'].get()
    giang_vien = entries['Giảng viên'].get()
    diem_tb = entries['Điểm TB'].get()
    danh_gia = entries['Đánh giá'].get()

    if not msv or not ten:
        messagebox.showerror("Lỗi", "Vui lòng điền các trường bắt buộc.")
        return

    try:
        query = """
        INSERT INTO sinhVien (MSV, Ten, GioiTinh, NgaySinh, DiaChi, Nganh, Mon, GiangVien, DiemTB, DanhGia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (msv, ten, gioitinh, ngay_sinh, dia_chi, nganh, mon, giang_vien, diem_tb, danh_gia))
        db.commit()
        messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
        display_students()
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Thêm sinh viên thất bại: {err}")

# Hàm để cập nhật thông tin sinh viên
def update_student(entries):
    msv = entries['MSV'].get()
    ten = entries['Tên'].get()
    gioitinh = entries['Giới tính'].get()
    ngay_sinh = entries['Ngày sinh'].get()
    dia_chi = entries['Địa chỉ'].get()
    nganh = entries['Ngành'].get()
    mon = entries['Môn'].get()
    giang_vien = entries['Giảng viên'].get()
    diem_tb = entries['Điểm TB'].get()
    danh_gia = entries['Đánh giá'].get()

    try:
        query = """
        UPDATE sinhVien
        SET Ten = %s, GioiTinh = %s, NgaySinh = %s, DiaChi = %s, Nganh = %s, Mon = %s, GiangVien = %s, DiemTB = %s, DanhGia = %s
        WHERE MSV = %s
        """
        cursor.execute(query, (ten, gioitinh, ngay_sinh, dia_chi, nganh, mon, giang_vien, diem_tb, danh_gia, msv))
        db.commit()
        messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!")
        display_students()
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Cập nhật sinh viên thất bại: {err}")

# Hàm để xóa sinh viên
def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn sinh viên để xóa.")
        return
    msv = tree.item(selected_item[0])['values'][0]
    try:
        query = "DELETE FROM sinhVien WHERE MSV = %s"
        cursor.execute(query, (msv,))
        db.commit()
        messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
        display_students()
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Xóa sinh viên thất bại: {err}")

# Hàm biểu đồ
def plot_students_by_major():
    query = "SELECT Nganh, COUNT(*) FROM sinhVien GROUP BY Nganh;"
    cursor.execute(query)
    data = cursor.fetchall()
    
    majors = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    plt.figure(figsize=(12, 6))
    plt.bar(majors, counts, color='lightcoral')
    plt.title('Phân bố sinh viên theo ngành học')
    plt.xlabel('Ngành học')
    plt.ylabel('Số lượng sinh viên')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_academic_performance():
    query = "SELECT Nganh, AVG(DiemTB) FROM sinhVien GROUP BY Nganh;"
    cursor.execute(query)
    data = cursor.fetchall()
    majors = [row[0] for row in data]
    average_scores = [row[1] for row in data]
    
    plt.figure(figsize=(12, 6))
    plt.bar(majors, average_scores, color='skyblue')
    plt.title('Điểm trung bình theo ngành học')
    plt.xlabel('Ngành học')
    plt.ylabel('Điểm trung bình')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_students_by_location():
    plt.figure(figsize=(10, 6))
    
    # Truy vấn dữ liệu
    query = "SELECT DiaChi, COUNT(*) FROM sinhVien GROUP BY DiaChi;"
    cursor.execute(query)
    data = cursor.fetchall()
    
    if not data:
        print("Không có dữ liệu để hiển thị.")
        return
    
    locations = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    # Vẽ biểu đồ cột
    bars = plt.bar(locations, counts, color=plt.cm.tab10.colors)
    
    # Thêm tiêu đề và nhãn
    plt.title('Phân bố sinh viên theo khu vực địa lý', fontsize=16)
    plt.xlabel('Khu vực', fontsize=14)
    plt.ylabel('Số lượng sinh viên', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    
    # Thêm chú thích cho các cột
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_extracurricular_participation():
    plt.figure(figsize=(10, 6))
    
    # Truy vấn dữ liệu
    query = "SELECT SuKien, COUNT(*) FROM HDNgoaiKhoa GROUP BY SuKien;"
    cursor.execute(query)
    data = cursor.fetchall()
    
    if not data:
        print("Không có dữ liệu để hiển thị.")
        return
    
    activities = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    # Vẽ biểu đồ cột
    bars = plt.bar(activities, counts, color=plt.cm.tab10.colors)
    
    # Thêm tiêu đề và nhãn
    plt.title('Tỷ lệ tham gia các hoạt động ngoại khóa', fontsize=16)
    plt.xlabel('Hoạt động', fontsize=14)
    plt.ylabel('Số lượng sinh viên', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    
    # Thêm chú thích cho các cột
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_scholarship_distribution():
    query_scholarship = """
    SELECT Nganh, COUNT(*) 
    FROM sinhVien 
    WHERE DiemTB > 8 
    GROUP BY Nganh;
    """
    cursor.execute(query_scholarship)
    scholarship_data = cursor.fetchall()

    query_total_count = "SELECT COUNT(*) FROM sinhVien;"
    cursor.execute(query_total_count)
    total_count = cursor.fetchone()[0]

    scholarship_counts = [row[1] for row in scholarship_data]
    majors = [row[0] for row in scholarship_data]
    
    non_scholarship_count = total_count - sum(scholarship_counts)
    scholarship_counts.append(non_scholarship_count)
    majors.append('Không học bổng')

    plt.figure(figsize=(10, 6))
    explode = [0.1] * len(scholarship_counts)
    plt.pie(scholarship_counts, labels=majors, autopct='%1.1f%%', explode=explode, shadow=True, startangle=140)
    
    plt.title('Phân bố học bổng theo ngành học')
    plt.axis('equal')
    plt.show()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Quản Lý Sinh Viên")

# Tạo các trường nhập liệu
tab_control = ttk.Notebook(root)
connection_frame = tk.Frame(tab_control)
tab_control.add(connection_frame, text='Kết nối CSDL')
tab_control.pack(expand=1, fill='both')

labels = ["Host:", "User :", "Password:", "Database:"]
entries = {}

for i, label in enumerate(labels):
    frame = tk.Frame(connection_frame)
    label_widget = tk.Label(frame, text=label, width=20, anchor='w')
    entry = tk.Entry(frame, show='*' if label == "Password:" else '')
    label_widget.grid(row=i, column=0, padx=5, pady=5)
    entry.grid(row=i, column=1, padx=5, pady=5)
    frame.pack(fill='x')
    entries[label] = entry

entry_host = entries["Host:"]
entry_user = entries["User :"]
entry_password = entries["Password:"]
entry_database = entries["Database:"]

# Nút kết nối
btn_connect = tk.Button(connection_frame, text="Kết nối", command=connect_to_database)
btn_connect.pack(pady=20)

# Tạo bảng hiển thị sinh viên
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame, columns=("MSV", "Ten", "GioiTinh", "NgaySinh", "DiaChi", "Nganh", "Mon", "GiangVien", "DiemTB", "SuKien", "DanhGia"), show='headings')
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

vertical_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

tree.configure(yscrollcommand=vertical_scrollbar.set)
tree.configure(xscrollcommand=horizontal_scrollbar.set)

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

# Nút thêm sinh viên
btn_add = tk.Button(root, text="Thêm Sinh Viên", command=lambda: open_student_window(is_edit=False))
btn_add.pack(pady=5)

# Nút sửa sinh viên
btn_edit = tk.Button(root, text="Sửa Sinh Viên", command=lambda: open_student_window(is_edit=True))
btn_edit.pack(pady=5)

# Nút xóa sinh viên
btn_delete = tk.Button(root, text="Xóa Sinh Viên", command=delete_student)
btn_delete.pack(pady=5)

chart_tab = ttk.Frame(tab_control)
tab_control.add(chart_tab, text='Biểu Đồ')

# Tạo các nút cho từng biểu đồ
charts = [
    ("Biểu đồ sinh viên theo ngành", plot_students_by_major),
    ("Biểu đồ thành tích học tập", plot_academic_performance),
    ("Biểu đồ phân bố theo khu vực", plot_students_by_location),
    ("Biểu đồ hoạt động ngoại khóa", plot_extracurricular_participation),
    ("Biểu đồ phân bố học bổng", plot_scholarship_distribution)
]

for text, command in charts:
    button = tk.Button(chart_tab, text=text, command=command)
    button.pack(pady=5)

tab_control.pack(expand=1, fill='both')

root.mainloop()