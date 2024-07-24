# auth.py
import database as dbs

def teacher_auth(username, password):
    teacher = dbs.get_teacher_by_username(username)
    if teacher and teacher[2] == password:
        return True
    else:
        return False
    
    
def student_auth(username, password):
    student = dbs.get_student_by_username(username)
    if student and student[4] == password:
        return True
    else:
        return False
