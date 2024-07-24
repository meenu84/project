# database.py
import sqlite3
from threading import get_ident

# Define a thread-local storage for the database connection
_db_connections = {}


def get_connection():
    # Get the thread identifier
    thread_id = get_ident()
    
    # Check if a connection already exists for this thread
    if thread_id not in _db_connections:
        # If not, create a new connection
        _db_connections[thread_id] = sqlite3.connect('test_management.db')
    
    return _db_connections[thread_id]


def close_connection():
    # Close the connection for the current thread
    thread_id = get_ident()
    if thread_id in _db_connections:
        _db_connections[thread_id].close()
        del _db_connections[thread_id]

def create_tables():
    with get_connection() as conn:
        c = conn.cursor()
        # Creating tables if they don't exist
        c.execute('''CREATE TABLE IF NOT EXISTS Teacher (
                    T_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Username TEXT UNIQUE,
                    Password TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Student (
                    S_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT,
                    Subject TEXT,
                    Username TEXT UNIQUE,
                    Password TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Subject (
                    Sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    SubjectName TEXT UNIQUE)''')

        c.execute('''CREATE TABLE IF NOT EXISTS Question (
                    Q_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Question TEXT,
                    Option1 TEXT,
                    Option2 TEXT,
                    Option3 TEXT,
                    Option4 TEXT,
                    Correct_answer TEXT,
                    Sub_id INTEGER,
                    FOREIGN KEY (Sub_id) REFERENCES Subject(Sub_id))''')

        c.execute('''CREATE TABLE IF NOT EXISTS Result (
                    Result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    S_id INTEGER,
                    Sub_id INTEGER,
                    Marks_scored INTEGER,
                    FOREIGN KEY (S_id) REFERENCES Student(S_id),
                    FOREIGN KEY (Sub_id) REFERENCES Subject(Sub_id))''')
        
        # Create the Student_Subject junction table
        c.execute('''CREATE TABLE IF NOT EXISTS Student_Subject (
                    S_id INTEGER,
                    Sub_id INTEGER,
                    FOREIGN KEY (S_id) REFERENCES Student(S_id),
                    FOREIGN KEY (Sub_id) REFERENCES Subject(Sub_id),
                    UNIQUE (S_id, Sub_id))''')

        # Committing the changes
        conn.commit()

def add_teacher(username, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Teacher (Username, Password) VALUES (?, ?)", (username, password))
        conn.commit()
        

def add_student(name, username, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Student (Name, Username, Password) VALUES (?, ?, ?)", (name, username, password))
        conn.commit()
        

def add_subject(subject_name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Subject (SubjectName) VALUES (?)", (subject_name,))
        conn.commit()
        

def add_question(question, option1, option2, option3, option4, correct_answer, sub_id):
    # Check if the number of questions for the subject exceeds the limit
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Question WHERE Sub_id = ?", (sub_id,))
        question_count = c.fetchone()[0]
        if question_count >= 10:
            return "Maximum limit of questions per subject reached."
        
        # If the limit is not reached, proceed to add the question
        c.execute("INSERT INTO Question (Question, Option1, Option2, Option3, Option4, Correct_answer, Sub_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (question, option1, option2, option3, option4, correct_answer, sub_id))
        conn.commit()
        return "Question added successfully."

        

def add_result(student_id, sub_id, marks_scored):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO Result (S_id, Sub_id, Marks_scored) VALUES (?, ?, ?)", (student_id, sub_id, marks_scored))
        conn.commit()

        

def view_teachers():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Teacher")
        teachers = c.fetchall()
        return teachers

def delete_teacher(teacher_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Teacher WHERE T_id = ?", (teacher_id,))
        conn.commit()

def update_teacher(teacher_id, new_username, new_password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE Teacher SET Username = ?, Password = ? WHERE T_id = ?", (new_username, new_password, teacher_id))
        conn.commit()

# Similar functions for Student, Subject, Question, and Result relations
# Student
def view_students():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Student")
        students = c.fetchall()
        return students

def delete_student(student_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Student WHERE S_id = ?", (student_id,))
        conn.commit()

def update_student(student_id, new_name, new_subject, new_username, new_password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE Student SET Name = ?, Subject = ?, Username = ?, Password = ? WHERE S_id = ?", (new_name, new_subject, new_username, new_password, student_id))
        conn.commit()

# Subject
def view_subjects():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Subject")
        subjects = c.fetchall()
        return subjects

def delete_subject(subject_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Subject WHERE Sub_id = ?", (subject_id,))
        conn.commit()

def update_subject(subject_id, new_subject_name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE Subject SET SubjectName = ? WHERE Sub_id = ?", (new_subject_name, subject_id))
        conn.commit()

# Question
def view_questions():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Question")
        questions = c.fetchall()
        return questions

def delete_question(question_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Question WHERE Q_id = ?", (question_id,))
        conn.commit()

def update_question(question_id, new_question, new_options, new_correct_answer, new_sub_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE Question SET Question = ?, Option1 = ?, Option2 = ?, Option3 = ?, Option4 = ?, Correct_answer = ?, Sub_id = ? WHERE Q_id = ?",
                  (new_question, new_options[0], new_options[1], new_options[2], new_options[3], new_correct_answer, new_sub_id, question_id))
        conn.commit()

# Result
def view_results():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Result")
        results = c.fetchall()
        return results

def delete_result(result_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Result WHERE Result_id = ?", (result_id,))
        conn.commit()

def update_result(result_id, new_s_id, new_sub_id, new_marks_scored):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE Result SET S_id = ?, Sub_id = ?, Marks_scored = ? WHERE Result_id = ?", (new_s_id, new_sub_id, new_marks_scored, result_id))
        conn.commit()

# Teacher
def get_teacher_by_username(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Teacher WHERE Username = ?", (username,))
        teacher = c.fetchone()
        return teacher

# Student
def get_student_by_username(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Student WHERE Username = ?", (username,))
        student = c.fetchone()
        return student

# Result
def get_marks_scored(student_id, subject_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT Marks_scored FROM Result WHERE S_id = ? AND Sub_id = ?", (student_id, subject_id))
        marks_scored = c.fetchone()
        return marks_scored[0] if marks_scored else None

def get_teacher_by_id(teacher_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Teacher WHERE T_id = ?", (teacher_id,))
        teacher = c.fetchone()
        return teacher

def get_all_teachers():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Teacher")
        teachers = c.fetchall()
        return teachers

def count_teachers():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Teacher")
        count = c.fetchone()[0]
        return count

def check_teacher_existence(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM Teacher WHERE Username = ?)", (username,))
        exists = c.fetchone()[0]
        return exists

def search_teachers(criteria):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Teacher WHERE Name LIKE ? OR Subject LIKE ?", (f'%{criteria}%', f'%{criteria}%'))
        teachers = c.fetchall()
        return teachers

def get_subject_id_by_name(subject_name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT Sub_id FROM Subject WHERE SubjectName = ?", (subject_name,))
        result = c.fetchone()
        return result[0] if result else None

def get_student_by_id(student_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Student WHERE S_id = ?", (student_id,))
        student = c.fetchone()
        return student

def get_all_students():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Student")
        students = c.fetchall()
        return students

def count_students():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Student")
        count = c.fetchone()[0]
        return count

def check_student_existence(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM Student WHERE Username = ?)", (username,))
        exists = c.fetchone()[0]
        return exists

def search_students(criteria):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Student WHERE Name LIKE ? OR Subject LIKE ?", (f'%{criteria}%', f'%{criteria}%'))
        students = c.fetchall()
        return students



def get_subject_by_id(subject_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Subject WHERE Sub_id = ?", (subject_id,))
        subject = c.fetchone()
        return subject

def get_all_subjects():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Subject")
        subjects = c.fetchall()
        return subjects

def count_subjects():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Subject")
        count = c.fetchone()[0]
        return count

def check_subject_existence(subject_name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM Subject WHERE SubjectName = ?)", (subject_name,))
        exists = c.fetchone()[0]
        return exists

def search_subjects(criteria):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Subject WHERE SubjectName LIKE ?", (f'%{criteria}%',))
        subjects = c.fetchall()
        return subjects


def get_question_by_id(question_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Question WHERE Q_id = ?", (question_id,))
        question = c.fetchone()
        return question

def count_questions():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Question")
        count = c.fetchone()[0]
        return count

def check_question_existence(question_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM Question WHERE Q_id = ?)", (question_id,))
        exists = c.fetchone()[0]
        return exists

def search_questions(criteria):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Question WHERE Question LIKE ?", (f'%{criteria}%',))
        questions = c.fetchall()
        return questions


def get_result_by_id(result_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Result WHERE Result_id = ?", (result_id,))
        result = c.fetchone()
        return result

def count_results():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Result")
        count = c.fetchone()[0]
        return count

def check_result_existence(student_id, subject_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT EXISTS(SELECT 1 FROM Result WHERE S_id = ? AND Sub_id = ?)", (student_id, subject_id))
        exists = c.fetchone()[0]
        return exists

def update_student_subject(username, new_subject):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE Student SET Subject = ? WHERE Username = ?", (new_subject, username))
        conn.commit()

'''def get_student_scores(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT Subject.SubjectName, Result.Marks_scored FROM Result INNER JOIN Subject ON Result.Sub_id = Subject.Sub_id INNER JOIN Student ON Result.S_id = Student.S_id WHERE Student.Username = ?", (username,))
        scores = c.fetchall()
        return scores'''


def reset_database():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM Teacher")
        c.execute("DELETE FROM Student")
        c.execute("DELETE FROM Subject")
        c.execute("DELETE FROM Question")
        c.execute("DELETE FROM Result")
        conn.commit()

def get_student_id_by_username(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT S_id FROM Student WHERE Username = ?", (username,))
        student_id = c.fetchone()
        return student_id[0] if student_id else None

#student_subject table 
def assign_subject_to_student(student_id, subject_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO Student_Subject (S_id, Sub_id) VALUES (?, ?)", (student_id, subject_id))
        conn.commit()

def get_subjects_assigned_to_student(student_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT Subject.* FROM Subject INNER JOIN Student_Subject ON Subject.Sub_id = Student_Subject.Sub_id WHERE Student_Subject.S_id = ?", (student_id,))
        subjects = c.fetchall()
        return subjects
    

#questions of particular subject 
def get_questions_by_subject(subject_id):
    """
    Retrieve questions based on the subject ID.

    Parameters:
        subject_id (int): The ID of the subject.

    Returns:
        list: A list of tuples, each containing question details.
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Question WHERE Sub_id = ?", (subject_id,))
        questions = c.fetchall()
    return questions
