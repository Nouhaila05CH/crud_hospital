import streamlit as S
import pandas as P
def load_data():
    try:
        data = P.read_csv("patients.csv")
        S.write("Data loaded successfully")
    except FileNotFoundError:
        data = P.DataFrame(columns=['id', 'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])
        S.write("No data file found")
    return data
def save_data(data):
    data.to_csv("patients.csv", index=False)
def add_patient(id, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke):
    global data
    new_patient = P.DataFrame({'id': [id],
                                'gender': [gender],
                                'age': [age],
                                'hypertension': [hypertension],
                                'heart_disease': [heart_disease],
                                'ever_married': [ever_married],
                                'work_type': [work_type],
                                'Residence_type': [residence_type],
                                'avg_glucose_level': [avg_glucose_level],
                                'bmi': [bmi],
                                'smoking_status': [smoking_status],
                                'stroke': [stroke]})
    data = P.concat([new_patient, data], ignore_index=True)  
    save_data(data)
def display_patients():
    global data
    S.write(data)
def update_patient(id, column, value):
    global data
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        data.loc[data['id'].astype(str).str.strip() == id, column] = value
        save_data(data)
        S.success('Patient data updated successfully')
    else:
        S.error('Patient ID not found')
def delete_patient(id):
    global data
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        data = data[data['id'].astype(str).str.strip() != id]
        save_data(data)
        S.success('Patient data deleted successfully')
    else:
        S.error('Patient ID not found')
def search_patient(id):
    global data
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        patient = data[data['id'].astype(str).str.strip() == id]
        S.write(patient)
    else:
        S.error('Patient ID not found')
S.title('Hospital Patients ')
data = load_data()
menu = S.sidebar.selectbox('Menu', ['Add Patient', 'View Patients', 'Update Patient', 'Delete Patient', 'Search Patient'])
if menu == 'Add Patient':
    S.sidebar.header('Add New Patient')
    patient_id = S.sidebar.text_input('ID')
    gender = S.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
    age = S.sidebar.number_input('Age', min_value=0, max_value=150)
    hypertension = S.sidebar.checkbox('Hypertension')
    heart_disease = S.sidebar.checkbox('Heart Disease')
    ever_married = S.sidebar.selectbox('Ever Married', ['Yes', 'No'])
    work_type = S.sidebar.selectbox('Work Type', ['Private', 'Self-employed', 'Govt_job', 'Children', 'Never_worked'])
    residence_type = S.sidebar.selectbox('Residence Type', ['Urban', 'Rural'])
    avg_glucose_level = S.sidebar.number_input('Average Glucose Level')
    bmi = S.sidebar.number_input('BMI')
    smoking_status = S.sidebar.selectbox('Smoking Status', ['Smokes', 'Formerly Smoked', 'Never Smoked', 'Unknown'])
    stroke = S.sidebar.checkbox('Stroke')
    if S.sidebar.button('Add'):
        add_patient(patient_id, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke)
        S.success('Patient added successfully')
elif menu == 'View Patients':
    S.header('View Patients')
    display_patients()
elif menu == 'Update Patient':
    S.sidebar.header('Update Patient')
    patient_id = S.sidebar.text_input('ID')
    column = S.sidebar.selectbox('Select Column', data.columns)
    new_value = S.sidebar.text_input('New Value')
    if S.sidebar.button('Update'):
        update_patient(patient_id, column, new_value)
elif menu == 'Delete Patient':
    S.sidebar.header('Delete Patient')
    patient_id = S.sidebar.text_input('ID')
    if S.sidebar.button('Delete'):
        delete_patient(patient_id)
elif menu == 'Search Patient':
    S.sidebar.header('Search Patient')
    patient_id = S.sidebar.text_input('ID')
    if S.sidebar.button('Search'):
        search_patient(patient_id)
