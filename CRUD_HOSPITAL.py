import streamlit as S
import pandas as P

# Fonction pour charger les données
def load_data():
    try:
        data = P.read_csv("patients.csv")
        S.write("Données chargées avec succès")
    except FileNotFoundError:
        data = P.DataFrame(columns=['id', 'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke'])
        S.write("Aucun fichier de données trouvé")
    return data

# Fonction pour sauvegarder les données
def save_data(data):
    data.to_csv("patients.csv", index=False)

# Fonction pour ajouter un patient
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

# Fonction pour afficher les patients
def display_patients():
    global data
    S.write(data)

# Fonction pour mettre à jour les informations d'un patient
def update_patient(id, column, value):
    global data
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        data.loc[data['id'].astype(str).str.strip() == id, column] = value
        save_data(data)
        S.success('Informations du patient mises à jour avec succès')
    else:
        S.error('Identifiant du patient non trouvé')

# Fonction pour supprimer un patient
def delete_patient(id):
    global data
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        data = data[data['id'].astype(str).str.strip() != id]
        save_data(data)
        S.success('Informations du patient supprimées avec succès')
    else:
        S.error('Identifiant du patient non trouvé')

# Fonction pour rechercher un patient
def search_patient(id):
    global data
    id = id.strip()
    if id in data['id'].astype(str).str.strip().values:
        patient = data[data['id'].astype(str).str.strip() == id]
        S.write(patient)
    else:
        S.error('Identifiant du patient non trouvé')

# Fonction de connexion
def login():
    S.title("Connexion")
    username = S.text_input("Nom d'utilisateur")
    password = S.text_input("Mot de passe", type="password")
    if S.button("Se connecter"):
        # Valider les informations de connexion
        if username == "admin" and password == "password":
            S.success("Connexion réussie")
            return True
        else:
            S.error("Nom d'utilisateur ou mot de passe incorrect")

# Fonction principale de l'application
def main():
    if login():
        # Les utilisateurs sont connectés, afficher le menu principal
        S.title('Patients de l\'hôpital')
        data = load_data()
        menu = S.sidebar.selectbox('Menu', ['Ajouter un patient', 'Afficher les patients', 'Mettre à jour un patient', 'Supprimer un patient', 'Rechercher un patient'])
        if menu == 'Ajouter un patient':
            S.sidebar.header('Ajouter un nouveau patient')
            patient_id = S.sidebar.text_input('ID')
            gender = S.sidebar.selectbox('Genre', ['Masculin', 'Féminin', 'Autre'])
            age = S.sidebar.number_input('Âge', min_value=0, max_value=150)
            hypertension = S.sidebar.checkbox('Hypertension')
            heart_disease = S.sidebar.checkbox('Maladie cardiaque')
            ever_married = S.sidebar.selectbox('Déjà marié', ['Oui', 'Non'])
            work_type = S.sidebar.selectbox('Type de travail', ['Privé', 'Indépendant', 'Emploi gouvernemental', 'Enfants', 'Jamais travaillé'])
            residence_type = S.sidebar.selectbox('Type de résidence', ['Urbain', 'Rural'])
            avg_glucose_level = S.sidebar.number_input('Niveau de glucose moyen')
            bmi = S.sidebar.number_input('IMC')
            smoking_status = S.sidebar.selectbox('Statut de fumeur', ['Fume', 'A arrêté de fumer', 'N\'a jamais fumé', 'Inconnu'])
            stroke = S.sidebar.checkbox('AVC')
            if S.sidebar.button('Ajouter'):
                add_patient(patient_id, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke)
                S.success('Patient ajouté avec succès')
        elif menu == 'Afficher les patients':
            S.header('Afficher les patients')
            display_patients()
        elif menu == 'Mettre à jour un patient':
            S.sidebar.header('Mettre à jour un patient')
            patient_id = S.sidebar.text_input('ID')
            column = S.sidebar.selectbox('Sélectionner une colonne', data.columns)
            new_value = S.sidebar.text_input('Nouvelle valeur')
            if S.sidebar.button('Mettre à jour'):
                update_patient(patient_id, column, new_value)
        elif menu == 'Supprimer un patient':
            S.sidebar.header('Supprimer un patient')
            patient_id = S.sidebar.text_input('ID')
            if S.sidebar.button('Supprimer'):
                delete_patient(patient_id)
        elif menu == 'Rechercher un patient':
            S.sidebar.header('Rechercher un patient')
            patient_id = S.sidebar.text_input('ID')
            if S.sidebar.button('Rechercher'):
                search_patient(patient_id)

# Appel de la fonction principale
if __name__ == "__main__":
    main()
