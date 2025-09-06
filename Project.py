import mysql.connector as mc
import cv2 as c
import tkinter as tk
from tkinter import messagebox as m
import easyocr as eo
import pandas as pd 
import os 
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

reader = eo.Reader(['en'])

def admin_login():
    login_win = tk.Tk()
    login_win.geometry("300x200")
    login_win.title("Admin Login")
    login_win.configure(bg="light grey")

    tk.Label(login_win, text="Username:", font=("Arial", 12), bg="light grey").pack(pady=5)
    e_user = tk.Entry(login_win, font=("Arial", 12))
    e_user.pack(pady=5)
    
    tk.Label(login_win, text="Password:", font=("Arial", 12), bg="light grey").pack(pady=5)
    e_pass = tk.Entry(login_win, font=("Arial", 12), show="*")
    e_pass.pack(pady=5)
    
    def check_login():
        username = e_user.get()
        password = e_pass.get()
        if username == "ABC" and password == "Abc@123":
            login_win.destroy()
            main_window()
        else:
            m.showerror("Error", "Wrong Username or Password!")
            e_user.delete(0, tk.END)
            e_pass.delete(0, tk.END)
    tk.Button(login_win, text="Login", font=("Arial", 12), command=check_login).pack(pady=10)
    login_win.mainloop()
def main_window():
    db = mc.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        database=DB_NAME
    )
    cur = db.cursor()
    
    win = tk.Tk()
    win.title("Attendance Report")
    win.configure(bg="sky blue")
    
    from tkinter import filedialog as fd
    tk.Label(win, text="Should we start??", font=("Arial", 20), bg="sky blue").pack(pady=20)
    
    def add_student_details():
        add_win = tk.Toplevel(win)
        add_win.title("Add Student Details")
        add_win.geometry("400x400")
        add_win.configure(bg="light grey")
        
        tk.Label(add_win, text="Name:", bg="light grey").pack(pady=5)
        e_name = tk.Entry(add_win)
        e_name.pack()

        tk.Label(add_win, text="Roll Number:", bg="light grey").pack(pady=5)
        e_roll = tk.Entry(add_win)
        e_roll.pack()

        tk.Label(add_win, text="Department:", bg="light grey").pack(pady=5)
        e_dept = tk.Entry(add_win)
        e_dept.pack()

        tk.Label(add_win, text="Year:", bg="light grey").pack(pady=5)
        e_year = tk.Entry(add_win)
        e_year.pack()
        def save_student():
            name = e_name.get().strip()
            roll_number = e_roll.get().strip().upper()
            department = e_dept.get().strip()
            year = e_year.get().strip()

            if not (name and roll_number and department and year):
                m.showerror("Error", "All fields are required!")
                return

            try:
                cur.execute(
                    "INSERT INTO students (name, roll_number, department, year) VALUES (%s, %s, %s, %s)",
                    (name, roll_number, department, year)
                )
                db.commit()
                m.showinfo("Success", "Student details added successfully!")
                add_win.destroy()
            except mc.Error as e:
                m.showerror("Database Error", f"Failed to add student: {e}")
     
        tk.Button(add_win, text="Save", command=save_student).pack(pady=20)
    def export_report():
        try:
            query = """
                SELECT
                    s.roll_number AS RollNumber,
                    s.name AS Name,
                    s.department AS Department,
                    s.year AS Year,
                    a.date AS Date,
                    a.status AS Status
                FROM attendance a
                JOIN students s ON a.student_id = s.student_id
                ORDER BY a.date ASC, s.roll_number ASC
            """
            cur.execute(query)
            rows = cur.fetchall()
            if rows:
                columns = [desc[0] for desc in cur.description]
                df = pd.DataFrame(rows, columns=columns)
                default_name = "Attendance_Report.xlsx"
                file_path = fd.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    initialfile=default_name,
                    title="Save Attendance Report As"
                )
                if not file_path:
                    return
                df.to_excel(file_path, index=False)
                m.showinfo("Success", f"Attendance report saved to {file_path}")
            else:
                m.showinfo("Info", "No attendance records found.")
        except mc.Error as e:
            m.showerror("Database Error", f"Failed to fetch attendance data: {e}")
        except Exception as e:
            m.showerror("Error", f"An error occurred: {e}")
    tk.Button(win,text="Export Attendance",font=(("Arail"),25),command=export_report).pack(pady=10)
    def atd():
        cam = c.VideoCapture(0)
        if not cam.isOpened():
            m.showerror("Warning", "Couldn't open camera")
            return
        while True:
            ret, frame = cam.read()
            if not ret:
                m.showerror("Error", "Some error occurred")
                break
            c.imshow("ID Scan", frame)
            take_eng(frame)
            if c.waitKey(200) & 0xFF == ord('q'):
                c.destroyWindow("ID Scan")
                break
        cam.release()
        c.destroyAllWindows()

    def take_eng(frame):
        res = reader.readtext(frame)
        detected_numbers = []
        for i in res:
            if len(i[1]) == 8 and i[1].isalnum():
                rollno = i[1].strip().upper()
                detected_numbers.append(rollno)
                att_mar(rollno)

    def att_mar(rollno):
        if rollno:
            cur.execute("SELECT student_id FROM students WHERE roll_number = %s", (rollno,))
            result = cur.fetchone()
            if result:
                student_id = result[0]
                cur.execute("SELECT status FROM attendance WHERE student_id = %s AND date = CURDATE()", (student_id,))
                existing_record = cur.fetchone()
                if existing_record:
                    if existing_record[0] == 'Present':
                        m.showinfo("Info", "Attendance for today is already marked as Present.")
                    else:
                        cur.execute(
                            "UPDATE attendance SET status = 'Present' WHERE student_id = %s AND date = CURDATE()",
                            (student_id,)
                        )
                        db.commit()
                        m.showinfo("Success", "Attendance updated to Present successfully!")
                else:
                    cur.execute(
                        "INSERT INTO attendance (student_id, roll_number, date, status) VALUES (%s, %s, CURDATE(), 'Present')",
                        (student_id, rollno)
                    )
                    db.commit()
                    m.showinfo("Success", "Attendance marked as Present successfully!")
            else:
                m.showerror("Error", f"Roll Number {rollno} not found in database.")

    b1 = tk.Button(win, text="Add Details", font=("Arial", 20), command=add_student_details)
    b1.pack(pady=20)

    b2 = tk.Button(win, text="Attendance", font=("Arial", 20), command=atd)
    b2.pack(pady=20)
    
    def ex_f(event=None):
        win.destroy()
    
    win.bind("<Escape>", ex_f)
    win.mainloop()

admin_login()
