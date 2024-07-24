import streamlit as st
from auth import teacher_auth, student_auth
import database as dbs

# Initialize session state for teacher and student login status
if not hasattr(st.session_state, 'logged_in_as_teacher'):
    st.session_state.logged_in_as_teacher = False

if not hasattr(st.session_state, 'logged_in_as_student'):
    st.session_state.logged_in_as_student = False

# main_user_interface
def main_ui():
    st.title("MCQ Test Management System")
    option = st.sidebar.selectbox("Choose your role:", ["Teacher", "Student"])

    if option == "Teacher":
        #st.session_state.logged_in_as_student = False
        teacher_option = st.radio("Choose an option:", ["Login", "Sign Up"])
        if teacher_option == "Login":
            teacher_login()
            if st.session_state.logged_in_as_teacher:
                    teacher_activities()
        elif teacher_option == "Sign Up":
            teacher_signup()
    elif option == "Student":
        #st.session_state.logged_in_as_teacher = False
        student_option = st.radio("Choose an option:", ["Login", "Sign Up"])
        if student_option == "Login":
            student_login()
            if st.session_state.logged_in_as_student:
                    student_activities()  
        elif student_option == "Sign Up":
            student_signup()





#login functions :
 
def teacher_signup():
    st.subheader("Teacher Sign Up")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Sign Up"):
        if dbs.get_teacher_by_username(username):
            st.error("Username already exists. Please choose a different one.")
        else:
            dbs.add_teacher(username, password)
            st.success("Teacher account created successfully! Please login.")

def student_signup():
    st.subheader("Student Sign Up")
    name = st.text_input("Name:")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Sign Up"):
        if dbs.get_student_by_username(username):
            st.error("Username already exists. Please choose a different one.")
        else:
            dbs.add_student(name, username, password)
            st.success("Student account created successfully! Please login.")

def teacher_login():
    with st.form(key='teacher_login_form'):
        st.subheader("Teacher Login")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button(label='Login')
        if submit_button:
            if teacher_auth(username, password):
                st.session_state.logged_in_as_teacher = True
                st.success("Login successful!")
                st.text("You are logged in as a teacher.")

def student_login():
    with st.form(key='student_login_form'):
        st.subheader("Student Login")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button(label='Login')
        if submit_button:
            if student_auth(username, password):
                st.session_state.logged_in_as_student = True
                st.session_state.username = username 
                st.success("Login successful!")
                st.text("You are logged in as a student.")
            else:
                st.error("Incorrect username or password. Please try again.")

                
def teacher_logout_ui():
    confirmation = st.checkbox("Are you sure you want to logout?")
    if confirmation:
        st.session_state.logged_in_as_teacher = False
        st.info("You are logged out as a teacher.")

def student_logout_ui():
    confirmation = st.checkbox("Are you sure you want to logout?")
    if confirmation:
        st.session_state.logged_in_as_student = False
        st.info("You are logged out as a student.")




# User Activties 
def teacher_activities():
    activity = st.sidebar.radio("Select Activity:", ["Add Question", "Add Subject", "View Questions", "View Students", "View Subject", "View Peer Teachers", "View Results", "Update Subject", "Delete Data", "Reset Database", "Logout"])
    if activity == "Add Question":
        add_question_ui()
    elif activity == "Add Subject":
        add_subject_ui()
    elif activity == "View Questions":
        view_questions_ui()
    elif activity == "View Students":
        view_students_ui()
    elif activity == "View Subject":
        view_subjects_ui()
    elif activity == "View Peer Teachers":
        view_teachers_ui()
    elif activity == "View Results":
        view_results_ui()
    elif activity == "Update Subject":
        update_subject_ui()
    elif activity == "Delete Data":
        delete_data_ui()
    elif activity == "Reset Database":
        reset_database_ui()
    elif activity == "Logout":
        teacher_logout_ui()

def student_activities():
    activity = st.sidebar.radio("Select Activity:", ["Attempt Test","View My Details", "Logout"])
    if activity == "Attempt Test":
        take_test()
    elif activity == "View My Details":
        view_student_details_ui(st.session_state.username)  # Pass the student's username to fetch their details
    elif activity == "Logout":
        student_logout_ui()


# Teacher UI Functions
def view_students_ui():
    st.subheader("View Students")
    students = dbs.get_all_students()
    if not students:
        st.write("No students available.")
    else:
        for i, student in enumerate(students, start=1):
            st.write(f"Student {i}:")
            st.write("Name:", student[1])
            st.write("Subject:", student[2])
            st.write("Username:", student[3])
            #st.write("Marks:", student[5])
            marks = dbs.get_marks_scored(student[0], student[2])
            if marks is not None:
                st.write("Marks Scored:", marks)
            else:
                st.write("No marks scored yet.")
            st.write("---")


def update_subject_ui():
    st.subheader("Update Subject")
    students = dbs.get_all_students()
    student_username = [student[3] for student in students]
    subjects = dbs.get_all_subjects()
    subject_name = [subject[1] for subject in subjects]

    # Dropdown menu to select the subject name to update
    subject_n = st.selectbox("Select Subject Name to Update", subject_name)
    
    # Dropdown menu to select the student username for the subject
    username = st.selectbox("Select Student Username for the Subject", student_username)
    
    if st.button("Update Subject"):
        if not dbs.get_student_by_username(username):
            st.error("Student not found.")
        else:
            dbs.update_student_subject(username, subject_n)
            st.success(f"Subject updated successfully for {username}.")
            # Assign the subject to the student
            student_id = dbs.get_student_id_by_username(username)
            subject_id = dbs.get_subject_id_by_name(subject_n)
            if student_id is not None and subject_id is not None:
                dbs.assign_subject_to_student(student_id, subject_id)
            else:
                st.error("Student ID or Subject ID not found.")


'''def update_subject_ui():
    st.subheader("Update Subject")
    students = dbs.get_all_students()
    student_username = [student[3] for student in students]
    #username = st.text_input("Enter student's username:")
    #subject = st.text_input("Enter new subject:")
    subjects = dbs.get_all_subjects()
    subject_name = [subject[1] for subject in subjects]

    # Dropdown menu to select the subject name to update
    subject_n = st.selectbox("Select Subject Name to Update", subject_name)
    
    # Dropdown menu to select the student username for the subject
    username = st.selectbox("Select Student Username for the Subject", student_username)
    
    if st.button("Update Subject"):
        if not dbs.get_student_by_username(username):
            st.error("Student not found.")
        else:
            dbs.update_student_subject(username, subject_n)
            st.success(f"Subject updated successfully for {username}.")'''

'''def add_question_ui():
    with st.form(key='add_question_form'):
        st.subheader("Add Question")
        question = st.text_area("Question:")
        option1 = st.text_input("Option 1:")
        option2 = st.text_input("Option 2:")
        option3 = st.text_input("Option 3:")
        option4 = st.text_input("Option 4:")
        correct_answer = st.selectbox("Correct Answer:", ["Option 1", "Option 2", "Option 3", "Option 4"])
        sub_id = st.text_input("Subject ID:")

        submit_button = st.form_submit_button(label='Add Question')
        if submit_button:
            options = [option1, option2, option3, option4]
            dbs.add_question(question, option1, option2, option3, option4, correct_answer,sub_id)
            st.success("Question added successfully!")'''

def add_question_ui():
    with st.form(key='add_question_form'):
        st.subheader("Add Question")
        question = st.text_area("Question:")
        option1 = st.text_input("Option 1:")
        option2 = st.text_input("Option 2:")
        option3 = st.text_input("Option 3:")
        option4 = st.text_input("Option 4:")
        correct_answer = st.selectbox("Correct Answer:", ["Option 1", "Option 2", "Option 3", "Option 4"])
        subject_options = [subject[1] for subject in dbs.get_all_subjects()]
        subject_name = st.selectbox("Select Subject", subject_options)

        submit_button = st.form_submit_button(label='Add Question')
        if submit_button:
            options = [option1, option2, option3, option4]
            correct_answer_index = ["Option 1", "Option 2", "Option 3", "Option 4"].index(correct_answer) + 1

            # Check if the subject exists
            if dbs.check_subject_existence(subject_name):
                subject_id = dbs.get_subject_id_by_name(subject_name)
                result_add = dbs.add_question(question, option1, option2, option3, option4, f"Option {correct_answer_index}", subject_id)
                if result_add == "Question added successfully.":
                    st.success("Question added successfully!")
                else:
                    st.error("Limit Reached")
            else:
                st.error("The provided subject name does not exist. Please create the subject first.")



def view_questions_ui():
    st.subheader("View Questions")
    questions = dbs.view_questions()

    if not questions:
        st.write("No questions available.")
    else:
        for i, question_tuple in enumerate(questions, start=1):
            st.write("----------------------------------------------------------------------------------------")
            st.write(f"Question {question_tuple[0]}: {question_tuple[1]}")
             # Assuming the first element is the question text
            st.write("Options:")
            st.write("A:", question_tuple[2])  # Assuming the second element is option A
            st.write("B:", question_tuple[3])  # Assuming the third element is option B
            st.write("C:", question_tuple[4])  # Assuming the fourth element is option C
            st.write("D:", question_tuple[5])  # Assuming the fifth element is option D
            st.write("Correct Answer:", question_tuple[6])  # Assuming the sixth element is the correct answer
            st.write("Subject ID:", question_tuple[7])  # Assuming the seventh element is the subject ID

# new function

def delete_data_ui():
    st.subheader("Delete Data")
    option = st.selectbox("Select an option:", ["Question", "Subject", "Student"])
    if option == "Question":
        delete_question_ui()
    elif option == "Subject":
        delete_subject_ui()
    elif option == "Student":
        delete_student_ui()

def delete_question_ui():
    st.subheader("Delete Question")
    question_ids = [q[0] for q in dbs.view_questions()]
    selected_question_id = st.selectbox("Select Question ID:", question_ids)
    if st.button("Delete Question"):
        if selected_question_id:
            dbs.delete_question(selected_question_id)
            st.success("Question deleted successfully.")
        else:
            st.error("Please select a question ID.")

def delete_subject_ui():
    st.subheader("Delete Subject")
    subject_ids = [s[0] for s in dbs.get_all_subjects()]
    selected_subject_id = st.selectbox("Select Subject ID:", subject_ids)
    if st.button("Delete Subject"):
        if selected_subject_id:
            dbs.delete_subject(selected_subject_id)
            st.success("Subject deleted successfully.")
        else:
            st.error("Please select a subject ID.")

def delete_student_ui():
    st.subheader("Delete Student")
    student_ids = [s[0] for s in dbs.get_all_students()]
    selected_student_id = st.selectbox("Select Student ID:", student_ids)
    if st.button("Delete Student"):
        if selected_student_id:
            dbs.delete_student(selected_student_id)
            st.success("Student deleted successfully.")
        else:
            st.error("Please select a student ID.")

def add_subject_ui():
    st.subheader("Add Subject")
    subject_name = st.text_input("Enter Subject Name:")
    if st.button("Add Subject"):
        if subject_name:
            dbs.add_subject(subject_name)
            st.success("Subject added successfully.")
        else:
            st.error("Please enter a subject name.")

def view_data_ui():
    st.subheader("View Data")
    option = st.selectbox("Select an option:", ["Subject Table", "Peer Teachers", "Result Table"])
    if option == "Subject Table":
        view_subjects_ui()
    elif option == "Peer Teachers":
        view_teachers_ui()
    elif option == "Result Table":
        view_results_ui()

def view_subjects_ui():
    st.subheader("View Subject Table")
    subjects = dbs.get_all_subjects()
    if subjects:
        for subject in subjects:
            st.write(f"Subject ID: {subject[0]}, Subject Name: {subject[1]}")
    else:
        st.write("No subjects available.")

def view_teachers_ui():
    st.subheader("View Peer Teachers")
    teachers = dbs.get_all_teachers()
    if teachers:
        for teacher in teachers:
            st.write(f"Teacher ID: {teacher[0]}, Username: {teacher[1]}")
    else:
        st.write("No peer teachers available.")

def view_results_ui():
    st.subheader("View Result Table")
    results = dbs.view_results()
    if results:
        for result in results:
            st.write(f"Result ID: {result[0]}, Student ID: {result[1]}, Subject ID: {result[2]}, Marks Scored: {result[3]}")
    else:
        st.write("No results available.")

def reset_database_ui():
    st.subheader("Reset Database")
    confirmation1 = st.checkbox("Confirm Reset Database (This will delete all data)")
    confirmation2 = st.checkbox("Are you sure?")
    if confirmation1 and confirmation2:
        dbs.reset_database()
        st.warning("Database reset successfully.")




#Student Ui functions : 


'''def take_test():
    if st.session_state.logged_in_as_student:
        st.title("Take Test")
        score = 0

        student_username = st.session_state.username  # Get the student's username from the session state

        # Fetch the student ID based on the username
        student_id = dbs.get_student_id_by_username(student_username)

        if student_id is None:
            st.error("Student ID not found for the given username.")
            return
    

        subject_options = [subject[1] for subject in dbs.get_all_subjects()]
        selected_subject = st.selectbox("Select Subject", subject_options)
        # Check if the student has already attempted the test for this subject
        #subject_name = st.text_input("Enter the subject you want to attempt the test for:")
        subject_id = dbs.get_subject_id_by_name(selected_subject)
        if dbs.check_result_existence(student_id, subject_id):
            st.warning("You have already attempted the test for this subject.")
            return

        with st.form(key='take_test_form'):
            # Fetch questions from database
            questions = dbs.view_questions()
            total_questions = len(questions)

            for i, question_tuple in enumerate(questions, start=1):
                st.subheader(f"Question {i}/{total_questions}")
                st.write(question_tuple[1])  # Assuming the second element of the tuple is the question text
                st.write(f"A) {question_tuple[2]}")
                st.write(f"B) {question_tuple[3]}")
                st.write(f"C) {question_tuple[4]}")
                st.write(f"D) {question_tuple[5]}")
                question_key = f"question_{i}_{question_tuple[1]}"  # Using question text to ensure uniqueness
                options = ['A', 'B', 'C', 'D']
                selected_option = st.radio(f"Select your answer for Question {i}:", options=options, key=question_key)
                correct_answer_index = int(question_tuple[6][-1]) - 1  # Assuming the correct answer is in the format "Option 1", "Option 2", etc.
                correct_answer = chr(65 + correct_answer_index)  # Convert the index to the corresponding letter ('A', 'B', 'C', 'D')
                if selected_option == correct_answer:
                    score += 1

                subject_id = question_tuple[7]  # Assuming the eighth element of the tuple is the subject ID

            submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                st.write(f"Your total score is: {score}/{total_questions}")
                print("Adding result to the database...")
                print("Student ID:", student_id)
                print("Subject ID:", subject_id)
                print("Score:", score)
                pass_score = (50 * total_questions) / 100
                if score >= pass_score:
                    st.success("Congratulations! You have passed the test.")
                else:
                    st.error("Sorry! You have failed the test.")
                # Update session state with the latest score
                # Insert score into result table
                dbs.add_result(student_id, subject_id, score)
                if dbs.add_result:
                    print("added success")
                else:
                    print("no")'''


def take_test():
    if st.session_state.logged_in_as_student:
        st.title("Take Test")
        score = 0

        student_username = st.session_state.username  # Get the student's username from the session state

        # Fetch the student ID based on the username
        student_id = dbs.get_student_id_by_username(student_username)

        if student_id is None:
            st.error("Student ID not found for the given username.")
            return

        # Get the subjects assigned to the student
        assigned_subjects = dbs.get_subjects_assigned_to_student(student_id)

        if not assigned_subjects:
            st.warning("You don't have any subjects assigned.")
            return

        # Dropdown menu to select the subject for the test
        selected_subject = st.selectbox("Select Subject", [subject[1] for subject in assigned_subjects])

        subject_id = dbs.get_subject_id_by_name(selected_subject)
        if subject_id is None:
            st.error("Subject ID not found for the selected subject.")
            return

        # Check if the student has already attempted the test for this subject
        if dbs.check_result_existence(student_id, subject_id):
            st.warning("You have already attempted the test for this subject.")
            return
        
        # Fetch questions for the selected subject from the database
        questions = dbs.get_questions_by_subject(subject_id)
        total_questions = len(questions)

        # Check if there are questions available for the selected subject
        if not questions:
            st.warning("There are no questions available for this subject.")
            return

        with st.form(key='take_test_form'):
            # Fetch questions for the selected subject from the database
            #questions = dbs.get_questions_by_subject(subject_id)
            #total_questions = len(questions)

            for i, question_tuple in enumerate(questions, start=1):
                st.subheader(f"Question {i}/{total_questions}")
                st.write(question_tuple[1])  # Assuming the second element of the tuple is the question text
                st.write(f"A) {question_tuple[2]}")
                st.write(f"B) {question_tuple[3]}")
                st.write(f"C) {question_tuple[4]}")
                st.write(f"D) {question_tuple[5]}")
                question_key = f"question_{i}_{question_tuple[1]}"  # Using question text to ensure uniqueness
                options = ['A', 'B', 'C', 'D']
                selected_option = st.radio(f"Select your answer for Question {i}:", options=options, key=question_key)
                correct_answer_index = int(question_tuple[6][-1]) - 1  # Assuming the correct answer is in the format "Option 1", "Option 2", etc.
                correct_answer = chr(65 + correct_answer_index)  # Convert the index to the corresponding letter ('A', 'B', 'C', 'D')
                if selected_option == correct_answer:
                    score += 1

            submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                st.write(f"Your total score is: {score}/{total_questions}")
                pass_score = (50 * total_questions) / 100
                if score >= pass_score:
                    st.success("Congratulations! You have passed the test.")
                else:
                    st.error("Sorry! You have failed the test.")
                # Insert score into result table
                dbs.add_result(student_id, subject_id, score)
                if dbs.add_result:
                    print("Result added successfully.")





def view_student_details_ui(username):
    st.subheader("View Student Details")
    student = dbs.get_student_by_username(username)

    if student:
        st.write(f"Name: {student[1]}")
        st.write(f"Subject: {student[2]}")
        st.write(f"Username: {student[3]}")
        st.write(f"Password: {student[4]}")
        st.write("-----------------------------------------------------------------------------------")
        view_student_score_ui()
        # Add any other details you want to display
    else:
        st.write("Student details not found.")

def view_student_score_ui():
    st.title("View My Score")
    student_username = st.session_state.username  # Assuming the username is stored in session state
    student_id = dbs.get_student_id_by_username(student_username)

    if student_id is None:
        st.error("Student ID not found for the given username.")
        return
    
    subjects = dbs.get_all_subjects()

    # Extract subject IDs from the result
    subject_ids = [subject[0] for subject in subjects]
    
    # Fetch student's scores from the result table for each subject
    scores = []
    for subject_id in subject_ids:
        score = dbs.get_marks_scored(student_id, subject_id)
        if score is not None:
            scores.append((subject_id, score))
    
    if scores:
        st.write("Your Scores:")
        st.write("| Subject ID | Score |")
        st.write("|------------|-------|")
        for subject_id, score in scores:
            st.write(f"| {subject_id} | {score} |")
    else:
        st.write("No scores available.")



if __name__ == "__main__":
    main_ui()
