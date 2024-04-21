import streamlit as st
import pandas as pd

# Function to initialize or load the data
def load_data():
    try:
        df = pd.read_csv("hospital_patients.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Patient ID", "Name", "Age", "Gender", "Diagnosis"])
    return df

# Function to save data to CSV file
def save_data(df):
    df.to_csv("hospital_patients.csv", index=False)

# Main function to run the application
def main():
    st.title("Hospital Patient Management System")
    
    # Load data
    df = load_data()

    # Display sidebar with options
    menu = ["View Patients", "Add Patient", "Update Patient", "Delete Patient"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View Patients":
        st.subheader("View Patient Records")
        st.write(df)

    elif choice == "Add Patient":
        st.subheader("Add New Patient")
        patient_id = st.text_input("Patient ID")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=150)
        gender = st.selectbox("Gender", ["Male", "Female"])
        diagnosis = st.text_input("Diagnosis")
        
        if st.button("Add Patient"):
            new_patient = {"Patient ID": patient_id, "Name": name, "Age": age, "Gender": gender, "Diagnosis": diagnosis}
            df = df.append(new_patient, ignore_index=True)
            save_data(df)
            st.success("Patient added successfully!")

    elif choice == "Update Patient":
        st.subheader("Update Patient Information")
        patient_id = st.text_input("Enter Patient ID to update")
        patient_index = df[df["Patient ID"] == patient_id].index
        
        if len(patient_index) > 0:
            patient_index = patient_index[0]
            name = st.text_input("Name", value=df.loc[patient_index, "Name"])
            age = st.number_input("Age", min_value=0, max_value=150, value=df.loc[patient_index, "Age"])
            gender = st.selectbox("Gender", ["Male", "Female"], index=0 if df.loc[patient_index, "Gender"] == "Male" else 1)
            diagnosis = st.text_input("Diagnosis", value=df.loc[patient_index, "Diagnosis"])
            
            if st.button("Update Patient"):
                df.loc[patient_index] = [patient_id, name, age, gender, diagnosis]
                save_data(df)
                st.success("Patient information updated successfully!")
        else:
            st.warning("Patient ID not found!")

    elif choice == "Delete Patient":
        st.subheader("Delete Patient Record")
        patient_id = st.text_input("Enter Patient ID to delete")
        
        if st.button("Delete Patient"):
            df = df[df["Patient ID"] != patient_id]
            save_data(df)
            st.success("Patient record deleted successfully!")

if __name__ == "__main__":
    main()
