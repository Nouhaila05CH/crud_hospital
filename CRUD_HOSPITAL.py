import streamlit as st
import pandas as pd

# Function to load data
def load_data():
    try:
        data = pd.read_csv("patients.csv")
        st.write("Data loaded successfully")
    except FileNotFoundError:
        data = pd.DataFrame(columns=['id', 'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])
        st.write("No data file found")
    return data

# Function to save data
def save_data(data):
    data.to_csv("patients.csv", index=False)

# Function to add a patient
def add_patient(patient_data):
    data = load_data()
    data = pd.concat([patient_data, data], ignore_index=True)
    save_data(data)
    st.success('Patient added successfully')

# Function to display patients
def display_patients():
    data = load_data()
    st.write(data)

# Function to update patient information
def update_patient(id, column, value):
    data = load_data()
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        data.loc[data['id'].astype(str).str.strip() == id, column] = value
        save_data(data)
        st.success('Patient information updated successfully')
    else:
        st.error('Patient ID not found')

# Function to delete a patient
def delete_patient(id):
    data = load_data()
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        data = data[data['id'].astype(str).str.strip() != id]
        save_data(data)
        st.success('Patient information deleted successfully')
    else:
        st.error('Patient ID not found')

# Function to search for a patient
def search_patient(id):
    data = load_data()
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        patient = data[data['id'].astype(str).str.strip() == id]
        st.write(patient)
    else:
        st.error('Patient ID not found')

# Main function of the application
def main():
    st.title('Hospital Patients')

    menu = st.sidebar.selectbox('Menu', ['Add Patient', 'Display Patients', 'Update Patient', 'Delete Patient', 'Search Patient'])

    if menu == 'Add Patient':
        st.sidebar.header('Add a New Patient')
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
            patient_data = pd.DataFrame({'id': [patient_id], 'gender': [gender], 'age': [age], 'hypertension': [hypertension], 'heart_disease': [heart_disease], 'ever_married': [ever_married], 'work_type': [work_type], 'residence_type': [residence_type], 'avg_glucose_level': [avg_glucose_level], 'bmi': [bmi], 'smoking_status': [smoking_status], 'stroke': [stroke]})
            add_patient(patient_data)

    elif menu == 'Display Patients':
        st.header('Display Patients')
        display_patients()

    elif menu == 'Update Patient':
        st.sidebar.header('Update Patient')
        patient_id = st.sidebar.text_input('ID')
        column = st.sidebar.selectbox('Select Column', ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])
        new_value = st.sidebar.text_input('New Value')
        if st.sidebar.button('Update'):
            update_patient(patient_id, column, new_value)

    elif menu == 'Delete Patient':
        st.sidebar.header('Delete Patient')
        patient_id = st.sidebar.text_input('ID')
        if st.sidebar.button('Delete'):
            delete_patient(patient_id)

    elif menu == 'Search Patient':
        st.sidebar.header('Search Patient')
        patient_id = st.sidebar.text_input('ID')
        if st.sidebar.button('Search'):
            search_patient(patient_id)

# Call the main function
if __name__ == "__main__":
    main()
