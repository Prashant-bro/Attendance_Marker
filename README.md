# 🎓 ID Scanning Attendance System

This project is an **ID Scanning–based Attendance System** that allows marking student attendance by scanning their **unique ID (Roll Number)** using a camera.  
It combines **OpenCV** + **EasyOCR** for ID detection, **MySQL** for database storage, **Tkinter GUI** for admin interface, and **Excel export** for reporting.

---

## 🚀 Features
- 🔑 Secure **Admin Login** before accessing the system.  
- 🆔 Add new students with details (Name, Roll Number, Department, Year).  
- 📷 **Scan student IDs** (8-character alphanumeric roll number) via webcam.  
- ✅ Attendance automatically marked as **Present** (default = Absent).  
- 📊 Export attendance records directly into an **Excel file**.  
- 🗂 MySQL backend ensures persistent storage of data.  
- 🎨 User-friendly interface built with **Tkinter GUI**.  

---

## 🗂 Database Schema

### **students**
| Field       | Type         | Key  | Extra          |
|-------------|--------------|------|----------------|
| student_id  | int          | PRI  | auto_increment |
| name        | varchar(100) |      |                |
| roll_number | varchar(20)  | UNI  |                |
| department  | varchar(50)  |      |                |
| year        | int          |      |                |

### **attendance**
| Field       | Type                     | Key  | Extra             |
|-------------|--------------------------|------|-------------------|
| id          | int                      | PRI  | auto_increment    |
| student_id  | int                      |      |                   |
| date        | date                     |      | DEFAULT curdate() |
| status      | enum('Present','Absent') |      | DEFAULT 'Absent'  |
| roll_number | varchar(20)              |      |                   |

---

## 🛠 Tech Stack
- **Python**  
- **OpenCV** – camera input  
- **EasyOCR** – ID text recognition  
- **Tkinter** – GUI  
- **MySQL** – database  
- **Pandas** – Excel export  

---

## ⚙️ Installation & Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/id-scanning-attendance.git
   cd id-scanning-attendance


2.Create a virtual environment (recommended)

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate   


3.Install dependencies

pip install -r requirements.txt


4.Configure MySQL Database

Create a database (e.g., attendance_db).

Run the following SQL commands:

-CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    department VARCHAR(50),
    year INT
);

-CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    date DATE DEFAULT CURDATE(),
    status ENUM('Present','Absent') DEFAULT 'Absent',
    roll_number VARCHAR(20)
);


-Add a .env file in your project root with your DB config:

DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=attendance_db


-Run the project

python final1.py

-📊 Usage

Login with Admin credentials (ABC / Abc@123).

Add student details.

Start camera → Scan student ID (roll number).

Attendance automatically updated in MySQL.

Export full report to Excel.

📌 Future Enhancements

Role-based login (Admin/Faculty).

Mobile app scanner support.

Web dashboard for managing reports.

SMS/Email notifications for absentees.

📝 License
-This project is licensed under the MIT License.