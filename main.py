import streamlit as st
import pandas as pd
import random
import mysql.connector

conn = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='pharma')
c = conn.cursor()



# Function to create Doctors table
def doctors_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Doctors(
                    D_Name VARCHAR(50) NOT NULL,
                    D_Specialization VARCHAR(50) NOT NULL,
                    D_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    D_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Doctors Table created successfully')

# Function to add data to Doctors table
def doctor_add_data(Dname, Dspec, Demail, Dnumber):
    try:
        c.execute(f"INSERT INTO Doctors (D_Name, D_Specialization, D_Email, D_Number) VALUES ('{Dname}', '{Dspec}', '{Demail}', '{Dnumber}')")
        conn.commit()
        print("Doctor added successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)


# Function to view all data in Doctors table
def doctor_view_all_data():
    try:
        c.execute('SELECT * FROM Doctors')
        doctor_data = c.fetchall()
        return doctor_data
    except mysql.connector.Error as err:
        logging.error("Error fetching doctor data: %s", err)
        return None




# Function to create Appointments table
def appointments_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Appointments(
                    A_Date DATE NOT NULL,
                    A_Doctor VARCHAR(50) NOT NULL,
                    A_Patient VARCHAR(50) NOT NULL, 
                    A_id INT PRIMARY KEY AUTO_INCREMENT
                    )''')
    print('Appointments Table created successfully')

# Function to add data to Appointments table
def appointment_add_data(Adate, Adoctor, Apatient):
    try:
        c.execute(f'INSERT INTO Appointments (A_Date, A_Doctor, A_Patient) VALUES ("{Adate}", "{Adoctor}", "{Apatient}")')
        conn.commit()
        print("Appointment added successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)


# Function to view all data in Appointments table
def appointment_view_all_data():
    try:
        c.execute('SELECT * FROM Appointments')
        appointment_data = c.fetchall()
        return appointment_data
    except mysql.connector.Error as err:
        print("Error:", err)



def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table create Successfully')

def customer_add_data(Cname, Cpass, Cemail, Cstate, Cnumber):
    c.execute(f'INSERT INTO Customers (C_Name, C_Password, C_Email, C_State, C_Number) VALUES ("{Cname}", "{Cpass}", "{Cemail}", "{Cstate}", "{Cnumber}")')
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data


def customer_update(Cemail, Cnumber):
    c.execute(f'UPDATE Customers SET C_Number = "{Cnumber}" WHERE C_Email = "{Cemail}"')
    conn.commit()
    print("Updating")


def customer_delete(Cemail):
    c.execute(f' DELETE FROM Customers WHERE C_Email = "{Cemail}"')
    conn.commit()


def drug_update(Duse, Did):
    c.execute(f'UPDATE Drugs SET D_Use = "{Duse}" WHERE D_id ={Did} ')
    conn.commit()


def drug_delete(Did):
    c.execute(f' DELETE FROM Drugs WHERE D_id = {Did}')
    conn.commit()


def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL, 
                D_id INT PRIMARY KEY NOT NULL)
                ''')
    print('DRUG Table create Successfully')


def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did):
    c.execute(
        f'INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_id) VALUES("{Dname}", "{Dexpdate}", "{Duse}", "{Dqty}","{Did}")')
    conn.commit()


def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data


def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL)
    ''')


def order_delete(Oid):
    c.execute(f' DELETE FROM Orders WHERE O_id = "{Oid}"')


def order_add_data(O_Name, O_Items, O_Qty, O_id):
    c.execute(f'INSERT INTO Orders (O_Name, O_Items,O_Qty, O_id) VALUES("{O_Name}", "{O_Items}", "{O_Qty}", "{O_id}")')
    conn.commit()


def order_view_data(customername):
    c.execute(f'SELECT * FROM Orders WHERE O_Name = "{customername}"')
    order_data = c.fetchall()
    return order_data


def order_view_all_data():
    c.execute('SELECT * FROM Orders')
    order_all_data = c.fetchall()
    return order_all_data


#__________________________________________________________________________________


def admin():


    st.title("Pharmacy Database Dashboard")
    menu = ["Drugs", "Customers", "Orders", "Doctors", "Appointments"]
    choice = st.sidebar.selectbox("Menu", menu)


    ## DRUGS
    if choice == "Drugs":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_area("When to Use")
            with col2:
                drug_quantity = st.text_area("Enter the quantity")
                drug_id = st.text_area("Enter the Drug id (example:#D1)")

            if st.button("Add Drug"):
                drug_add_data(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(drug_clean_df)
            with st.expander("View Drug Quantity"):
                drug_name_quantity_df = drug_clean_df[['Name','Quantity']]
                
                st.dataframe(drug_name_quantity_df)
        if choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_area("Drug ID")
            d_use = st.text_area("Drug Use")
            if st.button(label='Update'):
                drug_update(d_use,d_id)

        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_area("Drug ID")
            if st.button(label="Delete"):
                drug_delete(did)



    ## CUSTOMERS
    elif choice == "Customers":

        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password","Email-ID" ,"Area", "Number"])
                st.dataframe(cust_clean_df)

        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email,cust_number)

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)

    elif choice == "Orders":

        menu = ["View"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID"])
                st.dataframe(order_clean_df)
    # # doctors
    elif choice == "Doctors":
        menu = ["Add", "View"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":
            st.subheader("Add Doctor")
            doctor_name = st.text_input("Doctor Name")
            doctor_specialization = st.text_input("Specialization")
            doctor_email = st.text_input("Email")
            doctor_number = st.text_input("Phone Number")
            if st.button("Add Doctor"):
                doctor_add_data(doctor_name, doctor_specialization, doctor_email, doctor_number)
                st.success("Doctor Added Successfully!")
        elif choice == "View":
            st.subheader("View Doctors")
            doctor_result = doctor_view_all_data()
            if doctor_result:
                doctor_df = pd.DataFrame(doctor_result, columns=["Name", "Specialization", "Email", "Phone Number"])
                st.dataframe(doctor_df)
            else:
                st.write("No doctors found.")
    
    
    elif choice == "Appointments":
        menu = ["Add", "View"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":
            st.subheader("Add Appointment")
            appointment_date = st.date_input("Date")
            appointment_doctor = st.text_input("Doctor Name")
            appointment_patient = st.text_input("Patient Name")
            if st.button("Add Appointment"):
                appointment_add_data(appointment_date, appointment_doctor, appointment_patient)
                st.success("Appointment Added Successfully!")

        elif choice == "View":
            st.subheader("View Appointments")
            appointment_result = appointment_view_all_data()
            print(appointment_result)  # Add this line to print appointment_result
            if appointment_result:
                appointment_df = pd.DataFrame(appointment_result, columns=["Date", "Doctor", "Patient", "Appointment ID"])
                st.dataframe(appointment_df)
            else:
                st.write("No appointments found.")




def getauthenicate(username, password):
    c.execute(f'SELECT C_Password FROM Customers WHERE C_Name = "{username}"')
    cust_password = c.fetchall()
    if cust_password:  #
        if cust_password[0][0] == password:
            return True
    return False 


###################################################################

import logging
logging.basicConfig(level=logging.DEBUG)

def customer(username, password):
    if getauthenicate(username, password):
        logging.info("Authentication successful")
        st.title("Welcome to Pharmacy Store")

        st.subheader("Your Order Details")
        order_result = order_view_data(username)
        logging.debug(f"Order result: {order_result}")
        if order_result:
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
                st.dataframe(order_clean_df)
        else:
            st.write("No orders found.")

        st.subheader("Available Drugs:")
        drug_result = drug_view_all_data()
        logging.debug(f"Drug result: {drug_result}")
        if drug_result:
            order_items = []  
            order_quantities = []  
            order_prices = [] 

            # Display drug details
            for i, drug in enumerate(drug_result):
                drug_name = drug[0]
                drug_use = drug[2]
                drug_quantity = drug[3]  
                drug_price = drug[4]  
                st.subheader("Drug: " + drug_name)
                st.info("When to USE: " + str(drug_use))
                st.info("Available Quantity: " + str(drug_quantity))
                st.info("Price per unit: $" + str(drug_price))
                drug_order_quantity = st.number_input(label="Enter Quantity", min_value=0, max_value=drug_quantity, key=i)

                # Add drug to order
                if drug_order_quantity > 0:
                    order_items.append(drug_name)
                    order_quantities.append(drug_order_quantity)
                    order_prices.append(drug_price)

            total_price = sum(quantity * price for quantity, price in zip(order_quantities, order_prices))
            st.subheader("Total Price: $" + str(total_price))

            if st.button(label="Buy now"):
                O_items = ",".join(order_items)
                O_Qty = ",".join(str(quantity) for quantity in order_quantities)

                O_id = username + "#O" + str(random.randint(0, 1000000))
                order_add_data(username, O_items, O_Qty, O_id)
                st.success("Order placed successfully!")
        else:
            st.write("No drugs available for purchase.")
        # Appointment Booking
        st.subheader("Book Appointment:")
        appointment_date = st.date_input("Date")
        appointment_doctor = st.text_input("Doctor Name")
        appointment_patient = username  # Assuming patient name is the username
        if st.button("Book Appointment"):
            appointment_add_data(appointment_date, appointment_doctor, appointment_patient)
            st.success("Appointment Booked Successfully!")
    else:
        st.write("Invalid username or password.")




if __name__ == '__main__':
    drug_create_table()
    cust_create_table()
    order_create_table()
    doctors_create_table()
    appointments_create_table()

    menu = ["Login", "SignUp","Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            customer(username, password)

    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_area("Email ID")
        with col2:
            cust_area = st.text_area("State")
        with col3:
            cust_number = st.text_area("Phone Number")

        if st.button("Signup"):
            if (cust_password == cust_password1):
                customer_add_data(cust_name,cust_password,cust_email, cust_area, cust_number,)
                st.success("Account Created!")
                st.info("Go to Login Menu to login")
            else:
                st.warning('Password dont match')
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
   
        if st.sidebar.checkbox(label="Login"):
            if username == 'admin' and password == 'admin':
                admin()