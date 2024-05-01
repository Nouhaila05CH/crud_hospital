import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    try:
        data = pd.read_csv("patients.csv")
        st.write("Données chargées avec succès")
    except FileNotFoundError:
        data = pd.DataFrame(columns=['id', 'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])
        st.write("Aucun fichier de données trouvé")
    return data

def save_data(data):
    data.to_csv("patients.csv", index=False)

def add_patient():
    st.sidebar.header('Ajouter un nouveau patient')
    id = st.sidebar.text_input('ID')
    gender = st.sidebar.radio('Genre', ['Male', 'Female', 'Other'])
    age = st.sidebar.number_input('Âge', min_value=0, max_value=150)
    hypertension = st.sidebar.checkbox('Hypertension')
    heart_disease = st.sidebar.checkbox('Maladie cardiaque')
    ever_married = st.sidebar.radio('Marié', ['Yes', 'No'])
    work_type = st.sidebar.selectbox('Type de travail', ['Privé', 'Indépendant', 'Emploi gouvernemental', 'Enfants', 'Jamais travaillé'])
    residence_type = st.sidebar.radio('Type de résidence', ['Urbain', 'Rural'])
    avg_glucose_level = st.sidebar.number_input('Niveau moyen de glucose')
    bmi = st.sidebar.number_input('IMC')
    smoking_status = st.sidebar.selectbox('Statut tabagique', ['Fumeur', 'Ancien fumeur', 'Jamais fumé', 'Inconnu'])
    stroke = st.sidebar.checkbox('AVC')
    if st.sidebar.button('Ajouter'):
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
        data = pd.concat([new_patient, load_data()], ignore_index=True)  
        save_data(data)
        st.success('Patient ajouté avec succès')

def display_patients():
    st.header('Liste des patients')
    st.write(load_data())

def update_patient():
    st.sidebar.header('Mettre à jour le patient')
    patient_id = st.sidebar.text_input('ID')
    column = st.sidebar.selectbox('Sélectionner la colonne', data.columns)
    new_value = st.sidebar.text_input('Nouvelle valeur')
    if st.sidebar.button('Mettre à jour'):
        if patient_id.strip() in data['id'].astype(str).str.strip().values:
            data.loc[data['id'].astype(str).str.strip() == patient_id.strip(), column] = new_value
            save_data(data)
            st.success('Données du patient mises à jour avec succès')
        else:
            st.error('ID du patient introuvable')

def delete_patient():
    st.sidebar.header('Supprimer le patient')
    patient_id = st.sidebar.text_input('ID')
    if st.sidebar.button('Supprimer'):
        if patient_id.strip() in data['id'].astype(str).str.strip().values:
            data = data[data['id'].astype(str).str.strip() != patient_id.strip()]
            save_data(data)
            st.success('Données du patient supprimées avec succès')
        else:
            st.error('ID du patient introuvable')

def search_patient():
    st.sidebar.header('Rechercher un patient')
    patient_id = st.sidebar.text_input('ID')
    if st.sidebar.button('Rechercher'):
        if patient_id.strip() in data['id'].astype(str).str.strip().values:
            patient = data[data['id'].astype(str).str.strip() == patient_id.strip()]
            st.write(patient)
        else:
            st.error('ID du patient introuvable')

def visualize_hypertension():
    st.subheader('Répartition de l\'hypertension')
    hypertension_counts = data['hypertension'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(hypertension_counts, labels=hypertension_counts.index, autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)
    st.write(hypertension_counts)

def visualize_heart_disease():
    st.subheader('Répartition des maladies cardiaques')
    heart_disease_counts = data['heart_disease'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(heart_disease_counts, labels=heart_disease_counts.index, autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)
    st.write(heart_disease_counts)

def visualize_smoking_status():
    st.subheader('Répartition du statut tabagique')
    smoking_status_counts = data['smoking_status'].value_counts()
    st.bar_chart(smoking_status_counts)
    st.write(smoking_status_counts)

st.title('Gestion des patients hospitaliers')
data = load_data()
menu = st.sidebar.selectbox('Menu', ['Ajouter un patient', 'Afficher les patients', 'Mettre à jour le patient', 'Supprimer le patient', 'Rechercher un patient', 'Visualiser l\'hypertension', 'Visualiser les maladies cardiaques', 'Visualiser le statut tabagique'])

if menu == 'Ajouter un patient':
    add_patient()
elif menu == 'Afficher les patients':
    display_patients()
elif menu == 'Mettre à jour le patient':
    update_patient()
elif menu == 'Supprimer le patient':
    delete_patient()
elif menu == 'Rechercher un patient':
    search_patient()
elif menu == 'Visualiser l\'hypertension':
    visualize_hypertension()
elif menu == 'Visualiser les maladies cardiaques':
    visualize_heart_disease()
elif menu == 'Visualiser le statut tabagique':
    visualize_smoking_status()
