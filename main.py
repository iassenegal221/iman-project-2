import streamlit as st
import pandas as pd


def load_excel_data(file_path):
    # Load the Excel file into a DataFrame
    excel_data = pd.read_excel(file_path, sheet_name=None)
    return excel_data


import pandas as pd

import pandas as pd

def filter_unpaid_students(data, selected_sheet, selected_months):
    sheet_data = data[selected_sheet]
    required_columns = ['NOM', 'PRENOMS', 'N° DE SCOLARITE'] + selected_months
    filtered_data = sheet_data[required_columns].copy()

    for month in selected_months:
        filtered_data[month] = filtered_data[month].fillna("Impayé")

    unpaid_students = pd.DataFrame(columns=required_columns)

    for month in selected_months:
        unpaid_students = pd.concat([unpaid_students, filtered_data.loc[filtered_data[month] == "Impayé"]])

    return unpaid_students, filtered_data




def display_student_unpaid_months(data, student_name, months):
    student_data = data[(data['NOM'] + ' ' + data['PRENOMS']) == student_name]

    for month in months:
        student_data[month] = student_data[month].fillna("Impayé")

    has_paid = all(student_data[month].values[0] != "Impayé" for month in months)

    student_info = pd.DataFrame(columns=['N° DE SCOLARITE', 'Nom', 'Prénoms', 'Statut paiement'])

    if not student_data.empty:
        if has_paid:
            student_info.loc[0] = [student_data['N° DE SCOLARITE'].values[0],
                                   student_data['NOM'].values[0],
                                   student_data['PRENOMS'].values[0],
                                   "Payé"]
        else:
            student_info.loc[0] = [student_data['N° DE SCOLARITE'].values[0],
                                   student_data['NOM'].values[0],
                                   student_data['PRENOMS'].values[0],
                                   "Impayé"]

    return student_info



def main():
  page = st.sidebar.selectbox("Veuillez sélectionner une page", ["Analyse globale", "Analyse par étudiant"])
  if page == "Analyse globale":
        st.image('logo.jpeg')
        st.markdown("<h1 style='text-align: center; color: black;'>Mon tableau de bord d'analyse automatisée</h1>",
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Veuillez sélectionner le bon fichier Excel", type=["xls", "xlsx"])

        if uploaded_file:
            excel_data = load_excel_data(uploaded_file)
            sheet_names = list(excel_data.keys())

            st.title("Mon tableau de bord d'analyse automatisée")
            st.write("Veuillez sélectionner ce que vous voulez faire.")

            st.session_state.uploaded_file = uploaded_file
            st.session_state.excel_data = excel_data
            st.session_state.sheet_names = sheet_names

            selected_sheets = st.multiselect("Veuillez sélectionner une ou plusieurs classes", sheet_names)
            selected_months = st.multiselect("Veuillez sélectionner un ou plusieurs mois",
                                            ['JANIER', 'FEVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN', "JUILLET",
                                            "AOÛT", "SEPTEMBRE", "OCTOBRE", 'NOVEMBRE', 'DECEMBRE'])
            unpaid_students = {}
            filtered_data = {}
            for sheet_name in selected_sheets:
                unpaid_students[sheet_name], filtered_data[sheet_name] = filter_unpaid_students(excel_data, sheet_name,
                                                                                                selected_months)
                st.write("Classe:", sheet_name)
                st.table(unpaid_students[sheet_name])


  elif page == "Analyse par étudiant":
        st.title("Analyse par étudiant")
        selected_sheet = st.selectbox("Veuillez sélectionner une classe",
                                    st.session_state.sheet_names if 'sheet_names' in st.session_state else [])
        if selected_sheet:
            students_data = st.session_state.excel_data[selected_sheet]
            student_names = students_data['NOM'] + ' ' + students_data['PRENOMS']
            selected_student = st.selectbox("Veuillez sélectionner un étudiant", student_names)

            if selected_student:
                excel_data = st.session_state.excel_data
                selected_months = st.multiselect("Veuillez sélectionner un ou plusieurs mois",
                                                ['FEVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN', "JUILLET", "AOÛT"])

                unpaid_students, filtered_data = filter_unpaid_students(excel_data, selected_sheet,
                                                                        selected_months)

                combined_data = filtered_data[
                    (filtered_data['NOM'] + ' ' + filtered_data['PRENOMS']) == selected_student]
                st.table(combined_data)



if __name__ == "__main__":
    main()
