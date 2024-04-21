import streamlit as st
import pandas as pd

# Load initial data
data = pd.DataFrame(columns=['id', 'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])

# Function to add a new patient
def add_patient(id, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke):
    global data
    new_patient = pd.DataFrame({'id': [id],
                                'gender': [gender],
                                'age': [age],
                                'hypertension': [hypertension],
                                'heart_disease': [heart_disease],
                                'ever_married': [ever_married],
                                'work_type': [work_type],
                                'residence_type': [residence_type],
                                'avg_glucose_level': [avg_glucose_level],
                                'bmi': [bmi],
                                'smoking_status': [smoking_status],
                                'stroke': [stroke]})
    data = pd.concat([data, new_patient], ignore_index=True)

# Function to display patient data
def display_patients():
    global data
    st.write(data)

# Function to update patient data
def update_patient(id, column, value):
    global data
    data.loc[data['id'] == id, column] = value

# Function to delete patient data
def delete_patient(id):
    global data
    data = data[data['id'] != id]

# Streamlit UI
st.title('Hospital Patients CRUD App')

# Sidebar for CRUD operations
menu = st.sidebar.selectbox('Menu', ['Add Patient', 'View Patients', 'Update Patient', 'Delete Patient'])

if menu == 'Add Patient':
    st.sidebar.header('Add New Patient')
    patient_id = st.sidebar.text_input('ID')
    gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
    age = st.sidebar.number_input('Age', min_value=0, max_value=150)
    hypertension = st.sidebar.checkbox('Hypertension')
    heart_disease = st.sidebar.checkbox('Heart Disease')
    ever_married = st.sidebar.selectbox('Ever Married', ['Yes', 'No'])
    work_type = st.sidebar.selectbox('Work Type', ['Private', 'Self-employed', 'Govt_job', 'Children', 'Never_worked'])
    residence_type = st.sidebar.selectbox('Residence Type', ['Urban', 'Rural'])
    avg_glucose_level = st.sidebar.number_input('Average Glucose Level')
    bmi = st.sidebar.number_input('BMI')
    smoking_status = st.sidebar.selectbox('Smoking Status', ['Smokes', 'Formerly Smoked', 'Never Smoked', 'Unknown'])
    stroke = st.sidebar.checkbox('Stroke')
    
    if st.sidebar.button('Add'):
        add_patient(patient_id, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke)
        st.success('Patient added successfully!')

elif menu == 'View Patients':
    st.header('View Patients')
    display_patients()

elif menu == 'Update Patient':
    st.sidebar.header('Update Patient')
    patient_id = st.sidebar.text_input('ID')
    column = st.sidebar.selectbox('Select Column', data.columns)
    new_value = st.sidebar.text_input('New Value')

    if st.sidebar.button('Update'):
        update_patient(patient_id, column, new_value)
        st.success('Patient data updated successfully!')

elif menu == 'Delete Patient':
    st.sidebar.header('Delete Patient')
    patient_id = st.sidebar.text_input('ID')

    if st.sidebar.button('Delete'):
        delete_patient(patient_id)
        st.success('Patient data deleted successfully!')
