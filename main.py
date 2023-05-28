import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook

# Chargement du fichier Excel
@st.cache_data()
def load_excel_file(file):
    xls = pd.ExcelFile(file)
    sheets = xls.sheet_names
    data = {}
    workbook = load_workbook(file)
    for sheet in sheets:
        sheet_data = workbook[sheet]
        data[sheet] = pd.DataFrame(sheet_data.values)
        data[sheet].columns = data[sheet].iloc[0]
        data[sheet] = data[sheet][1:]
    return data

# Affichage des données du sheet sélectionné
def display_sheet_data(sheet_data):
    st.write("Données correspondant aux options choisies:")
    st.dataframe(sheet_data)

# Filtrer les données en fonction du niveau et de la classe
def filter_sheet_data(sheet_data, niveau=None, classe=None):
    filtered_data = sheet_data
    if niveau is not None:
        filtered_data = filtered_data[filtered_data['Niveau'] == niveau]
    if classe is not None:
        filtered_data = filtered_data[filtered_data['Classe'] == classe]
    return filtered_data


# Calcul du nombre d'étudiants n'ayant pas payé
def calculate_unpaid_students(sheet_data):
    unpaid_students = sheet_data[sheet_data['Montant'] > 0]
    return len(unpaid_students)

# Création du graphique de répartition
def create_distribution_chart(sheet_data):
    distribution = sheet_data['Niveau'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(distribution.index, distribution.values)
    ax.set_xlabel('Niveau')
    ax.set_ylabel("Nombre d'étudiants")
    ax.set_title('Répartition des étudiants par niveau')
    st.pyplot(fig)

# Création du graphique du total Montant par sheet
def create_total_montant_chart(data):
    sheet_names = list(data.keys())
    total_montant = []
    for sheet_name in sheet_names:
        sheet_data = data[sheet_name]
        total = sheet_data['Montant'].sum()
        total_montant.append(total)

    # Sort the sheet names and total montant in descending order
    sheet_names, total_montant = zip(*sorted(zip(sheet_names, total_montant), key=lambda x: x[1], reverse=True))

    fig, ax = plt.subplots(figsize=(15, 12))  # Adjust the figsize according to your preferences
    plt.yticks(rotation=0)  # Rotate y-axis labels if needed
    ax.barh(sheet_names, total_montant)

    # Add labels on the right side of the bars
    for i, v in enumerate(total_montant):
        ax.text(v, i, f"{v:,} FCFA", ha='left', va='center')

    ax.set_xlabel('Montant total')
    ax.set_ylabel('Fillière')
    ax.set_title('Montant total impayé par fillière (toute classe et tout niveau)')
    st.pyplot(fig)



def main():
    st.image('logo.jpeg')
    st.markdown("<h1 style='text-align: center; color: black;'>Mon tableau de bord d'analyse automatisée</h1>", unsafe_allow_html=True)
    file = st.file_uploader("Veuillez sélectionner le bon fichier excel", type=["xls", "xlsx"])
    return file


# Chargement du fichier Excel

if __name__ =="__main__":
    file = main()
    if file is not None:
        data = load_excel_file(file)

        # Sélection du sheet
        selected_sheet = st.selectbox("Sélectionnez le sheet", list(data.keys()))

        # Filtrer par Niveau et Classe (options supplémentaires)
        sheet_data = data[selected_sheet]
        niveaux = sheet_data['Niveau'].unique()
        classes = sheet_data['Classe'].unique()

        selected_niveau = st.selectbox("Sélectionnez le niveau", [None] + list(niveaux))
        selected_classe = st.selectbox("Sélectionnez la classe", [None] + list(classes))

        # Filtrer les données en fonction du niveau et de la classe
        filtered_data = filter_sheet_data(sheet_data, selected_niveau, selected_classe)

        # Affichage des données filtrées
        display_sheet_data(filtered_data)

        # Calcul du nombre d'étudiants n'ayant pas payé
        unpaid_count = calculate_unpaid_students(filtered_data)

        if unpaid_count > 1:
            st.write("Nombre d'étudiants n'ayant pas payé dans la fillière:", unpaid_count, "étudiants")
        else:
            st.write("Nombre d'étudiants n'ayant pas payé dans la fillière:", unpaid_count, "étudiant")



     
        # Création du graphique du total Montant par sheet
        create_total_montant_chart(data)



