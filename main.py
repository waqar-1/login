import hashlib
from os import write
import streamlit as st
import pandas as pd

# DB Management
import sqlite3
import base64

main_bg = "back.png"
main_bg_ext = "jpg"

side_bg = "back.png"
side_bg_ext = "jpg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)
conn = sqlite3.connect('data.db')
c = conn.cursor()


# Security
# passlib,hashlib,bcrypt,scrypt


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',
              (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',
              (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    """Crime Reporting Servece"""

    st.title("Crime Reporting service")

    menu = ["Report Now", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Report Now":
        st.subheader("Complaints Registration Form ")
        st.subheader("Your Identity is our priority( No One knows who You Are ")

        st.header("Full Name")
        user_input = st.text_input("Your Name")


        display = ("Male","Female ")
        st.text_input("E-mail")

        options = list(range(len(display)))

        

        value = st.selectbox("Gender", options, format_func=lambda x: display[x])
        st.text_input("Cnic No")
        display = ("Student"," Goverment Job","Private","Army","Farmer","other")

        options = list(range(len(display)))

        

        value = st.selectbox("Occupation", options, format_func=lambda x: display[x])

        st.header("Crime Details")
        
        display = ("Cyber Crime", "Extortion","White Collar Crime","Theft","Robbery","Terrorism","Murderer")

        options = list(range(len(display)))

        

        value = st.selectbox("Type of Crime", options, format_func=lambda x: display[x])


        st.write(value)
        st.header("Please Select Date or Time")
        st.date_input('Select Date')
        user_input = st.number_input("Enter Time")
        st.header("Address")
        user_input = st.text_input("Address")

        st.header("Contact ")
        st.text_input("Mobile/tel")

        submit = st.button('submit Complaint')
        if submit:
           st.write(f'Complaint successfully Submited ')
		


    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox(
                    "Task", ["Add Post", "Analytics", "Profiles"])
                if task == "Add Post":
                    st.subheader("Add Your Post")

                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=[
                                            "Username", "Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
