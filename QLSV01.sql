CREATE DATABASE IF NOT EXISTS QLSV;
USE QLSV;
-- Tạo bảng sinhVien
CREATE TABLE IF NOT EXISTS sinhVien (
    MSV VARCHAR(20) PRIMARY KEY,
    Ten VARCHAR(100) NOT NULL,
    GioiTinh ENUM('nam', 'nữ'),
    NgaySinh DATE NOT NULL,
    DiaChi VARCHAR(255),
    Nganh VARCHAR(100),
    Mon VARCHAR(100),
    GiangVien VARCHAR(100),
    DiemTB DECIMAL(3, 2) CHECK (DiemTB >= 0 AND DiemTB <= 10),
    DanhGia VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS HDNgoaiKhoa (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    MSV VARCHAR(20),
    SuKien VARCHAR(100),
    FOREIGN KEY (MSV) REFERENCES sinhVien(MSV) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    TenDangNhap VARCHAR(50) NOT NULL UNIQUE,
    MatKhau VARCHAR(255) NOT NULL,
    Quyen ENUM('Admin', 'Normal User', 'Restricted User') NOT NULL
);

CREATE USER IF NOT EXISTS 'admin_group'@'%' IDENTIFIED BY 'admin_password';
GRANT ALL PRIVILEGES ON QLSV.* TO 'admin_group'@'%';

CREATE USER IF NOT EXISTS 'normal_user_group'@'%' IDENTIFIED BY 'normal_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON QLSV.* TO 'normal_user_group'@'%';

CREATE USER IF NOT EXISTS 'restricted_user_group'@'%' IDENTIFIED BY 'restricted_password';
GRANT SELECT ON QLSV.* TO 'restricted_user_group'@'%';

CREATE USER IF NOT EXISTS 'Manh'@'%' IDENTIFIED BY 'Manh123';
GRANT 'admin_group' TO 'Manh'@'%';

CREATE USER IF NOT EXISTS 'Khoan'@'%' IDENTIFIED BY 'Khoan123';
GRANT 'admin_group' TO 'Khoan'@'%'; 

CREATE USER IF NOT EXISTS 'Hieu'@'%' IDENTIFIED BY 'Hieu123';
GRANT 'normal_user_group' TO 'Hieu'@'%';

CREATE USER IF NOT EXISTS 'Viet'@'localhost' IDENTIFIED BY 'Viet123';
GRANT 'restricted_user_group' TO 'Viet'@'localhost'; 

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'Manh'@'%';
SHOW GRANTS FOR 'Khoan'@'%';
SHOW GRANTS FOR 'Hieu'@'%';
SHOW GRANTS FOR 'Viet'@'localhost';

SELECT User, Host, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv
FROM mysql.user
WHERE User IN ('Manh', 'Khoan', 'Hieu', 'Viet');

-- Mã hóa mật khẩu trước khi chèn vào cơ sở dữ liệu
INSERT INTO users (TenDangNhap, MatKhau, Quyen) VALUES
('admin', SHA2('admin_password', 256), 'Admin'),
('normal_user', SHA2('normal_password', 256), 'Normal User'),
('restricted_user', SHA2('restricted_password', 256), 'Restricted User');

INSERT INTO sinhVien (MSV, Ten, GioiTinh, NgaySinh, DiaChi, Nganh, Mon, GiangVien, DiemTB, DanhGia) VALUES
('SV001', 'Nguyễn Văn A', 'nam', '2000-01-01', 'Hà Nội', 'Công nghệ thông tin', 'Lập trình Python', 'Trần Văn B', 8.5, 'Xuất sắc'),
('SV002', 'Trần Thị B', 'nữ', '2000-02-02', 'Hà Nội', 'Kinh tế', 'Kinh tế vi mô', 'Nguyễn Văn C', 7.0, 'Khá'),
('SV003', 'Lê Văn C', 'nam', '2000-03-03', 'Đà Nẵng', 'Điện tử viễn thông', 'Mạch điện', 'Nguyễn Văn D', 6.5, 'Trung bình'),
('SV004', 'Phạm Thị D', 'nữ', '2000-04-04', 'Hồ Chí Minh', 'Ngôn ngữ Anh', 'Ngữ pháp tiếng Anh', 'Trần Văn E', 9.0, 'Xuất sắc'),
('SV005', 'Nguyễn Văn E', 'nam', '2000-05-05', 'Hà Nội', 'Quản trị kinh doanh', 'Marketing', 'Lê Văn F', 8.0, 'Khá'),
('SV006', 'Nguyễn Thị G', 'nữ', '2000-06-06', 'Hà Nội', 'Khoa học máy tính', 'Lập trình Java', 'Nguyễn Văn H', 7.8, 'Khá'),
('SV007', 'Trần Văn H', 'nam', '2000-07-07', 'Đà Nẵng', 'Kỹ thuật phần mềm', 'Quản lý dự án', 'Trần Văn I', 8.2, 'Khá'),
('SV008', 'Lê Thị I', 'nữ', '2000-08-08', 'Hồ Chí Minh', 'Hệ thống thông tin', 'Phân tích hệ thống', 'Nguyễn Văn J', 9.5, 'Xuất sắc'),
('SV009', 'Nguyễn Văn K', 'nam', '2000-09-09', 'Hà Nội', 'Công nghệ thông tin', 'An toàn thông tin', 'Trần Văn L', 6.0, 'Trung bình'),
('SV010', 'Trần Thị M', 'nữ', '2000-10-10', 'Đà Nẵng', 'Quản trị kinh doanh', 'Chiến lược kinh doanh', 'Nguyễn Văn N', 8.9, 'Xuất sắc'),
('SV011', 'Lê Văn O', 'nam', '2000-11-11', 'Hồ Chí Minh', 'Điện tử viễn thông', 'Mạch điện tử', 'Trần Văn P', 7.4, 'Khá'),
('SV012', 'Phạm Thị Q', 'nữ', '2000-12-12', 'Hà Nội', 'Ngôn ngữ Anh', 'Viết luận', 'Nguyễn Văn R', 8.1, 'Khá'),
('SV013', 'Nguyễn Văn S', 'nam', '2000-01-13', 'Đà Nẵng', 'Khoa học máy tính', 'Lập trình C++', 'Trần Văn T', 9.2, 'Xuất sắc'),
('SV014', 'Trần Thị U', 'nữ', '2000-02-14', 'Hồ Chí Minh', 'Kinh tế', 'Kinh tế quốc tế', 'Nguyễn Văn V', 7.5, 'Khá'),
('SV015', 'Lê Văn W', 'nam', '2000-03-15', 'Hà Nội', 'Công nghệ thông tin', 'Phát triển web', 'Trần Văn X', 8.7, 'Xuất sắc');

INSERT INTO HDNgoaiKhoa (MSV, SuKien) VALUES
('SV001', 'Chạy bộ từ thiện'),
('SV002', 'Hội thảo Kinh tế'),
('SV003', 'Câu lạc bộ Lập trình'),
('SV004', 'Tham gia diễn đàn tiếng Anh'),
('SV005', 'Hội thi Khởi nghiệp');